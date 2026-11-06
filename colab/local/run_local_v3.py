"""Calcul local (Mac, GPU Apple MPS) : encodeur à plusieurs graines et extraction des vecteurs (pour Mahalanobis et kNN, hypothèse H8).
Usage : python run_local_v3.py 43:1 43:2 ... (travaux « graine:rotation », dans l'ordre voulu). REPRENABLE : chaque travail saute ce qui est déjà fait
(poids, prédictions validation/test, vecteurs) et l'entraînement reprend à son dernier point de contrôle."""
import json, os, sys, time, shutil
import numpy as np, pandas as pd, torch
sys.path.insert(0, os.path.dirname(__file__))
import tp2_encoder as E
HERE = os.path.dirname(os.path.abspath(__file__)); COL = os.path.dirname(HERE)
OUT = os.path.join(COL, 'out_v3_local'); MOD = os.path.join(COL, '..', 'artifacts', 'models', 'encoder_local'); OLD_OUT = os.path.join(COL, 'out_v2_local'); os.makedirs(OUT, exist_ok=True); os.makedirs(MOD, exist_ok=True)
df = pd.read_csv(os.path.join(COL, 'encoder_data_v2.csv.gz')); df['text'] = df.text.fillna(''); tax = json.load(open(os.path.join(COL, 'taxonomy_and_rotations_v1.json')))
tr = df[df.split == 'train'].reset_index(drop=True); va = df[df.split == 'val'].reset_index(drop=True); te = df[df.split == 'test'].reset_index(drop=True)
FAMS = sorted(tax['taxonomy']); PAPER = tax['classes_paper_order']; ROT = tax['rotations']; NAME, MAXLEN = 'distilbert-base-uncased', 256
print(len(tr), 'train |', len(va), 'val |', len(te), 'test | device', E.pick_device(), flush=True)
for job in sys.argv[1:]:
    seed, r = [int(a) for a in job.split(':')]; rot = r - 1; tag = f'uncased_rot{r}_len{MAXLEN}_s{seed}'; vecf = f'{OUT}/{tag}_vec.npz'
    if os.path.exists(vecf) and os.path.exists(f'{OUT}/{tag}.json' if seed != 42 or r < 3 else vecf): print('déjà fait :', tag, flush=True); continue
    hidden = set(ROT[rot]); known = [c for c in PAPER if c not in hidden]; c2i = {c: i for i, c in enumerate(known)}; f2i = {f: i for i, f in enumerate(FAMS)}
    t0 = time.time(); tk = tr[tr.category.isin(known)].reset_index(drop=True); wt = f'{MOD}/{tag}.pt'; tok = E.AutoTokenizer.from_pretrained(NAME)
    if os.path.exists(wt):
        model = E.HierEncoder(NAME, len(known), len(FAMS)); model.load_state_dict(torch.load(wt, map_location='cpu')); model = model.to(E.pick_device()); info = json.load(open(f'{MOD}/{tag}.info.json')); print(tag, 'modèle rechargé', flush=True)
    else:
        model, tok, info = E.train_encoder(NAME, tk.text.values, tk.category.map(c2i).values, tk.family.map(f2i).values, len(known), len(FAMS), max_len=MAXLEN, epochs=2, lr=3e-5, batch_size=32, seed=seed, ckpt_path=f'{MOD}/{tag}.ckpt')
        torch.save(model.state_dict(), wt); json.dump(info, open(f'{MOD}/{tag}.info.json', 'w')); print(tag, 'entraîné', info['train_minutes'], 'min', flush=True)
    if not (seed == 42 and r >= 3):                                                          # seed 42, rotations 3 à 5 : prédictions déjà dans out_v2_local
        for nm, d in (('val', va), ('test', te)):
            if os.path.exists(f'{OUT}/{tag}_{nm}.npz'): continue
            t1 = time.time(); out = E.predict(model, tok, d.text.values, max_len=MAXLEN, mc=10); np.savez_compressed(f'{OUT}/{tag}_{nm}.npz', **out); print(' ', nm, 'prédit en', round((time.time() - t1) / 60, 1), 'min', flush=True)
        json.dump({'tag': tag, 'seed': seed, 'known': known, 'families': FAMS, 'hidden': sorted(hidden), 'info': info, 'hardware': 'Apple M3 Pro (MPS), local'}, open(f'{OUT}/{tag}.json', 'w'), indent=1)
    t1 = time.time(); np.savez_compressed(vecf, tr=E.embed(model, tok, tk.text.values, max_len=MAXLEN).astype(np.float16), y_tr=tk.category.values.astype(str), va=E.embed(model, tok, va.text.values, max_len=MAXLEN).astype(np.float16), te=E.embed(model, tok, te.text.values, max_len=MAXLEN).astype(np.float16))
    print(' ', 'vecteurs extraits en', round((time.time() - t1) / 60, 1), 'min ; total', round(time.time() - t0), 's', flush=True); del model
print('FIN', flush=True)
