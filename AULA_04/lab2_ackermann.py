"""Lab 2: trajetória Ackermann e comparação com o robô diferencial."""

import math

import pygame


LARGURA, ALTURA = 900, 600
FPS = 60
L = 2.0
ESCALA = 70.0


def ackermann_command(velocity, steering, wheelbase=L):
    steering = max(-math.radians(30), min(math.radians(30), steering))
    omega = velocity * math.tan(steering) / wheelbase
    radius = math.inf if abs(steering) < 1e-12 else wheelbase / math.tan(steering)
    return omega, radius


class AckermannRobot:
    def __init__(self):
        self.x, self.y, self.theta = 0.0, 0.0, 0.0
        self.history = []

    def update(self, velocity, steering, dt):
        omega, _ = ackermann_command(velocity, steering)
        self.theta += omega * dt
        self.x += velocity * math.cos(self.theta) * dt
        self.y += velocity * math.sin(self.theta) * dt
        self.history.append((self.x, self.y))

    def draw(self, screen):
        points = [(int(450 + x * ESCALA), int(300 - y * ESCALA)) for x, y in self.history]
        if len(points) > 1:
            pygame.draw.lines(screen, (100, 220, 120), False, points, 2)
        px, py = 450 + self.x * ESCALA, 300 - self.y * ESCALA
        pygame.draw.circle(screen, (0, 180, 255), (int(px), int(py)), 15)
        pygame.draw.line(
            screen,
            (255, 60, 60),
            (int(px), int(py)),
            (int(px + 25 * math.cos(self.theta)), int(py - 25 * math.sin(self.theta))),
            3,
        )


def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Aula 04 - Ackermann x Diferencial")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 16)
    robot = AckermannRobot()
    velocity = 1.0
    steering = 0.0
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                robot = AckermannRobot()

        keys = pygame.key.get_pressed()
        velocity = max(0.0, min(2.0, velocity + (keys[pygame.K_w] - keys[pygame.K_s]) * dt))
        steering += (keys[pygame.K_d] - keys[pygame.K_a]) * math.radians(45) * dt
        steering = max(-math.radians(30), min(math.radians(30), steering))
        omega, radius = ackermann_command(velocity, steering)
        robot.update(velocity, steering, dt)

        screen.fill((30, 30, 30))
        robot.draw(screen)
        raio = "infinito" if math.isinf(radius) else f"{abs(radius):.2f} m"
        lines = (
            f"v={velocity:.2f} m/s | phi={math.degrees(steering):.1f} graus | omega={omega:.3f} rad/s",
            f"Raio Ackermann: {raio} | Diferencial: raio zero e possível",
            "W/S: velocidade | A/D: esterço | R: reiniciar | ESC: fechar",
        )
        for row, text in enumerate(lines):
            screen.blit(font.render(text, True, (220, 220, 220)), (15, 15 + row * 22))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
