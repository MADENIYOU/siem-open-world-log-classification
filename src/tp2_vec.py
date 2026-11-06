"""Vectorisation de logs par moyenne de vecteurs de mots (TP2, étape 5).

Familles de vecteurs de mots :
  - w2v_cbow, w2v_sg : Word2Vec appris sur les logs d'entraînement (gensim) ;
  - fasttext         : FastText (Skip-gram + n-grammes de caractères) appris sur les logs ;
  - glove            : GloVe pré-entraîné (Wikipedia + Gigaword), simplement chargé.

Un log devient la moyenne (éventuellement pondérée par l'IDF) des vecteurs de ses mots.
fit() n'est appelé que sur l'entraînement : jamais sur val ni test. Aucune étiquette n'est lue.
"""
import time

import numpy as np
import scipy.sparse as sps
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer

from tp2_logtext import tokenize as _tok


def tokenize(text):
    return _tok(text)                      # pipeline A : minuscules, mots de 2 lettres ou plus


def _identity(s):
    return s


class DocEmbedder(BaseEstimator, TransformerMixin):
    def __init__(self, kind="w2v_sg", dim=100, window=5, min_count=3, epochs=5, weighting="mean",
                 seed=42, workers=8, glove_path=None, bucket=200000):
        self.kind = kind; self.dim = dim; self.window = window; self.min_count = min_count
        self.epochs = epochs; self.weighting = weighting; self.seed = seed; self.workers = workers
        self.glove_path = glove_path; self.bucket = bucket

    def fit(self, texts, y=None):
        t0 = time.perf_counter()
        docs = [tokenize(t) for t in texts]
        if self.kind == "glove":
            from gensim.models import KeyedVectors
            self.wv_ = KeyedVectors.load(str(self.glove_path))
            self.dim = self.wv_.vector_size
        elif self.kind in ("w2v_cbow", "w2v_sg"):
            from gensim.models import Word2Vec
            m = Word2Vec(sentences=docs, vector_size=self.dim, window=self.window, min_count=self.min_count,
                         sg=int(self.kind == "w2v_sg"), epochs=self.epochs, workers=self.workers, seed=self.seed)
            self.wv_ = m.wv
        elif self.kind == "fasttext":
            from gensim.models import FastText
            m = FastText(sentences=docs, vector_size=self.dim, window=self.window, min_count=self.min_count,
                         sg=1, epochs=self.epochs, workers=self.workers, seed=self.seed, bucket=self.bucket,
                         min_n=3, max_n=6)
            self.wv_ = m.wv
        else:
            raise ValueError(self.kind)
        cv = CountVectorizer(tokenizer=_identity, preprocessor=None, lowercase=False, token_pattern=None, binary=True)
        Xb = cv.fit_transform(docs); df = np.asarray(Xb.sum(0)).ravel(); n = Xb.shape[0]
        self.idf_ = {w: float(np.log((1 + n) / (1 + d)) + 1.0) for w, d in zip(cv.get_feature_names_out(), df)}
        self.idf_default_ = float(np.log(1 + n) + 1.0)
        self.fit_seconds_ = time.perf_counter() - t0
        return self

    def transform(self, texts):
        docs = [tokenize(t) for t in texts]
        cv = CountVectorizer(tokenizer=_identity, preprocessor=None, lowercase=False, token_pattern=None)
        C = cv.fit_transform(docs).astype(np.float32).tocsr()
        words = cv.get_feature_names_out()
        E = np.zeros((len(words), self.dim), dtype=np.float32); known = np.zeros(len(words), dtype=np.float32)
        subwords = self.kind == "fasttext"
        for i, w in enumerate(words):
            if subwords or w in self.wv_.key_to_index:
                E[i] = self.wv_[w]; known[i] = 1.0
        wt = np.ones(len(words), dtype=np.float32)
        if self.weighting == "idf":
            wt = np.array([self.idf_.get(w, self.idf_default_) for w in words], dtype=np.float32)
        Cw = (C @ sps.diags(wt * known)).tocsr()
        num = Cw @ E
        den = np.asarray(Cw.sum(1)).ravel()
        out = np.zeros_like(num); nz = den > 0
        out[nz] = num[nz] / den[nz, None]
        tot = np.asarray(C.sum(1)).ravel(); cov = np.asarray((C @ sps.diags(known)).sum(1)).ravel()
        self.last_coverage_ = float(cov.sum() / max(tot.sum(), 1)); self.last_empty_ = float((~nz).mean())
        return out

    def __getstate__(self):
        st = self.__dict__.copy()
        if self.kind == "glove":
            st.pop("wv_", None)
        return st

    def __setstate__(self, st):
        self.__dict__.update(st)
        if self.kind == "glove" and "wv_" not in self.__dict__:
            from gensim.models import KeyedVectors
            self.wv_ = KeyedVectors.load(str(self.glove_path))
