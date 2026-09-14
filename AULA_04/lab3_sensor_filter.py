"""Lab 3: varredura de sete feixes com ruído e filtro de alcance."""

import math

import numpy as np
import pygame


LARGURA, ALTURA = 900, 600
FPS = 60
ALCANCE = 200.0
ANGULOS = np.linspace(-math.pi / 2, math.pi / 2, 7)


def filter_distance(distance, minimum=10.0, maximum=ALCANCE):
    if distance < minimum:
        return None
    return min(distance, maximum)


def noisy_distance(real_distance, rng=np.random):
    return real_distance + float(rng.normal(0.0, 5.0))


def ray_distance(x, y, theta, beta, obstacles):
    angle = theta + beta
    for step in range(2, int(ALCANCE) + 1, 2):
        rx = x + step * math.cos(angle)
        ry = y + step * math.sin(angle)
        if rx <= 0 or rx >= LARGURA or ry <= 0 or ry >= ALTURA or any(ob.collidepoint(rx, ry) for ob in obstacles):
            return float(step)
    return ALCANCE


def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Aula 04 - Filtro de Distância")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 14)
    robot = (180.0, 300.0, 0.0)
    obstacles = [pygame.Rect(390, 130, 90, 340), pygame.Rect(650, 80, 150, 100), pygame.Rect(650, 420, 150, 100)]
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        x, y, theta = robot
        readings = []
        for beta in ANGULOS:
            real = ray_distance(x, y, theta, beta, obstacles)
            raw = noisy_distance(real)
            readings.append((beta, raw, filter_distance(raw)))

        screen.fill((30, 30, 30))
        for obstacle in obstacles:
            pygame.draw.rect(screen, (180, 50, 50), obstacle)
        for row, (beta, raw, treated) in enumerate(readings):
            angle = theta + beta
            raw_x, raw_y = x + raw * math.cos(angle), y + raw * math.sin(angle)
            treated_distance = 0.0 if treated is None else treated
            treated_x = x + treated_distance * math.cos(angle)
            treated_y = y + treated_distance * math.sin(angle)
            pygame.draw.line(screen, (255, 150, 40), (int(x), int(y)), (int(raw_x), int(raw_y)), 1)
            color = (220, 60, 60) if treated is None else (80, 220, 120)
            pygame.draw.line(screen, color, (int(x), int(y)), (int(treated_x), int(treated_y)), 3)
            treated_text = "descartada" if treated is None else f"{treated:.1f} px"
            screen.blit(font.render(f"Feixe {row + 1}: bruta={raw:6.1f} px | tratada={treated_text}", True, (230, 230, 230)), (15, 15 + row * 22))

        pygame.draw.circle(screen, (0, 180, 255), (int(x), int(y)), 15)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
