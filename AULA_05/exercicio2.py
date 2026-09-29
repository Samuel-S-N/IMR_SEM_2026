"""Exercício 2: nó sensor — processador e filtro do tópico /scan."""

import numpy as np


ALCANCE_MINIMO = 0.1
ALCANCE_MAXIMO = 5.0


def _menor_valido(leituras, indices):
    validos = [leituras[i] for i in indices if ALCANCE_MINIMO <= leituras[i] <= ALCANCE_MAXIMO]
    return min(validos) if validos else ALCANCE_MAXIMO


def processar_scan(leituras_lidar):
    leituras = np.asarray(leituras_lidar, dtype=float)
    frente_idx = list(range(345, 360)) + list(range(0, 16))
    esquerda_idx = range(45, 136)
    direita_idx = range(225, 316)

    return {
        "frente": _menor_valido(leituras, frente_idx),
        "esquerda": _menor_valido(leituras, esquerda_idx),
        "direita": _menor_valido(leituras, direita_idx),
    }


if __name__ == "__main__":
    np.random.seed(0)
    leituras = np.random.uniform(0.2, 4.0, size=360)
    leituras[0] = 0.0  # ruído: leitura nula (descartar)
    leituras[10] = 8.0  # ruído: fora de alcance (descartar)
    leituras[90] = 0.35  # obstáculo real à esquerda

    print(processar_scan(leituras))
