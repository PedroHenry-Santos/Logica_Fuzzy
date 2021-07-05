import numpy as np
import matplotlib.pyplot as plt

from classes.Variavel import Variavel


class Universo:

    def __init__(self, nome):
        self.nome = nome
        self.faixa = 0
        self.variaveis = {}
        self.singleton = []
        self.interseccoes = {}

    def cria_faixa(self, inicio, fim, variacao):
        self.faixa = np.linspace(inicio, fim, variacao)

    def cria_variavel(self, nome):
        self.variaveis[nome] = Variavel(len(self.faixa))

    def verifica_interseccoes(self):
        estado_do_valor = []
        for k in range(len(self.singleton)):
            for i in self.variaveis:
                if (self.variaveis[i].pertinencia[
                    list(self.singleton[k]).index(1)
                ] > 0):
                    estado_do_valor.append(i)

            print("O Caso %d se encontra na(s) seguinte(s) regiões de(a) %s:" %
                  (k + 1, self.nome))

            for j in estado_do_valor:
                if (j == "baixa" or j == "pequeno"):
                    print("-"+"\033[1;34m"+" %s\033[0;0m" % (j))
                elif (j == "alta" or j == "grande"):
                    print("-"+"\033[1;32m"+" %s\033[0;0m" % (j))
                elif (j == "media" or j == "medio"):
                    print("-"+"\033[1;91m"+" %s\033[0;0m" % (j))

            self.interseccoes["caso "+str(k + 1)] = estado_do_valor.copy()
            estado_do_valor.clear()

    def imprimir_regiao(self):
        plt.title(self.nome)
        plt.xlabel('x')
        plt.ylabel('u(x)')
        for i in self.variaveis:
            plt.plot(
                self.faixa,
                self.variaveis[i].pertinencia,
                label=i
            )
            plt.fill_between(self.faixa,
                             self.variaveis[i].pertinencia,
                             alpha=0.5,
                             where=(self.variaveis[i].pertinencia > 0)
                             )
        plt.legend()

    def cria_singleton(self, valor):

        for i in range(len(valor)):
            indice = np.argmin(np.abs(self.faixa - valor[i]))
            singleton = np.zeros(len(self.faixa))
            singleton[indice] = 1
            self.singleton.append(singleton)

        contador = 0

        quantidade = np.ceil(len(valor) / 2).astype(int)
        interacoes = np.floor(len(valor) / 2).astype(int)
        contador = 0

        plt.figure(figsize=(15, quantidade * 3))

        for i in range(int(interacoes)):
            subprot = int(str(quantidade) + '2' + str(contador + 1))
            plt.subplot(subprot)
            self.imprimir_regiao()
            plt.plot(self.faixa, self.singleton[contador], label=(
                "Singleton " + str(contador + 1)))
            plt.fill_between(self.faixa,
                             self.singleton[contador],
                             alpha=0.5,
                             where=(self.singleton[contador] > 0)
                             )
            plt.legend()
            contador += 1
            subprot = int(str(quantidade) + '2' + str(contador + 1))
            plt.subplot(subprot)
            self.imprimir_regiao()
            plt.plot(self.faixa, self.singleton[contador], label=(
                "Singleton " + str(contador + 1)))
            plt.fill_between(self.faixa,
                             self.singleton[contador],
                             alpha=0.5,
                             where=(self.singleton[contador] > 0)
                             )
            plt.legend()
            contador += 1

        if (quantidade > interacoes):
            subprot = int(str(quantidade) + '2' + str(contador + 1))
            plt.subplot(subprot)
            self.imprimir_regiao()
            plt.plot(self.faixa, self.singleton[contador], label=(
                "Singleton " + str(contador + 1)))
            plt.fill_between(self.faixa,
                             self.singleton[contador],
                             alpha=0.5,
                             where=(self.singleton[contador] > 0)
                             )
            plt.legend()

        plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95,
                            hspace=0.5, wspace=0.35)
