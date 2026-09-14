"""Lab 1: pose em malha aberta para um robô diferencial."""

import math

import pygame


LARGURA, ALTURA = 900, 600
FPS = 60
ESCALA = 100.0  # 100 pixels por metro
ORIGEM_TELA = (120, 300)
COMANDOS = ((4.0, 0.5, 0.0), (2.0, 0.0, 0.7854), (3.0, 0.4, 0.0))


def normalize_angle(angle):
    return (angle + math.pi) % (2 * math.pi) - math.pi


def integrate_pose(pose, velocity, omega, dt):
    x, y, theta = pose
    theta = normalize_angle(theta + omega * dt)
    return (
        x + velocity * math.cos(theta) * dt,
        y + velocity * math.sin(theta) * dt,
        theta,
    )


def simulate_pose(commands, dt=1 / FPS):
    pose = (0.0, 0.0, 0.0)
    for duration, velocity, omega in commands:
        elapsed = 0.0
        while elapsed < duration:
            step = min(dt, duration - elapsed)
            pose = integrate_pose(pose, velocity, omega, step)
            elapsed += step
    return pose


def theoretical_pose(commands):
    x, y, theta = 0.0, 0.0, 0.0
    for duration, velocity, omega in commands:
        if abs(omega) < 1e-12:
            x += velocity * math.cos(theta) * duration
            y += velocity * math.sin(theta) * duration
        else:
            radius = velocity / omega
            next_theta = theta + omega * duration
            x += radius * (math.sin(next_theta) - math.sin(theta))
            y += radius * (math.cos(theta) - math.cos(next_theta))
            theta = next_theta
    return x, y, normalize_angle(theta)


class PoseRobot:
    def __init__(self):
        self.pose = (0.0, 0.0, 0.0)
        self.history = []

    def update(self, velocity, omega, dt):
        self.pose = integrate_pose(self.pose, velocity, omega, dt)
        x, y, _ = self.pose
        self.history.append((ORIGEM_TELA[0] + x * ESCALA, ORIGEM_TELA[1] - y * ESCALA))

    def draw(self, screen):
        if len(self.history) > 1:
            pygame.draw.lines(screen, (100, 220, 120), False, self.history, 2)
        x, y, theta = self.pose
        px = ORIGEM_TELA[0] + x * ESCALA
        py = ORIGEM_TELA[1] - y * ESCALA
        pygame.draw.circle(screen, (0, 180, 255), (int(px), int(py)), 15)
        pygame.draw.line(
            screen,
            (255, 60, 60),
            (int(px), int(py)),
            (int(px + 25 * math.cos(theta)), int(py - 25 * math.sin(theta))),
            3,
        )


def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Aula 04 - Validador de Pose")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 16)
    robot = PoseRobot()
    theoretical = theoretical_pose(COMANDOS)
    phase = 0
    elapsed = 0.0
    printed = False
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        if phase < len(COMANDOS):
            duration, velocity, omega = COMANDOS[phase]
            step = min(dt, duration - elapsed)
            robot.update(velocity, omega, step)
            elapsed += step
            if elapsed >= duration:
                phase += 1
                elapsed = 0.0
        elif not printed:
            print(f"Pose final teórica: x={theoretical[0]:.4f} m, y={theoretical[1]:.4f} m, theta={theoretical[2]:.4f} rad")
            print(f"Pose simulada:      x={robot.pose[0]:.4f} m, y={robot.pose[1]:.4f} m, theta={robot.pose[2]:.4f} rad")
            printed = True

        screen.fill((30, 30, 30))
        robot.draw(screen)
        x, y, theta = robot.pose
        lines = (
            f"Trecho: {min(phase + 1, len(COMANDOS))}/3",
            f"Pose: ({x:.2f} m, {y:.2f} m, {theta:.2f} rad)",
            "ESC: fechar",
        )
        for row, text in enumerate(lines):
            screen.blit(font.render(text, True, (220, 220, 220)), (15, 15 + row * 22))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
