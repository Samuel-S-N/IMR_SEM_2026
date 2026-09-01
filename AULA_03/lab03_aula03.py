import pygame
import math
import numpy as np

LARGURA, ALTURA = 900, 650
FPS = 60
COR_FUNDO = (20, 24, 30)
COR_ROBO = (0, 200, 255)
COR_OBSTACULO = (180, 50, 50)
COR_RAIO_LIVRE = (0, 255, 100)
COR_RAIO_COLISAO = (255, 200, 0)

class RaycastDemoRobot:
    def __init__(self, x, y, theta=0.0):
        self.x = float(x)
        self.y = float(y)
        self.theta = float(theta)
        
        # 5 feixes: -60°, -30°, 0°, +30°, +60°
        angles_deg = [-60, -30, 0, 30, 60]
        self.sensor_angles = [math.radians(a) for a in angles_deg]
        
        # Alcance máximo de 200 px
        self.sensor_range = 200.0
        self.sensor_readings = [self.sensor_range] * len(self.sensor_angles)
        self.font = pygame.font.SysFont("monospace", 12)

    def cast_rays(self, obstacles):
        """Verifica a interseção dos raios com obstáculos retangulares."""
        self.sensor_readings = []
        for beta in self.sensor_angles:
            angle = self.theta + beta
            min_dist = self.sensor_range
            
            # Amostragem linear ao longo do raio (raymarch simplificado)
            for step in range(5, int(self.sensor_range), 4):
                rx = self.x + step * math.cos(angle)
                ry = self.y + step * math.sin(angle)
                
                # Checa colisão com as bordas da tela
                if rx <= 0 or rx >= LARGURA or ry <= 0 or ry >= ALTURA:
                    min_dist = float(step)
                    break
                    
                # Checa colisão com retângulos de obstáculos
                hit = False
                for obs in obstacles:
                    if obs.collidepoint(rx, ry):
                        min_dist = float(step)
                        hit = True
                        break
                if hit:
                    break
            
            # Adicionar ruído gaussiano (média 0, desvio-padrão 2.0 px)
            noise = np.random.normal(0, 2.0)
            min_dist_noisy = min_dist + noise
            
            # Garantir que a distância ruidosa fique nos limites [0, sensor_range]
            min_dist_noisy = max(0.0, min(self.sensor_range, min_dist_noisy))
            
            self.sensor_readings.append(min_dist_noisy)

    def draw(self, surface):
        # Desenha feixes sensores e seus valores
        for i, beta in enumerate(self.sensor_angles):
            angle = self.theta + beta
            dist = self.sensor_readings[i]
            
            # Distância baseada na leitura real para desenho visual sem passar do obstáculo
            # No entanto, o ruído pode fazer o raio parecer um pouco dentro ou antes.
            rx = self.x + dist * math.cos(angle)
            ry = self.y + dist * math.sin(angle)
            
            # Tolerância para mudar de cor (menor que range - alguma folga pro ruído)
            cor = COR_RAIO_COLISAO if dist < self.sensor_range - 5 else COR_RAIO_LIVRE
            pygame.draw.line(surface, cor, (int(self.x), int(self.y)), (int(rx), int(ry)), 2)
            pygame.draw.circle(surface, cor, (int(rx), int(ry)), 4)
            
            # Renderiza o valor do sensor ao lado do raio
            text_surf = self.font.render(f"{dist:.1f}", True, (255, 255, 255))
            # Posiciona o texto perto da ponta do raio
            surface.blit(text_surf, (int(rx) + 5, int(ry) + 5))
            
        # Desenha corpo
        pos = (int(self.x), int(self.y))
        pygame.draw.circle(surface, COR_ROBO, pos, 16)
        fx = self.x + 24 * math.cos(self.theta)
        fy = self.y + 24 * math.sin(self.theta)
        pygame.draw.line(surface, (255, 50, 50), pos, (int(fx), int(fy)), 3)

def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Lab 03: Percepção com Múltiplos Sensores de Feixe (com ruído)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 14)

    robot = RaycastDemoRobot(150, 300, 0.0)
    obstacles = [
        pygame.Rect(350, 150, 100, 350),
        pygame.Rect(600, 100, 150, 100),
        pygame.Rect(600, 400, 150, 150)
    ]

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Robô segue a posição do mouse para demonstrar a varredura sensorial
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - robot.x, my - robot.y
        robot.theta = math.atan2(dy, dx)
        robot.x += dx * 0.03
        robot.y += dy * 0.03

        robot.cast_rays(obstacles)

        screen.fill(COR_FUNDO)
        for obs in obstacles:
            pygame.draw.rect(screen, COR_OBSTACULO, obs)
            pygame.draw.rect(screen, (255, 100, 100), obs, 2)
        
        robot.draw(screen)

        leituras = [f"Sensor {i+1} ({int(math.degrees(robot.sensor_angles[i]))}°): {dist:5.1f} px" 
                    for i, dist in enumerate(robot.sensor_readings)]
        for i, l in enumerate(leituras):
            screen.blit(font.render(l, True, (220, 220, 220)), (20, 20 + i * 20))
        screen.blit(font.render("Mova o mouse para testar a detecção dos sensores.", True, (255, 215, 0)), (20, 140))

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
