"""Exercício 5: máquina de estados finitos do robô autônomo."""

import math

from exercicio3 import controle_reativo
from exercicio4 import calcular_orientacao_alvo


DISTANCIA_DESVIO = 0.5
DISTANCIA_OBJETIVO = 0.2
V_IR_PARA_ALVO = 0.5


def maquina_de_estados(x, y, theta, x_alvo, y_alvo, dist_frente, dist_esq, dist_dir):
    dist_alvo = math.hypot(x_alvo - x, y_alvo - y)

    if dist_alvo < DISTANCIA_OBJETIVO:
        return "OBJETIVO_ALCANÇADO", 0.0, 0.0

    if dist_frente < DISTANCIA_DESVIO:
        distancias = {"frente": dist_frente, "esquerda": dist_esq, "direita": dist_dir}
        _, omega = controle_reativo(distancias)
        return "DESVIAR_OBSTACULO", 0.0, omega

    omega = calcular_orientacao_alvo(x, y, theta, x_alvo, y_alvo)
    return "IR_PARA_ALVO", V_IR_PARA_ALVO, omega


if __name__ == "__main__":
    print(maquina_de_estados(0.0, 0.0, 0.0, 5.0, 0.0, dist_frente=3.0, dist_esq=2.0, dist_dir=2.0))
    print(maquina_de_estados(0.0, 0.0, 0.0, 5.0, 0.0, dist_frente=0.3, dist_esq=1.5, dist_dir=0.6))
    print(maquina_de_estados(4.95, 0.0, 0.0, 5.0, 0.0, dist_frente=3.0, dist_esq=2.0, dist_dir=2.0))
