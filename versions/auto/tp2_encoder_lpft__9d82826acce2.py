"""Encodeur DistilBERT : sonde linéaire puis affinage doux (LP-FT, Kumar et al. 2022) et adaptation par prédiction de mots masqués (MLM). Réutilise HierEncoder de tp2_encoder. Version L1 (2026-11-10)."""
import math, time, os
import numpy as np, torch, torch.nn as nn
from transformers import AutoTokenizer, AutoModelForMaskedLM, DataCollatorForLanguageModeling, get_linear_schedule_with_warmup
import tp2_encoder as E
TOK = "distilbert-base-uncased"


def train_lpft(name, texts, y_fine, y_fam, n_fine, n_fam, *, max_len=256, lp_epochs=1, lp_lr=1e-3, ft_epochs=2, ft_lr=1e-5, batch_size=32, seed=42, device=None, warmup=0.06):
    device = device or E.pick_device(); E.set_seed(seed); tok = AutoTokenizer.from_pretrained(TOK); model = E.HierEncoder(name, n_fine, n_fam).to(device)
    ids = tok(list(texts), truncation=True, max_length=max_len)["input_ids"]; yf = torch.tensor(np.asarray(y_fine), dtype=torch.long); yfa = torch.tensor(np.asarray(y_fam), dtype=torch.long); ce = nn.CrossEntropyLoss(); rng = np.random.default_rng(seed); t0 = time.perf_counter(); hist = []
    def run(epochs, params, lr, freeze_base):
        opt = torch.optim.AdamW(params, lr=lr, weight_decay=0.01); per_ep = math.ceil(len(ids) / batch_size); total = per_ep * epochs; sched = get_linear_schedule_with_warmup(opt, int(warmup * total), total); step = 0
        for ep in range(epochs):
            perm = rng.permutation(len(ids)); model.train()
            if freeze_base: model.base.eval()
            for b in range(per_ep):
                idx = perm[b * batch_size:(b + 1) * batch_size]; x, m = E._batch(ids, idx, tok.pad_token_id, device); lf, lc = model(x, m); loss = ce(lf, yfa[idx].to(device)) + ce(lc, yf[idx].to(device)); loss.backward()
                torch.nn.utils.clip_grad_norm_(params, 1.0); opt.step(); sched.step(); opt.zero_grad(set_to_none=True); step += 1
                if step % 50 == 0: hist.append(float(loss.item()))
    for p in model.base.parameters(): p.requires_grad = False
    run(lp_epochs, list(model.fam.parameters()) + list(model.fine.parameters()), lp_lr, True)
    for p in model.base.parameters(): p.requires_grad = True
    run(ft_epochs, list(model.parameters()), ft_lr, False)
    return model, tok, {"model": name, "lp_epochs": lp_epochs, "lp_lr": lp_lr, "ft_epochs": ft_epochs, "ft_lr": ft_lr, "device": device, "train_minutes": round((time.perf_counter() - t0) / 60, 2), "n_train": len(ids)}


def adapt_mlm(texts, out_dir, *, name=TOK, max_len=128, epochs=1, lr=5e-5, batch_size=32, seed=42, device=None, mlm_prob=0.15):
    """Poursuit le pré-entraînement (mots masqués) sur des logs SANS étiquette ; enregistre l'encodeur de base dans out_dir."""
    device = device or E.pick_device(); E.set_seed(seed); tok = AutoTokenizer.from_pretrained(TOK); model = AutoModelForMaskedLM.from_pretrained(name).to(device); col = DataCollatorForLanguageModeling(tok, mlm_probability=mlm_prob); enc = tok(list(texts), truncation=True, max_length=max_len)
    ex = [{"input_ids": a, "attention_mask": m} for a, m in zip(enc["input_ids"], enc["attention_mask"])]; rng = np.random.default_rng(seed); per_ep = math.ceil(len(ex) / batch_size); total = per_ep * epochs
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01); sched = get_linear_schedule_with_warmup(opt, int(0.06 * total), total); model.train(); t0 = time.perf_counter(); losses = []
    for ep in range(epochs):
        perm = rng.permutation(len(ex))
        for b in range(per_ep):
            batch = col([ex[j] for j in perm[b * batch_size:(b + 1) * batch_size]]); batch = {k: v.to(device) for k, v in batch.items()}; loss = model(**batch).loss; loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step(); sched.step(); opt.zero_grad(set_to_none=True)
            if b % 50 == 0: losses.append(float(loss.item()))
    os.makedirs(out_dir, exist_ok=True); model.distilbert.save_pretrained(out_dir)
    return {"mlm_minutes": round((time.perf_counter() - t0) / 60, 2), "n_texts": len(ex), "loss_first": losses[0], "loss_last": losses[-1], "epochs": epochs}
