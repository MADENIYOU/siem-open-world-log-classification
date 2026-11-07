"""Normalisation de logs de sécurité (TP2, étape 4).

Règles DÉTERMINISTES : aucune statistique n'est apprise sur les données, donc les appliquer au test ne crée pas de fuite.
"""
import re
import unicodedata

MONTHS = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
DAYS = "Mon|Tue|Wed|Thu|Fri|Sat|Sun"
PATTERNS = {   # ordre d'application : du plus spécifique au plus général
    "time": [
        re.compile(rf"\b(?:{DAYS})\s+(?:{MONTHS})\s+\d{{1,2}}\s+\d{{2}}:\d{{2}}:\d{{2}}\s+\d{{4}}\b"),
        re.compile(r"\b\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:[.,]\d+)?\b"),
        re.compile(rf"\b(?:{MONTHS})\s+\d{{1,2}}\s+\d{{2}}:\d{{2}}:\d{{2}}\b"),
        re.compile(r"\b\d{1,2}[./]\d{1,2}\s+\d{2}:\d{2}:\d{2}\b"),
        re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),
        re.compile(r"\b\d{2}:\d{2}:\d{2}\b"),
    ],
    "uuid": [re.compile(r"\b[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}\b")],
    "mac": [re.compile(r"\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b")],
    "ip": [re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")],
    "url": [re.compile(r"(?i)\b(?:https?|ftp)://[^\s\"'<>]+")],
    "email": [re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")],
    "hex": [re.compile(r"\b0x[0-9a-fA-F]+\b"), re.compile(r"\b(?=[0-9a-fA-F]*\d)(?=[0-9a-fA-F]*[a-fA-F])[0-9a-fA-F]{8,}\b")],
    "num": [re.compile(r"\b\d+(?:\.\d+)?\b")],
}
TOKENS = {"time": " timetok ", "uuid": " uuidtok ", "mac": " mactok ", "ip": " iptok ", "url": " urltok ", "email": " emailtok ", "hex": " hextok ", "num": " numtok "}
ORDER = ["time", "uuid", "mac", "ip", "url", "email", "hex", "num"]
WORD_RE = re.compile(r"[A-Za-z]{2,}")
WORD_PUNCT_RE = re.compile(r"[A-Za-z]{2,}|[^\sA-Za-z\d]")
CTRL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
SKLEARN_STOP = None


def normalize(text, mask=(), unicode_norm=True):
    """Texte -> texte : Unicode NFKC, retrait des caractères de contrôle, puis masquage typé des champs variables listés dans `mask`."""
    t = text.rstrip("\r\n")
    if unicode_norm:
        t = unicodedata.normalize("NFKC", t)
        t = CTRL_RE.sub(" ", t)
    for kind in ORDER:
        if kind in mask:
            for pat in PATTERNS[kind]:
                t = pat.sub(TOKENS[kind], t)
    return t


def tokenize(text, mask=(), lower=True, punct=False, stop=False, trunc=None, unicode_norm=True):
    """Texte -> liste de jetons. mask : types de champs remplacés par un jeton (ex. ('ip', 'time', 'num'))."""
    t = text[:trunc] if trunc else text
    t = normalize(t, mask, unicode_norm)
    toks = (WORD_PUNCT_RE if punct else WORD_RE).findall(t)
    if lower:
        toks = [w.lower() for w in toks]
    if stop:
        global SKLEARN_STOP
        if SKLEARN_STOP is None:
            from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
            SKLEARN_STOP = frozenset(ENGLISH_STOP_WORDS)
        toks = [w for w in toks if w.lower() not in SKLEARN_STOP]
    return toks
