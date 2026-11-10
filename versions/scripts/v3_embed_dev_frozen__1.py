"""Embeddings GELÉS de DistilBERT (distilbert-base-uncased, sans réglage fin) pour les logs du DÉVELOPPEMENT seulement (v3_blockA.load()), moyenne des vecteurs de la dernière couche, longueur 128. Reprenable par blocs de 4096 logs.
Écrit artifacts/results/v3/emb_distilbert_frozen/part_XXXX.npy et index.json (empreinte de la liste des logs). Usage : python scripts/v3_embed_dev_frozen.py"""
import sys, os, json, hashlib, time, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
import numpy as np, torch
from transformers import AutoTokenizer, AutoModel
import v3_blockA as A
dev, _ = A.load(); texts = list(dev.log.values); OUT = ROOT / "artifacts" / "results" / "v3" / "emb_distilbert_frozen"; OUT.mkdir(parents=True, exist_ok=True); BLOCK = 4096
fp = hashlib.sha256("\n".join(texts).encode()).hexdigest(); idx = OUT / "index.json"
if idx.exists() and json.loads(idx.read_text())["sha256"] != fp: raise SystemExit("la liste des logs a changé : ne pas écraser (archiver le dossier)")
idx.write_text(json.dumps({"sha256": fp, "n": len(texts), "block": BLOCK, "model": "distilbert-base-uncased", "max_len": 128, "pooling": "moyenne des jetons, dernière couche"}))
dev_t = "mps" if torch.backends.mps.is_available() else "cpu"; tok = AutoTokenizer.from_pretrained("distilbert-base-uncased"); model = AutoModel.from_pretrained("distilbert-base-uncased").to(dev_t).eval(); t0 = time.time()
for b0 in range(0, len(texts), BLOCK):
    f = OUT / f"part_{b0 // BLOCK:04d}.npy"
    if f.exists(): continue
    chunk = texts[b0:b0 + BLOCK]; enc = tok(chunk, truncation=True, max_length=128)["input_ids"]; order = np.argsort([len(x) for x in enc]); out = np.zeros((len(chunk), 768), np.float32)
    with torch.no_grad():
        for s in range(0, len(chunk), 128):
            ii = order[s:s + 128]; L = max(len(enc[j]) for j in ii); x = torch.zeros((len(ii), L), dtype=torch.long); m = torch.zeros((len(ii), L), dtype=torch.long)
            for r, j in enumerate(ii): x[r, :len(enc[j])] = torch.tensor(enc[j]); m[r, :len(enc[j])] = 1
            h = model(input_ids=x.to(dev_t), attention_mask=m.to(dev_t)).last_hidden_state; mm = m.to(dev_t).unsqueeze(-1).float(); out[ii] = ((h * mm).sum(1) / mm.sum(1)).float().cpu().numpy()
    np.save(str(f) + ".tmp.npy", out); os.replace(str(f) + ".tmp.npy", f); print(f"bloc {b0 // BLOCK} / {(len(texts) - 1) // BLOCK} : {round((time.time() - t0) / 60, 1)} min", flush=True)
print("terminé", flush=True)
