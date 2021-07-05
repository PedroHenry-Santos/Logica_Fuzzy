import numpy as np


class Variavel:

    def __init__(self, faixa):
        self.parametros = {}
        self.pertinencia = np.zeros(faixa)
        self.faixa = faixa

    def preenche_parametros(self, a, m, n, b):
        self.parametros["a"] = a
        self.parametros["m"] = m
        self.parametros["n"] = n
        self.parametros["b"] = b

    def gera_pertinencia(
        self,
        faixa,
    ) -> None:
        for i in range(self.faixa):
            self.pertinencia[i] = max(min(
                (faixa[i] - self.parametros["a"]) /
                (self.parametros["m"] - self.parametros["a"]),
                1,
                (self.parametros["b"] - faixa[i]) /
                (self.parametros["b"] - self.parametros["n"])
            ), 0)
