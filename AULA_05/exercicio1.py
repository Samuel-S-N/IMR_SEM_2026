"""Exercício 1: nó atuador — conversor de /cmd_vel com saturação dos motores."""


def converter_cmd_vel(v, omega, L=0.3, max_wheel_speed=1.5):
    v_e = v - omega * L / 2.0
    v_d = v + omega * L / 2.0

    maior = max(abs(v_e), abs(v_d))
    if maior > max_wheel_speed:
        escala = max_wheel_speed / maior
        v_e *= escala
        v_d *= escala

    return v_e, v_d


if __name__ == "__main__":
    print(converter_cmd_vel(1.2, 3.0))  # Deve limitar sem travar o motor
    print(converter_cmd_vel(0.8, 0.5))  # Dentro do limite, não deve alterar a proporção
    print(converter_cmd_vel(-1.0, -4.0))  # Saturação também no sentido negativo
