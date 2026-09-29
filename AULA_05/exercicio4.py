"""Exercício 4: controlador proporcional para atração ao alvo."""

import math


def normalize_angle(angle):
    return (angle + math.pi) % (2 * math.pi) - math.pi


def calcular_orientacao_alvo(x, y, theta, x_alvo, y_alvo, Kp=1.5):
    theta_alvo = math.atan2(y_alvo - y, x_alvo - x)
    e_theta = normalize_angle(theta_alvo - theta)
    omega = Kp * e_theta
    return omega


if __name__ == "__main__":
    print(calcular_orientacao_alvo(0.0, 0.0, 0.0, 1.0, 1.0))  # alvo a 45°, robô alinhado ao eixo x
    print(calcular_orientacao_alvo(0.0, 0.0, math.pi, 1.0, 0.0))  # alvo atrás do robô (erro próximo de pi)
    print(calcular_orientacao_alvo(2.0, 2.0, math.pi / 2, 2.0, 2.0))  # já no alvo, direção indefinida
