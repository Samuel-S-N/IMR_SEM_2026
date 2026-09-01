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
COR_ALVO = (200, 255, 50)

class ReactiveRobot:
    def __init__(self, x, y, theta=0.0, wheelbase=30.0, radius=15.0):
        # Cinemática Diferencial
        self.x = float(x)
        self.y = float(y)
        self.theta = float(theta)
        self.L = float(wheelbase)
        self.radius = float(radius)
        self.v = 0.0
        self.omega = 0.0
        
        # 5 Sensores
        angles_deg = [-60, -30, 0, 30, 60]
        self.sensor_angles = [math.radians(a) for a in angles_deg]
        self.sensor_range = 150.0
        self.sensor_readings = [self.sensor_range] * len(self.sensor_angles)
        
        self.history = []

    def cast_rays(self, obstacles):
        self.sensor_readings = []
        for beta in self.sensor_angles:
            angle = self.theta + beta
            min_dist = self.sensor_range
            
            for step in range(5, int(self.sensor_range), 4):
                rx = self.x + step * math.cos(angle)
                ry = self.y + step * math.sin(angle)
                
                if rx <= 0 or rx >= LARGURA_TELA or ry <= 0 or ry >= ALTURA_TELA:
                    min_dist = float(step)
                    break
                    
                hit = False
                for obs in obstacles:
                    if obs.collidepoint(rx, ry):
                        min_dist = float(step)
                        hit = True
                        break
                if hit:
                    break
            self.sensor_readings.append(min_dist)

    def set_direct_velocity(self, v, omega):
        self.v = v
        self.omega = omega

    def update(self, dt):
        self.theta += self.omega * dt
        self.theta = (self.theta + math.pi) % (2 * math.pi) - math.pi
        self.x += self.v * math.cos(self.theta) * dt
        self.y += self.v * math.sin(self.theta) * dt
        
        if len(self.history) == 0 or np.hypot(self.x - self.history[-1][0], self.y - self.history[-1][1]) > 5:
            self.history.append((self.x, self.y))
            if len(self.history) > 300:
                self.history.pop(0)

    def draw(self, surface):
        if len(self.history) > 1:
            pygame.draw.lines(surface, COR_TRAJETORIA, False, self.history, 2)
            
        for i, beta in enumerate(self.sensor_angles):
            angle = self.theta + beta
            dist = self.sensor_readings[i]
            rx = self.x + dist * math.cos(angle)
            ry = self.y + dist * math.sin(angle)
            cor = COR_RAIO_COLISAO if dist < self.sensor_range else COR_RAIO_LIVRE
            pygame.draw.line(surface, cor, (int(self.x), int(self.y)), (int(rx), int(ry)), 1)
            pygame.draw.circle(surface, cor, (int(rx), int(ry)), 3)

        pos_int = (int(self.x), int(self.y))
        pygame.draw.circle(surface, COR_ROBO, pos_int, int(self.radius))
        
        linha_frente_x = self.x + (self.radius + 10) * math.cos(self.theta)
        linha_frente_y = self.y + (self.radius + 10) * math.sin(self.theta)
        pygame.draw.line(surface, COR_DIRECAO, pos_int, (int(linha_frente_x), int(linha_frente_y)), 3)

def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Lab 05: Go-to-Goal com Desvio Reativo")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 14)

    robot = ReactiveRobot(x=100, y=100, theta=0.0)

    obstacles = [
        pygame.Rect(300, 150, 100, 300),
        pygame.Rect(500, 100, 200, 50),
        pygame.Rect(500, 400, 100, 150)
    ]

    target_pos = None
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                target_pos = pygame.mouse.get_pos()

        robot.cast_rays(obstacles)
        
        if target_pos is not None:
            tx, ty = target_pos
            dist_to_target = math.hypot(tx - robot.x, ty - robot.y)
            
            if dist_to_target < 15.0:
                # Chegou no alvo
                robot.set_direct_velocity(0.0, 0.0)
                modo = "No Alvo"
            else:
                # Go-to-Goal Padrão (Modo 1)
                angle_to_target = math.atan2(ty - robot.y, tx - robot.x)
                error_theta = angle_to_target - robot.theta
                error_theta = (error_theta + math.pi) % (2 * math.pi) - math.pi
                
                # Constantes proporcionais Go-to-Goal
                K_theta = 2.0
                K_v = 1.5
                
                omega_alvo = K_theta * error_theta
                v_alvo = min(K_v * dist_to_target, 120.0)
                
                # Verifica Modo 2 (Desvio de Emergência)
                repulsion_omega = 0.0
                K_obs = 1000.0
                in_emergency = False
                
                for i, s_i in enumerate(robot.sensor_readings):
                    if s_i < 60.0:
                        in_emergency = True
                        beta_i = robot.sensor_angles[i]
                        # Se obstáculo na direita (+beta_i), repele para esquerda (-omega) -> usa -sign(beta_i)
                        # O roteiro sugere omega_total = omega_alvo + K_obs/s_i * sign(beta_i), o sinal pode depender da conv. de coord.
                        # Em pygame, o Y inverte, então a matemática de desvio se reflete
                        sinal = -1.0 if beta_i > 0 else 1.0
                        if beta_i == 0.0:
                            sinal = 1.0 # força desvio pra um lado se bater de frente
                        repulsion_omega += (K_obs / max(s_i, 1.0)) * sinal
                
                if in_emergency:
                    modo = "Emergência (Desvio)"
                    omega_total = omega_alvo + repulsion_omega
                    # Reduz a velocidade linear ao desviar
                    v_alvo = 50.0 
                else:
                    modo = "Atração (Go-to-Goal)"
                    omega_total = omega_alvo
                    
                robot.set_direct_velocity(v_alvo, omega_total)
        else:
            modo = "Aguardando Alvo (Clique na tela)"
            robot.set_direct_velocity(0.0, 0.0)

        robot.update(dt)

        # Renderização
        screen.fill(COR_FUNDO)
        
        for obs in obstacles:
            pygame.draw.rect(screen, COR_OBSTACULO, obs)
            pygame.draw.rect(screen, (255, 100, 100), obs, 2)
            
        if target_pos is not None:
            pygame.draw.circle(screen, COR_ALVO, target_pos, 8)
            pygame.draw.circle(screen, COR_ALVO, target_pos, 16, 1)
            
        robot.draw(screen)

        # Painel de Telemetria
        info_txt = [
            f"Modo: {modo}",
            f"V linear: {robot.v:.1f} px/s | Omega: {robot.omega:.2f} rad/s"
        ]
        if target_pos:
            info_txt.append(f"Dist. Alvo: {dist_to_target:.1f} px | Erro Ang: {math.degrees(error_theta):.1f}°")
            
        for i, txt in enumerate(info_txt):
            rendered = font.render(txt, True, (220, 220, 220))
            screen.blit(rendered, (15, 15 + i * 20))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
