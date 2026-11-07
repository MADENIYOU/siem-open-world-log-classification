"""Exécute le notebook TP2 de bout en bout et le réécrit avec ses sorties.
Usage (depuis TP/TP1, avec son environnement) :  env -u MPLBACKEND .venv312/bin/python ../TP2/scripts/run_notebook.py
NE PAS définir MPLBACKEND=Agg : les figures en ligne disparaîtraient. Délai par cellule : 1 500 s (en cas d'échec, le notebook n'est pas réécrit ;
les calculs mis en cache le sont, on relance simplement)."""
import time
from pathlib import Path
import nbformat
from nbclient import NotebookClient
ROOT = Path(__file__).resolve().parents[1]; NB = ROOT / "TP2_logs_hierarchique_monde_ouvert.ipynb"; t0 = time.time()
import shutil, time as _t
(ROOT / 'archive' / 'notebook').mkdir(parents=True, exist_ok=True); shutil.copy2(NB, ROOT / 'archive' / 'notebook' / f"TP2_{_t.strftime('%Y%m%d-%H%M%S')}.ipynb")   # règle : on garde toujours le précédent (archive_state.py pour les résultats)
nb = nbformat.read(NB, as_version=4)
NotebookClient(nb, timeout=1500, kernel_name="python3", resources={"metadata": {"path": str(ROOT)}}).execute()
nbformat.write(nb, NB)
print("OK en %.0f s ; erreurs: %d ; cellules: %d" % (time.time() - t0, sum(1 for c in nb.cells if c.cell_type == "code" for o in c.outputs if o.output_type == "error"), len(nb.cells)))
