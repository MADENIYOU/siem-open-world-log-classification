"""Jetons typés des logs (itération I2, version F1) : programme émetteur, noms de champs, types de valeurs, gabarit de forme.
Pas de dépendance au test : fonction pure du texte du log."""
import re
RE_PROG = re.compile(r"(?:^|\s)([A-Za-z][\w./-]{1,30})\[\d+\]:")
RE_KV = re.compile(r"([A-Za-z_][\w.-]{0,24})=(\"[^\"]*\"|\S+)")
RE_BR = re.compile(r"\[([A-Za-z][\w ]{0,20}?) ([^\]]{1,40})\]")
RE_TOK = re.compile(r"\S+")
RE_IP = re.compile(r"^\d{1,3}(\.\d{1,3}){3}(:\d+)?$"); RE_HEX = re.compile(r"^(0x)?[0-9a-fA-F]{8,}$"); RE_TIME = re.compile(r"^\d{1,2}:\d{2}(:\d{2})?"); RE_DATE = re.compile(r"^\d{1,4}[-/.]\d{1,2}[-/.]\d{1,4}$")
RE_MAIL = re.compile(r"^[^@\s]+@[^@\s]+\.\w+$"); RE_NUM = re.compile(r"^-?\d+([.,]\d+)?%?$")


def vtype(v):
    v = v.strip("\"'(),;[]")
    if not v: return "vide"
    if RE_IP.match(v): return "ip"
    if RE_MAIL.match(v): return "mail"
    if RE_TIME.match(v): return "heure"
    if RE_DATE.match(v): return "date"
    if RE_NUM.match(v): return "nombre"
    if RE_HEX.match(v): return "hex"
    if v.startswith("/") or "\\" in v: return "chemin"
    if re.search(r"\d", v) and re.search(r"[A-Za-z]", v): return "melange"
    return "mot"


def typed_tokens(text):
    out = []; m = RE_PROG.search(text)
    if m: out.append("prog_" + m.group(1).lower())
    for k, v in RE_KV.findall(text):
        k = k.lower(); out += ["champ_" + k, "ct_" + k + "_" + vtype(v)]
    for k, v in RE_BR.findall(text):
        k = k.lower().replace(" ", "_"); out += ["champ_" + k, "ct_" + k + "_" + vtype(v)]
    out.append("forme_" + "-".join(vtype(t)[:3] for t in RE_TOK.findall(text)[:8]))
    return out
