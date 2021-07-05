import numpy as np
import matplotlib.pyplot as plt

from classes.Universo import Universo

# Lembrete: Com tempo criar uma maneira de adicionar regras dinamicamente
# com as verificações de limite de adições. Implementar:
# def adiciona_regras ():


class Fuzzy:
    def __init__(self):
        self.universos = {}
        self.conjunto_interseccoes = {}
        self.conjunto_regras_por_caso = {}
        self.regioes_de_resposta = {}
        self.defuzzificacao_por_caso = {}

    def cria_universo_discurso(self, nome):
        self.universos[nome] = Universo(nome)

    def centro_de_area(self):
        conjunto = []

        for u in self.regioes_de_resposta:

            valor = sum((
                self.regioes_de_resposta[u] * self.universos["Pressao"].faixa)
            ) / sum(self.regioes_de_resposta[u])

            conjunto.append(valor)
            print(
                "O centro de aréa do \033[1;35m%s: %f\033[0;0m"
                %
                (u, valor)
            )

        self.defuzzificacao_por_caso["centro de area"] = conjunto

    def media_dos_maximos(self):
        conjunto = []

        for u in self.regioes_de_resposta:

            valor_maximo = max(self.regioes_de_resposta[u])
            maximos = []
            contador = 0

            for i in range(len(self.regioes_de_resposta[u])):
                if (self.regioes_de_resposta[u][i] == valor_maximo):
                    maximos.append(self.universos["Pressao"].faixa[i])
                    contador += 1

            valor = sum(np.array(maximos)) / contador
            conjunto.append(valor)
            print(
                "A média dos máximos do \033[1;35m%s: %f\033[0;0m"
                %
                (u, valor)
            )

        self.defuzzificacao_por_caso["media dos maximos"] = conjunto

    def primeiro_maximo(self):
        conjunto = []

        for u in self.regioes_de_resposta:
            valor_maximo = max(self.regioes_de_resposta[u])

            for i in range(len(self.regioes_de_resposta[u])):
                if (self.regioes_de_resposta[u][i] == valor_maximo):
                    valor = self.universos["Pressao"].faixa[i]
                    conjunto.append(valor)
                    print(
                        "O primeiro máximo do \033[1;35m%s: %f\033[0;0m"
                        %
                         (u, valor)
                    )
                    break

        self.defuzzificacao_por_caso["primeiro maximo"] = conjunto

    def apresenta_resioes_de_resposta(self):
        quantidade = np.ceil(len(self.regioes_de_resposta) / 2).astype(int)
        interacoes = np.floor(len(self.regioes_de_resposta) / 2).astype(int)
        contador = 0

        plt.figure(figsize=(15, quantidade * 3))

        for i in range(int(interacoes)):
            subprot = int(str(quantidade) + '2' + str(contador + 1))
            plt.subplot(subprot)
            self.universos["Pressao"].imprimir_regiao()
            plt.plot(
                self.universos["Pressao"].faixa,
                self.regioes_de_resposta[
                    str("caso " + str(contador + 1))],
                label=("Região de resposta " + str(contador + 1)),
                color="m")
            plt.fill_between(self.universos["Pressao"].faixa,
                             self.regioes_de_resposta[
                                 str("caso " + str(contador + 1))],
                             alpha=0.5,
                             color="m",
                             where=(
                                 self.
                                 regioes_de_resposta[
                                     str("caso " + str(contador + 1))
                                 ] > 0)
                             )
            plt.legend()
            contador += 1
            subprot = int(str(quantidade) + '2' + str(contador + 1))
            plt.subplot(subprot)
            self.universos["Pressao"].imprimir_regiao()
            plt.plot(
                self.universos["Pressao"].faixa,
                self.regioes_de_resposta[str("caso " + str(contador + 1))],
                label=("Região de resposta " + str(contador + 1)),
                color="m")
            plt.fill_between(self.universos["Pressao"].faixa,
                             self.regioes_de_resposta[
                                 str("caso " + str(contador + 1))],
                             alpha=0.5,
                             color="m",
                             where=(
                                 self.
                                 regioes_de_resposta[
                                     str("caso " + str(contador + 1))
                                 ] > 0)
                             )
            plt.legend()
            contador += 1

        if (quantidade > interacoes):
            subprot = int(str(quantidade) + '2' + str(contador + 1))
            plt.subplot(subprot)
            self.universos["Pressao"].imprimir_regiao()
            plt.plot(
                self.universos["Pressao"].faixa,
                self.regioes_de_resposta[str("caso " + str(contador + 1))],
                label=("Região de resposta " + str(contador + 1)),
                color="m")
            plt.fill_between(self.universos["Pressao"].faixa,
                             self.regioes_de_resposta[
                                 str("caso " + str(contador + 1))],
                             alpha=0.5,
                             color="m",
                             where=(
                                 self.
                                 regioes_de_resposta[
                                     str("caso " + str(contador + 1))
                                 ] > 0)
                             )
            plt.legend()

        plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95,
                            hspace=0.25, wspace=0.35)
        plt.show()

    def gera_regioes_de_resposta(self):
        contador = 0

        for i in self.conjunto_interseccoes:
            for j in range(0, len(self.conjunto_interseccoes[i]), 2):

                self.conjunto_interseccoes[i][j] = self.inferencia(
                    self.universos["Temperatura"]
                    .singleton[contador],
                    self.universos["Temperatura"]
                    .variaveis[self.conjunto_interseccoes[i][j][0]]
                    .pertinencia,
                    self.universos["Pressao"]
                    .variaveis[self.conjunto_interseccoes[i][j][1]]
                    .pertinencia
                ).copy()

                self.conjunto_interseccoes[i][j + 1] = self.inferencia(
                    self.universos["Volume"]
                    .singleton[contador],
                    self.universos["Volume"]
                    .variaveis[self.conjunto_interseccoes[i][j + 1][0]]
                    .pertinencia,
                    self.universos["Pressao"]
                    .variaveis[self.conjunto_interseccoes[i][j + 1][1]]
                    .pertinencia
                ).copy()

            self.regioes_de_resposta[i] = self.agregacao(
                self.conjunto_interseccoes[i]).copy()
            contador += 1

    def apresenta_regras_por_caso(self):

        for caso in self.conjunto_regras_por_caso:
            print(
                "\nNo \033[1;35m%s\033[0;0m se encontra as seguintes regras:\n"
                % (caso))

            for regra in self.conjunto_regras_por_caso[caso]:
                print("\033[1;35m- %s\033[0;0m" % (regra))

    def mandani(self, A, B):

        matriz = np.zeros((len(A), len(B)))

        for i in range(len(A)):
            for j in range(len(B)):
                matriz[i][j] = min(A[i], B[j])

        return matriz

    def inferencia(self, A_linha, A, B):
        B_linha = np.zeros(len(B))
        matriz = self.mandani(A, B)
        matriz.reshape(len(B), len(A))
        tmp = np.zeros(len(A_linha))

        for i in range(len(B_linha)):
            for j in range(len(A_linha)):
                tmp[j] = min(A_linha[j], matriz[j][i])

            B_linha[i] = max(tmp)

        return B_linha

    def agregacao(self, Lista):

        somatoria = np.zeros(len(Lista[0]))

        for j in range(len(Lista[0])):
            unitario = []

            for k in range(len(Lista)):
                unitario.append(Lista[k][j])

            somatoria[j] = max(unitario)

        return somatoria

    def verifica_regras(self):
        conjuntos = []
        regras = []

        for caso in self.universos["Temperatura"].interseccoes:
            for i in range(len(self.universos["Temperatura"]
                               .interseccoes[caso])):
                for j in range(len(self.universos["Volume"]
                                   .interseccoes[caso])):
                    if (
                            self.universos["Temperatura"]
                                .interseccoes[caso][i] == "baixa" and
                            self.universos["Volume"]
                                .interseccoes[caso][j] == "pequeno"):
                        conjuntos.append(
                            {
                                caso: [["baixa",  "baixa"],
                                       ["pequeno", "baixa"]]
                            })
                        regras.append({caso: "Regra 1"})

                    if (
                            self.universos["Temperatura"]
                                .interseccoes[caso][i] == "media" and
                            self.universos["Volume"]
                                .interseccoes[caso][j] == "pequeno"):
                        conjuntos.append(
                            {
                                caso: [["media",  "baixa"],
                                       ["pequeno", "baixa"]]
                            })
                        regras.append({caso: "Regra 2"})

                    if (
                            self.universos["Temperatura"]
                                .interseccoes[caso][i] == "alta" and
                            self.universos["Volume"]
                                .interseccoes[caso][j] == "pequeno"):
                        conjuntos.append(
                            {caso: [["alta",  "media"], ["pequeno", "media"]]})
                        regras.append({caso: "Regra 3"})

                    if (
                            self.universos["Temperatura"]
                                .interseccoes[caso][i] == "baixa" and
                            self.universos["Volume"]
                                .interseccoes[caso][j] == "medio"):
                        conjuntos.append(
                            {caso: [["baixa",  "baixa"], ["medio", "baixa"]]})
                        regras.append({caso: "Regra 4"})

                    if (
                            self.universos["Temperatura"]
                                .interseccoes[caso][i] == "media" and
                            self.universos["Volume"]
                                .interseccoes[caso][j] == "medio"):
                        conjuntos.append(
                            {caso: [["media",  "media"], ["medio", "media"]]})
                        regras.append({caso: "Regra 5"})

                    if (
                            self.universos["Temperatura"]
                                .interseccoes[caso][i] == "alta" and
                            self.universos["Volume"]
                                .interseccoes[caso][j] == "medio"):
                        conjuntos.append(
                            {caso: [["alta",  "alta"], ["medio", "alta"]]})
                        regras.append({caso: "Regra 6"})

                    if (
                            self.universos["Temperatura"]
                                .interseccoes[caso][i] == "baixa" and
                            self.universos["Volume"]
                                .interseccoes[caso][j] == "grande"):
                        conjuntos.append(
                            {caso: [["baixa",  "media"], ["grande", "media"]]})
                        regras.append({caso: "Regra 7"})

                    if (
                            self.universos["Temperatura"]
                                .interseccoes[caso][i] == "media" and
                            self.universos["Volume"]
                                .interseccoes[caso][j] == "grande"):
                        conjuntos.append(
                            {caso: [["media",  "alta"], ["grande", "alta"]]})
                        regras.append({caso: "Regra 8"})

                    if (
                            self.universos["Temperatura"]
                                .interseccoes[caso][i] == "alta" and
                            self.universos["Volume"]
                            .interseccoes[caso][j] == "grande"):
                        conjuntos.append(
                            {caso: [["alta",  "alta"], ["grande", "alta"]]})
                        regras.append({caso: "Regra 9"})

        for i in conjuntos:
            for j in list(i.keys()):
                if (not(j in self.conjunto_interseccoes)):
                    self.conjunto_interseccoes[j] = []
            for k in self.conjunto_interseccoes:
                if (k in i):
                    self.conjunto_interseccoes[k].append((i[k][0]))
                    self.conjunto_interseccoes[k].append((i[k][1]))

        for i in regras:
            for j in list(i.keys()):
                if (not(j in self.conjunto_regras_por_caso)):
                    self.conjunto_regras_por_caso[j] = []
            for k in self.conjunto_regras_por_caso:
                if (k in i):
                    self.conjunto_regras_por_caso[k].append((i[k]))
