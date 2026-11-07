"""Attaques textuelles sur des logs de sécurité (TP2, étape 8).

Trois attaques qui ne dépendent PAS du modèle attaqué (elles ne le « regardent » pas), déterministes pour une graine donnée :
  - typos      : fautes de frappe dans des mots (échange de deux lettres voisines, lettre supprimée, lettre doublée) ;
  - homoglyphs : lettres latines remplacées par des lettres d'autres alphabets d'aspect identique (a -> а cyrillique...) ;
  - padding    : insertion de mots anodins (sans rapport avec le log) à des positions tirées au hasard.
Un spammeur, ou ici un attaquant qui veut brouiller un SIEM, peut faire les trois sans connaître le modèle.
"""
import random
import re

WORD = re.compile(r"[A-Za-z]{4,}")
HOMOGLYPH = {"a": "а", "e": "е", "o": "о", "p": "р", "c": "с", "x": "х", "y": "у", "i": "і",
             "A": "А", "E": "Е", "O": "О", "P": "Р", "C": "С", "X": "Х", "B": "В", "H": "Н", "M": "М", "T": "Т"}
INVERSE_HOMOGLYPH = {v: k for k, v in HOMOGLYPH.items()}
FILLER = ("the report update normal service message notice info default value current number list item record version module "
          "standard general common simple basic public random sample example another several various certain particular").split()


def typos(text, rate, seed=0):
    rnd = random.Random(seed)

    def mutate(m):
        w = m.group(0)
        if rnd.random() >= rate:
            return w
        i = rnd.randrange(1, len(w) - 1); op = rnd.choice(("swap", "drop", "dup"))
        if op == "swap":
            return w[:i] + w[i + 1] + w[i] + w[i + 2:]
        if op == "drop":
            return w[:i] + w[i + 1:]
        return w[:i] + w[i] + w[i:]
    return WORD.sub(mutate, text)


def homoglyphs(text, rate, seed=0):
    rnd = random.Random(seed)
    return "".join(HOMOGLYPH[c] if (c in HOMOGLYPH and rnd.random() < rate) else c for c in text)


def padding(text, rate, seed=0, filler=FILLER):
    rnd = random.Random(seed); words = text.split(" ")
    n_ins = max(1, int(round(rate * len(words)))) if rate > 0 else 0
    for _ in range(n_ins):
        words.insert(rnd.randrange(0, len(words) + 1), rnd.choice(filler))
    return " ".join(words)


def unconfuse(text):
    """Parade : remplace les homoglyphes connus par leur lettre latine (étape 9)."""
    return "".join(INVERSE_HOMOGLYPH.get(c, c) for c in text)


ATTACKS = {"typos": typos, "homoglyphs": homoglyphs, "padding": padding}


def robust_tokens(text):
    """Pipeline A précédé de la normalisation des homoglyphes (parade, étape 9). Fonction de module : sérialisable avec le modèle."""
    from tp2_logtext import tokenize
    return tokenize(unconfuse(text))
