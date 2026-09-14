"""Exercício 5: centralização proporcional em um corredor."""

import math

import pygame


LARGURA, ALTURA = 900, 600
FPS = 60
VELOCIDADE = 40.0
KP = 0.01


def corridor_command(d_left, d_right, kp=KP, velocity=VELOCIDADE):
    return velocity, kp * (d_left - d_right)


class CorridorRobot:
    def __init__(self):
        self.x, self.y, self.theta = 120.0, 220.0, 0.12
        self.sensor_angles = (-math.pi / 2, math.pi / 2)
        self.sensor_range = 400.0
        self.readings = [self.sensor_range, self.sensor_range]
        self.history = []

    def side_distances(self, walls):
        self.readings = []
        for beta in self.sensor_angles:
            angle = self.theta + beta
            distance = self.sensor_range
            for step in range(2, int(self.sensor_range) + 1, 2):
                rx, ry = self.x + step * math.cos(angle), self.y + step * math.sin(angle)
                if any(wall.collidepoint(rx, ry) for wall in walls):
                    distance = float(step)
                    break
            self.readings.append(distance)

    def update(self, velocity, omega, dt):
        self.theta += omega * dt
        self.x += velocity * math.cos(self.theta) * dt
        self.y += velocity * math.sin(self.theta) * dt
        self.history.append((self.x, self.y))

    def draw(self, screen):
        if len(self.history) > 1:
            pygame.draw.lines(screen, (100, 220, 120), False, [(int(x), int(y)) for x, y in self.history], 2)
        pygame.draw.circle(screen, (0, 180, 255), (int(self.x), int(self.y)), 15)
        pygame.draw.line(screen, (255, 60, 60), (int(self.x), int(self.y)), (int(self.x + 25 * math.cos(self.theta)), int(self.y + 25 * math.sin(self.theta))), 3)


def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Aula 04 - Centralização no Corredor")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 15)
    walls = (pygame.Rect(0, 100, LARGURA, 20), pygame.Rect(0, 480, LARGURA, 20))
    robot = CorridorRobot()
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        robot.side_distances(walls)
        # No eixo Y invertido do Pygame, o feixe +90° aponta para a parede de baixo.
        d_left, d_right = robot.readings[1], robot.readings[0]
        velocity, omega = corridor_command(d_left, d_right)
        robot.update(velocity, omega, dt)

        screen.fill((30, 30, 30))
        for wall in walls:
            pygame.draw.rect(screen, (180, 50, 50), wall)
        robot.draw(screen)
        lines = (f"d_esq={d_left:.1f} px | d_dir={d_right:.1f} px", f"erro={d_left - d_right:.1f} | omega={omega:.3f} rad/s", "v=40 px/s | ESC: fechar")
        for row, text in enumerate(lines):
            screen.blit(font.render(text, True, (220, 220, 220)), (15, 15 + row * 22))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
