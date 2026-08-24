"""AC1-2: quadrado em malha aberta, controlado por tempo."""

from math import pi

import pygame

from simulador_aula02 import ALTURA_TELA, LARGURA_TELA, DiffDriveRobot


def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Aula 02 - Quadrado em malha aberta")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 14)
    robot = DiffDriveRobot(LARGURA_TELA // 2, ALTURA_TELA // 2)
    phase = "forward"
    elapsed = 0.0
    side = 0
    running = True

    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        elapsed += dt
        if side == 4:
            robot.set_direct_velocity(0.0, 0.0)
            phase = "done"
        elif phase == "forward":
            robot.set_direct_velocity(100.0, 0.0)
            if elapsed >= 2.0:
                elapsed -= 2.0
                phase = "turn"
        else:
            robot.set_direct_velocity(0.0, pi / 2.0)
            if elapsed >= 1.0:
                elapsed -= 1.0
                side += 1
                phase = "forward"

        robot.update(dt)
        screen.fill((30, 30, 30))
        robot.draw(screen)
        text = f"lado={side}/4 | fase={phase} | pose=({robot.x:.1f}, {robot.y:.1f}, {robot.theta:.2f})"
        screen.blit(font.render(text, True, (220, 220, 220)), (15, 15))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
