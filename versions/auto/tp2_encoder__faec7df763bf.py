"""Encodeur Transformer hiérarchique pour logs en monde ouvert (TP2, étape 6). Calcul sur GPU (Colab ou Kaggle).

Une base (DistilBERT / BERT) + deux têtes linéaires : famille (F sorties) et classe fine (K sorties, classes CONNUES seulement).
Perte = entropie croisée famille + entropie croisée classe fine. À l'inférence : logits des deux têtes, et Monte-Carlo dropout
(T passages avec dropout actif) pour estimer l'incertitude. Les scores d'incertitude sont calculés ensuite, en local.
"""
import json
import math, os
import random
import time

import numpy as np
import torch
import torch.nn as nn
from transformers import AutoModel, AutoTokenizer, get_linear_schedule_with_warmup


def pick_device():
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def set_seed(seed):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


class HierEncoder(nn.Module):
    def __init__(self, name, n_fine, n_fam, dropout=0.1):
        super().__init__()
        self.base = AutoModel.from_pretrained(name, attn_implementation=None if torch.cuda.is_available() else "eager")   # hors GPU CUDA (Mac MPS, CPU) : attention classique, car l'attention rapide ne gère pas le dropout (MC dropout)
        h = self.base.config.hidden_size
        self.drop = nn.Dropout(dropout); self.fam = nn.Linear(h, n_fam); self.fine = nn.Linear(h, n_fine)

    def forward(self, input_ids, attention_mask):
        out = self.base(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state
        m = attention_mask.unsqueeze(-1).float(); pooled = (out * m).sum(1) / m.sum(1)      # moyenne des jetons, remplissage exclu
        z = self.drop(pooled)
        return self.fam(z), self.fine(z)


def _batch(ids, idx, pad_id, device):
    L = max(len(ids[j]) for j in idx)
    x = torch.full((len(idx), L), pad_id, dtype=torch.long); m = torch.zeros((len(idx), L), dtype=torch.long)
    for r, j in enumerate(idx):
        x[r, :len(ids[j])] = torch.tensor(ids[j]); m[r, :len(ids[j])] = 1
    return x.to(device), m.to(device)


def train_encoder(name, texts, y_fine, y_fam, n_fine, n_fam, *, max_len=256, epochs=2, lr=3e-5, batch_size=32, seed=42, device=None, warmup=0.06, ckpt_path=None, ckpt_every=200):
    device = device or pick_device(); set_seed(seed)
    tok = AutoTokenizer.from_pretrained(name); model = HierEncoder(name, n_fine, n_fam).to(device)
    ids = tok(list(texts), truncation=True, max_length=max_len)["input_ids"]
    yf = torch.tensor(np.asarray(y_fine), dtype=torch.long); yfa = torch.tensor(np.asarray(y_fam), dtype=torch.long)
    total = math.ceil(len(ids) / batch_size) * epochs
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01); sched = get_linear_schedule_with_warmup(opt, int(warmup * total), total)
    ce = nn.CrossEntropyLoss(); rng = np.random.default_rng(seed); step = 0; t0 = time.perf_counter(); hist = []; run = 0.0
    perms = [rng.permutation(len(ids)) for _ in range(epochs)]                              # ordre des lots fixé d'avance : une reprise rejoue exactement la même suite
    per_ep = math.ceil(len(ids) / batch_size); t_before = 0.0
    if ckpt_path and os.path.exists(ckpt_path):                                              # REPRISE : on repart du dernier point de contrôle, pas de zéro
        ck = torch.load(ckpt_path, map_location="cpu"); model.load_state_dict(ck["model"]); opt.load_state_dict(ck["opt"]); sched.load_state_dict(ck["sched"])
        step, hist, run, t_before = ck["step"], ck["hist"], ck["run"], ck["elapsed"]; print(f"reprise de l'entraînement au pas {step}/{total}", flush=True)
    t0 = time.perf_counter() - t_before; model.train()
    while step < total:
        ep, b = divmod(step, per_ep); idx = perms[ep][b * batch_size:(b + 1) * batch_size]; x, m = _batch(ids, idx, tok.pad_token_id, device)
        lf, lc = model(x, m); loss = ce(lf, yfa[idx].to(device)) + ce(lc, yf[idx].to(device))
        loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step(); sched.step(); opt.zero_grad(set_to_none=True)
        step += 1; run += float(loss.item())
        if step % 100 == 0: hist.append({"step": step, "loss": run / 100, "min": round((time.perf_counter() - t0) / 60, 2)}); run = 0.0
        if ckpt_path and step % ckpt_every == 0 and step < total:                            # point de contrôle atomique (fichier temporaire puis remplacement)
            torch.save({"model": model.state_dict(), "opt": opt.state_dict(), "sched": sched.state_dict(), "step": step, "hist": hist, "run": run, "elapsed": time.perf_counter() - t0}, ckpt_path + ".tmp"); os.replace(ckpt_path + ".tmp", ckpt_path)
    if ckpt_path and os.path.exists(ckpt_path): os.remove(ckpt_path)
    info = {"model": name, "max_len": max_len, "epochs": epochs, "lr": lr, "batch_size": batch_size, "seed": seed, "device": device, "steps": step,
            "train_minutes": round((time.perf_counter() - t0) / 60, 2), "n_train": len(ids), "history": hist}
    return model, tok, info


@torch.no_grad()
def predict(model, tok, texts, *, max_len=256, batch_size=128, mc=10, device=None):
    device = device or pick_device(); model.to(device)
    ids = tok(list(texts), truncation=True, max_length=max_len)["input_ids"]; order = np.argsort([len(x) for x in ids])
    n = len(ids); nf = model.fine.out_features; nfa = model.fam.out_features
    out = {"logits_fine": np.zeros((n, nf), np.float32), "logits_fam": np.zeros((n, nfa), np.float32), "mc_fine": np.zeros((n, nf), np.float32), "mc_fam": np.zeros((n, nfa), np.float32)}
    for s in range(0, n, batch_size):
        idx = order[s:s + batch_size]; x, m = _batch(ids, idx, tok.pad_token_id, device)
        model.eval(); lf, lc = model(x, m); out["logits_fam"][idx] = lf.float().cpu().numpy(); out["logits_fine"][idx] = lc.float().cpu().numpy()
        if mc:
            model.train()                                                                    # dropout actif : T passages stochastiques
            pf = torch.zeros_like(lf); pc = torch.zeros_like(lc)
            for _ in range(mc):
                a, b = model(x, m); pf += torch.softmax(a.float(), -1); pc += torch.softmax(b.float(), -1)
            out["mc_fam"][idx] = (pf / mc).cpu().numpy(); out["mc_fine"][idx] = (pc / mc).cpu().numpy(); model.eval()
    return out


@torch.no_grad()
def embed(model, tok, texts, *, max_len=256, batch_size=128, device=None):
    """Vecteur de chaque log : moyenne des vecteurs de jetons (avant les têtes), mode évaluation, sans dropout (pour Mahalanobis et kNN)."""
    device = device or pick_device(); model.to(device).eval()
    ids = tok(list(texts), truncation=True, max_length=max_len)["input_ids"]; order = np.argsort([len(x) for x in ids]); out = np.zeros((len(ids), model.base.config.hidden_size), np.float32)
    for s in range(0, len(ids), batch_size):
        idx = order[s:s + batch_size]; x, m = _batch(ids, idx, tok.pad_token_id, device)
        h = model.base(input_ids=x, attention_mask=m).last_hidden_state; mm = m.unsqueeze(-1).float(); out[idx] = ((h * mm).sum(1) / mm.sum(1)).float().cpu().numpy()
    return out
