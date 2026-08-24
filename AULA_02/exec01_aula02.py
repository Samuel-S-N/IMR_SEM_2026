"""AC1-1: controle independente das rodas com o teclado."""

import pygame

from simulador_aula02 import ALTURA_TELA, LARGURA_TELA, DiffDriveRobot


def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Aula 02 - Controle por rodas")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 14)
    robot = DiffDriveRobot(LARGURA_TELA // 2, ALTURA_TELA // 2)
    running = True

    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        v_left = 100.0 * (keys[pygame.K_w] - keys[pygame.K_s])
        v_right = 100.0 * (keys[pygame.K_i] - keys[pygame.K_k])
        robot.set_wheel_velocities(v_left, v_right)
        robot.update(dt)

        screen.fill((30, 30, 30))
        robot.draw(screen)
        lines = (
            f"vL={v_left:5.1f} | vR={v_right:5.1f}",
            f"v={robot.v:5.1f} | omega={robot.omega:5.2f}",
            "W/S: roda esquerda | I/K: roda direita | ESC: fechar",
        )
        for row, text in enumerate(lines):
            screen.blit(font.render(text, True, (220, 220, 220)), (15, 15 + row * 20))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
