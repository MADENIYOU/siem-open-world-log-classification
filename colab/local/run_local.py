"""Calcul local (Mac, GPU Apple MPS) des rotations de l'encodeur TP2 : mêmes réglages que le Colab v2.
Usage : python run_local.py 5 4 3   (numéros de rotation 1..5, dans l'ordre voulu). Calcul uniquement, aucune analyse."""
import json, os, sys, time
import numpy as np, pandas as pd, torch
sys.path.insert(0, os.path.dirname(__file__))
import tp2_encoder as E
HERE = os.path.dirname(os.path.abspath(__file__)); COL = os.path.dirname(HERE)
OUT = os.path.join(COL, 'out_v2_local'); MOD = os.path.join(COL, '..', 'artifacts', 'models', 'encoder_local'); os.makedirs(OUT, exist_ok=True); os.makedirs(MOD, exist_ok=True)
df = pd.read_csv(os.path.join(COL, 'encoder_data_v2.csv.gz')); df['text'] = df.text.fillna(''); tax = json.load(open(os.path.join(COL, 'taxonomy_and_rotations_v1.json')))
tr = df[df.split == 'train'].reset_index(drop=True); va = df[df.split == 'val'].reset_index(drop=True); te = df[df.split == 'test'].reset_index(drop=True)
FAMS = sorted(tax['taxonomy']); PAPER = tax['classes_paper_order']; ROT = tax['rotations']
print(len(tr), 'train |', len(va), 'val |', len(te), 'test | device', E.pick_device(), flush=True)
NAME, MAXLEN = 'distilbert-base-uncased', 256
for r in [int(a) for a in sys.argv[1:]]:
    rot = r - 1; tag = f'uncased_rot{r}_len{MAXLEN}_s42'
    if os.path.exists(f'{OUT}/{tag}_test.npz'): print('déjà fait :', tag, flush=True); continue
    hidden = set(ROT[rot]); known = [c for c in PAPER if c not in hidden]; c2i = {c: i for i, c in enumerate(known)}; f2i = {f: i for i, f in enumerate(FAMS)}
    t0 = time.time(); tk = tr[tr.category.isin(known)].reset_index(drop=True)
    if os.path.exists(f'{MOD}/{tag}.pt'):
        tok = E.AutoTokenizer.from_pretrained(NAME); model = E.HierEncoder(NAME, len(known), len(FAMS)).to(E.pick_device()); model.load_state_dict(torch.load(f'{MOD}/{tag}.pt', map_location='cpu')); info = json.load(open(f'{MOD}/{tag}.info.json')); print(tag, 'modèle rechargé', flush=True)
    else:
        model, tok, info = E.train_encoder(NAME, tk.text.values, tk.category.map(c2i).values, tk.family.map(f2i).values, len(known), len(FAMS), max_len=MAXLEN, epochs=2, lr=3e-5, batch_size=32, seed=42, ckpt_path=f'{MOD}/{tag}.ckpt')
        torch.save(model.state_dict(), f'{MOD}/{tag}.pt'); json.dump(info, open(f'{MOD}/{tag}.info.json', 'w')); print(tag, 'entraîné', info['train_minutes'], 'min', flush=True)
    for nm, d in (('val', va), ('test', te)):
        t1 = time.time(); out = E.predict(model, tok, d.text.values, max_len=MAXLEN, mc=10); np.savez_compressed(f'{OUT}/{tag}_{nm}.npz', **out); print(' ', nm, 'prédit en', round((time.time() - t1) / 60, 1), 'min', flush=True)
    json.dump({'tag': tag, 'known': known, 'families': FAMS, 'hidden': sorted(hidden), 'info': info, 'hardware': 'Apple M3 Pro (MPS), local'}, open(f'{OUT}/{tag}.json', 'w'), indent=1)
    acc = (np.load(f'{OUT}/{tag}_test.npz')['logits_fine'].argmax(1) == te.category.map(lambda c: c2i.get(c, -1)).values)[te.category.isin(known)].mean()
    print(f"{tag}: exactitude fermée connus (test) {acc:.3f} ; total {time.time() - t0:.0f} s", flush=True)
