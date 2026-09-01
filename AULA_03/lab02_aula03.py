import pygame
import math
import numpy as np

# Constantes de Configuração
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60
COR_FUNDO = (30, 30, 30)
COR_ROBO = (0, 180, 255)
COR_DIRECAO = (255, 50, 50)
COR_TRAJETORIA = (100, 200, 100)

class DiffDriveRobot:
    def __init__(self, x, y, theta=0.0, wheelbase=30.0, radius=15.0):
        # Estado do robô: [x, y, theta]
        self.x = float(x)
        self.y = float(y)
        self.theta = float(theta)  # em radianos
        
        # Parâmetros físicos (em pixels)
        self.L = float(wheelbase)  # Distância entre rodas
        self.radius = float(radius)
        
        # Entradas de controle
        self.v = 0.0      # Velocidade linear (pixels/s)
        self.omega = 0.0  # Velocidade angular (rad/s)
        
        # Histórico de posições para plotar rastro
        self.history = []

    def set_direct_velocity(self, v, omega):
        """Comando direto de velocidade linear e angular."""
        self.v = v
        self.omega = omega

    def update(self, dt):
        """Integração numérica da cinemática diferencial."""
        self.theta += self.omega * dt
        # Normaliza o ângulo entre [-pi, pi]
        self.theta = (self.theta + math.pi) % (2 * math.pi) - math.pi
        
        self.x += self.v * math.cos(self.theta) * dt
        self.y += self.v * math.sin(self.theta) * dt
        
        # Guarda histórico
        if len(self.history) == 0 or np.hypot(self.x - self.history[-1][0], self.y - self.history[-1][1]) > 5:
            self.history.append((self.x, self.y))
            if len(self.history) > 500:
                self.history.pop(0)

    def draw(self, surface):
        if len(self.history) > 1:
            pygame.draw.lines(surface, COR_TRAJETORIA, False, self.history, 2)
            
        pos_int = (int(self.x), int(self.y))
        pygame.draw.circle(surface, COR_ROBO, pos_int, int(self.radius))
        
        linha_frente_x = self.x + (self.radius + 10) * math.cos(self.theta)
        linha_frente_y = self.y + (self.radius + 10) * math.sin(self.theta)
        pygame.draw.line(surface, COR_DIRECAO, pos_int, (int(linha_frente_x), int(linha_frente_y)), 3)

def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Lab 02: Rotação In-Place (Giro de 90°)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 14)

    robot = DiffDriveRobot(x=LARGURA_TELA // 2, y=ALTURA_TELA // 2, theta=0.0)

    target_angle = math.pi / 2  # 90 graus
    omega_cmd = 0.5  # rad/s
    initial_theta = robot.theta
    accumulated_angle = 0.0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Verifica se já alcançou 90 graus
        if accumulated_angle < target_angle:
            robot.set_direct_velocity(0.0, omega_cmd)
        else:
            # Garante o zeramento da velocidade
            robot.set_direct_velocity(0.0, 0.0)

        # Atualiza a física do robô
        old_theta = robot.theta
        robot.update(dt)
        
        # Calcular delta theta (cuidando com as transições de pi para -pi se fosse o caso)
        delta_theta = robot.theta - old_theta
        if delta_theta < -math.pi:
            delta_theta += 2 * math.pi
        elif delta_theta > math.pi:
            delta_theta -= 2 * math.pi
            
        if accumulated_angle < target_angle:
            accumulated_angle += abs(delta_theta)

        # Renderização
        screen.fill(COR_FUNDO)
        robot.draw(screen)

        # Painel de Telemetria
        info_txt = [
            f"Alvo: 90.0 graus | Ângulo Acumulado: {math.degrees(accumulated_angle):.1f} deg",
            f"Pose X: {robot.x:.1f} px | Y: {robot.y:.1f} px | Theta Atual: {math.degrees(robot.theta):.1f} deg",
            f"Comandos: v = {robot.v:.1f} px/s | omega = {robot.omega:.2f} rad/s"
        ]
        
        if accumulated_angle >= target_angle:
            info_txt.append("ROTAÇÃO CONCLUÍDA! (Velocidades zeradas)")
            
        for i, txt in enumerate(info_txt):
            rendered = font.render(txt, True, (220, 220, 220))
            screen.blit(rendered, (15, 15 + i * 20))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
