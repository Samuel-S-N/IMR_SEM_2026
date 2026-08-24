"""AC1-3: navegação até um ponto usando controle proporcional."""

import math

import pygame

from simulador_aula02 import ALTURA_TELA, LARGURA_TELA, DiffDriveRobot


def normalize_angle(angle):
    return (angle + math.pi) % (2 * math.pi) - math.pi


def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Aula 02 - Go-to-goal proporcional")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 14)
    robot = DiffDriveRobot(LARGURA_TELA // 2, ALTURA_TELA // 2)
    target = None
    running = True

    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                target = event.pos

        distance = 0.0
        if target is not None:
            dx = target[0] - robot.x
            dy = target[1] - robot.y
            distance = math.hypot(dx, dy)
            if distance < 10.0:
                robot.set_direct_velocity(0.0, 0.0)
            else:
                desired = math.atan2(dy, dx)
                error = normalize_angle(desired - robot.theta)
                omega = 2.5 * error
                velocity = 100.0 * max(0.0, math.cos(error))
                robot.set_direct_velocity(velocity, omega)
        else:
            robot.set_direct_velocity(0.0, 0.0)

        robot.update(dt)
        screen.fill((30, 30, 30))
        robot.draw(screen)
        if target is not None:
            pygame.draw.circle(screen, (255, 220, 0), target, 8, 2)
        text = f"alvo={target or '-'} | distancia={distance:.1f}px | clique para escolher"
        screen.blit(font.render(text, True, (220, 220, 220)), (15, 15))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
