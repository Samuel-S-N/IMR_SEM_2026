"""Lab 4: conexões diretas de Braitenberg (atração/agressão)."""

import math

import pygame


LARGURA, ALTURA = 900, 600
FPS = 60


def direct_wheel_velocities(d_left, d_right, base=40.0, alpha=80.0, maximum=200.0):
    left = base + alpha * (1.0 - d_left / maximum)
    right = base + alpha * (1.0 - d_right / maximum)
    return left, right


class BraitenbergRobot:
    def __init__(self, x, y, theta=0.0):
        self.x, self.y, self.theta = float(x), float(y), float(theta)
        self.wheelbase = 30.0
        self.sensor_angles = (-math.pi / 4, 0.0, math.pi / 4)
        self.sensor_range = 200.0
        self.readings = [self.sensor_range] * 3
        self.history = []

    def cast_rays(self, obstacles):
        self.readings = []
        for beta in self.sensor_angles:
            angle = self.theta + beta
            distance = self.sensor_range
            for step in range(4, int(self.sensor_range) + 1, 4):
                rx, ry = self.x + step * math.cos(angle), self.y + step * math.sin(angle)
                if rx <= 0 or rx >= LARGURA or ry <= 0 or ry >= ALTURA or any(ob.collidepoint(rx, ry) for ob in obstacles):
                    distance = float(step)
                    break
            self.readings.append(distance)

    def update(self, left, right, dt):
        velocity = (left + right) / 2.0
        omega = (right - left) / self.wheelbase
        self.theta += omega * dt
        self.x += velocity * math.cos(self.theta) * dt
        self.y += velocity * math.sin(self.theta) * dt
        self.history.append((self.x, self.y))

    def draw(self, screen):
        if len(self.history) > 1:
            pygame.draw.lines(screen, (100, 220, 120), False, [(int(x), int(y)) for x, y in self.history], 2)
        for beta, distance in zip(self.sensor_angles, self.readings):
            angle = self.theta + beta
            end = (int(self.x + distance * math.cos(angle)), int(self.y + distance * math.sin(angle)))
            pygame.draw.line(screen, (255, 200, 40), (int(self.x), int(self.y)), end, 1)
        pygame.draw.circle(screen, (0, 180, 255), (int(self.x), int(self.y)), 15)
        pygame.draw.line(screen, (255, 60, 60), (int(self.x), int(self.y)), (int(self.x + 25 * math.cos(self.theta)), int(self.y + 25 * math.sin(self.theta))), 3)


def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Aula 04 - Braitenberg Direto")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 15)
    robot = BraitenbergRobot(120, 300)
    obstacles = [pygame.Rect(350, 220, 100, 160), pygame.Rect(650, 100, 120, 100), pygame.Rect(650, 400, 120, 100)]
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        robot.cast_rays(obstacles)
        d_left, _, d_right = robot.readings
        left, right = direct_wheel_velocities(d_left, d_right)
        robot.update(left, right, dt)

        screen.fill((30, 30, 30))
        for obstacle in obstacles:
            pygame.draw.rect(screen, (180, 50, 50), obstacle)
        robot.draw(screen)
        lines = (f"Sensores E/D: {d_left:.1f} | {d_right:.1f} px", f"Rodas L/R: {left:.1f} | {right:.1f} px/s", "ESC: fechar")
        for row, text in enumerate(lines):
            screen.blit(font.render(text, True, (220, 220, 220)), (15, 15 + row * 22))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
