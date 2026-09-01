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
COR_OBSTACULO = (180, 50, 50)
COR_RAIO_LIVRE = (0, 255, 100)
COR_RAIO_COLISAO = (255, 200, 0)

class BraitenbergRobot:
    def __init__(self, x, y, theta=0.0, wheelbase=30.0, radius=15.0):
        # Cinemática Diferencial
        self.x = float(x)
        self.y = float(y)
        self.theta = float(theta)
        self.L = float(wheelbase)
        self.radius = float(radius)
        self.v = 0.0
        self.omega = 0.0
        
        # Sensores (Esq, Frente, Dir)
        self.sensor_angles = [-math.pi/4, 0.0, math.pi/4]
        self.sensor_range = 200.0
        self.sensor_readings = [self.sensor_range] * 3
        
        self.history = []

    def cast_rays(self, obstacles):
        """Verifica a interseção dos raios com obstáculos retangulares."""
        self.sensor_readings = []
        for beta in self.sensor_angles:
            angle = self.theta + beta
            min_dist = self.sensor_range
            
            # Amostragem linear
            for step in range(5, int(self.sensor_range), 4):
                rx = self.x + step * math.cos(angle)
                ry = self.y + step * math.sin(angle)
                
                # Borda da tela
                if rx <= 0 or rx >= LARGURA_TELA or ry <= 0 or ry >= ALTURA_TELA:
                    min_dist = float(step)
                    break
                    
                # Obstáculos
                hit = False
                for obs in obstacles:
                    if obs.collidepoint(rx, ry):
                        min_dist = float(step)
                        hit = True
                        break
                if hit:
                    break
            self.sensor_readings.append(min_dist)

    def set_wheel_velocities(self, v_left, v_right):
        self.v = (v_right + v_left) / 2.0
        self.omega = (v_right - v_left) / self.L

    def update(self, dt):
        """Integração numérica da cinemática diferencial."""
        self.theta += self.omega * dt
        self.theta = (self.theta + math.pi) % (2 * math.pi) - math.pi
        self.x += self.v * math.cos(self.theta) * dt
        self.y += self.v * math.sin(self.theta) * dt
        
        # Guarda histórico
        if len(self.history) == 0 or np.hypot(self.x - self.history[-1][0], self.y - self.history[-1][1]) > 5:
            self.history.append((self.x, self.y))
            if len(self.history) > 300:
                self.history.pop(0)

    def draw(self, surface):
        # Rastro
        if len(self.history) > 1:
            pygame.draw.lines(surface, COR_TRAJETORIA, False, self.history, 2)
            
        # Feixes sensores
        for i, beta in enumerate(self.sensor_angles):
            angle = self.theta + beta
            dist = self.sensor_readings[i]
            rx = self.x + dist * math.cos(angle)
            ry = self.y + dist * math.sin(angle)
            cor = COR_RAIO_COLISAO if dist < self.sensor_range else COR_RAIO_LIVRE
            pygame.draw.line(surface, cor, (int(self.x), int(self.y)), (int(rx), int(ry)), 1)
            pygame.draw.circle(surface, cor, (int(rx), int(ry)), 3)

        # Corpo do robô
        pos_int = (int(self.x), int(self.y))
        pygame.draw.circle(surface, COR_ROBO, pos_int, int(self.radius))
        
        linha_frente_x = self.x + (self.radius + 10) * math.cos(self.theta)
        linha_frente_y = self.y + (self.radius + 10) * math.sin(self.theta)
        pygame.draw.line(surface, COR_DIRECAO, pos_int, (int(linha_frente_x), int(linha_frente_y)), 3)

def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Lab 04: Veículo de Braitenberg (Medo Puro)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 14)

    robot = BraitenbergRobot(x=LARGURA_TELA // 2, y=ALTURA_TELA // 2, theta=0.0)

    # Criar uma "sala" com obstáculos
    obstacles = [
        pygame.Rect(100, 100, 100, 100),
        pygame.Rect(400, 200, 50, 250),
        pygame.Rect(600, 50, 100, 100),
        pygame.Rect(150, 400, 150, 50),
        pygame.Rect(600, 450, 150, 100)
    ]

    running = True
    
    # Constantes do controlador
    v_base = 100.0 # px/s
    K_s = 1.0 # Ganho
    S_max = robot.sensor_range

    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        robot.cast_rays(obstacles)
        s_esq = robot.sensor_readings[0]
        s_frente = robot.sensor_readings[1]
        s_dir = robot.sensor_readings[2]
        
        # Lógica de Controle Braitenberg (Medo / Repulsão cruzada)
        if s_frente < 40:
            # Giro imediato no próprio eixo para evitar colisão frontal
            v_L = -100.0
            v_R = 100.0
        else:
            # Roda esquerda acelera com obstáculo na direita
            v_L = v_base + K_s * (S_max - s_dir)
            # Roda direita acelera com obstáculo na esquerda
            v_R = v_base + K_s * (S_max - s_esq)
            
        robot.set_wheel_velocities(v_L, v_R)
        robot.update(dt)

        # Renderização
        screen.fill(COR_FUNDO)
        
        for obs in obstacles:
            pygame.draw.rect(screen, COR_OBSTACULO, obs)
            pygame.draw.rect(screen, (255, 100, 100), obs, 2)
            
        robot.draw(screen)

        # Painel de Telemetria
        info_txt = [
            f"Sensores (E/F/D): {s_esq:.1f} | {s_frente:.1f} | {s_dir:.1f}",
            f"Motores (L/R): {v_L:.1f} | {v_R:.1f}",
            f"V linear: {robot.v:.1f} px/s | Omega: {robot.omega:.2f} rad/s"
        ]
        
        for i, txt in enumerate(info_txt):
            rendered = font.render(txt, True, (220, 220, 220))
            screen.blit(rendered, (15, 15 + i * 20))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
