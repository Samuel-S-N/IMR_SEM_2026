"""Exercício 3: lógica reativa de obstáculos (Braitenberg com trava de segurança)."""

import numpy as np

from exercicio2 import processar_scan


DISTANCIA_CRITICA = 0.4
V_AVANCO = 0.5
KP_LATERAL = 1.0


def controle_reativo(distancias):
    frente = distancias["frente"]
    esquerda = distancias["esquerda"]
    direita = distancias["direita"]

    if frente < DISTANCIA_CRITICA:
        omega = 1.0 if esquerda > direita else -1.0
        return 0.0, omega

    omega = KP_LATERAL * (esquerda - direita)
    return V_AVANCO, omega


if __name__ == "__main__":
    print(controle_reativo({"frente": 0.2, "esquerda": 1.5, "direita": 0.6}))  # freia e gira p/ esquerda (mais livre)
    print(controle_reativo({"frente": 0.2, "esquerda": 0.6, "direita": 1.5}))  # freia e gira p/ direita (mais livre)
    print(controle_reativo({"frente": 2.0, "esquerda": 1.0, "direita": 1.8}))  # avança corrigindo p/ direita

    np.random.seed(0)
    leituras = np.random.uniform(0.2, 4.0, size=360)
    distancias = processar_scan(leituras)
    print(distancias, "->", controle_reativo(distancias))
