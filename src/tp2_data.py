"""Lecture des six fichiers SIEVE et table des gabarits (TP2, protocole v3).
Les fichiers utilisent des fins de ligne Windows et des virgules dans les logs : on lit à la main (voir notebook, 1.2)."""
from pathlib import Path
import numpy as np
import pandas as pd


def read_sieve(path):
    cats, logs = [], []
    with open(path, encoding="utf-8", newline="") as fh:
        assert fh.readline().rstrip("\r\n") == "category,log"
        for line in fh:
            c, l = line.rstrip("\r\n").split(",", 1); cats.append(c); logs.append(l)
    return pd.DataFrame({"category": cats, "log": logs})


def load_versions(root):
    """Dictionnaire {version 0..5: DataFrame(category, log, version, row)}."""
    raw = Path(root) / "artifacts" / "data" / "raw" / "sieve_extracted"
    out = {}
    for v in range(6):
        d = read_sieve(raw / f"SIEVE_0{v}_100K.csv"); d["version"] = v; d["row"] = np.arange(len(d)); out[v] = d
    return out


def load_splits_v1(root):
    return pd.read_csv(Path(root) / "artifacts" / "data" / "splits_v1.csv.gz")


def group_table(splits_v1):
    """Une ligne par gabarit reconstruit : classe, nombre de logs, a-t-il servi de test dans le protocole v1 ?"""
    g = splits_v1.groupby("group").agg(category=("category", "first"), n_logs=("row", "size"),
                                       in_v1_test=("split", lambda s: bool((s == "test").any()))).reset_index()
    return g
