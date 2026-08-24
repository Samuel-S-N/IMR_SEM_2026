# Entregas da Aula 02

## Exercícios

- `exec01_aula02.py`: controla as rodas esquerda e direita separadamente.
  As teclas `W` e `S` controlam a roda esquerda; `I` e `K`, a direita.
- `exec02_aula02.py`: executa quatro ciclos de 2 segundos em linha reta a
  100 px/s e 1 segundo de giro a pi/2 rad/s.
- `exec03_aula02.py`: recebe um alvo com o clique do mouse e usa um
  controlador proporcional para orientar o robô até ficar a menos de 10 px.

## Compreensão dos tópicos

### Estado do robô e pose 2D

O estado é representado por `(x, y, theta)`: `x` e `y` são a posição no
plano e `theta` é a orientação do robô em radianos.

### Cinemática diferencial

Para um robô com duas rodas, as velocidades linear e angular são calculadas
por:

```text
v = (vR + vL) / 2
omega = (vR - vL) / L
```

Velocidades iguais fazem o robô seguir reto; velocidades opostas produzem um
giro no próprio eixo; uma roda parada produz um pivô em torno dela.

### Odometria discreta

Em cada intervalo `dt`, a pose é atualizada por integração numérica:

```text
theta <- theta + omega * dt
x     <- x + v * cos(theta) * dt
y     <- y + v * sin(theta) * dt
```

Como a integração usa passos discretos e não há realimentação da posição,
pequenos erros de tempo e arredondamento se acumulam.

### Navegação go-to-goal

Para um alvo `(x_alvo, y_alvo)`, calculamos `theta_desejado` com `atan2` e o
erro angular normalizado em `[-pi, pi]`. O comando angular é proporcional ao
erro:

```text
omega = Kp * erro_theta
```

O robô para quando a distância ao alvo fica menor que 10 pixels. Esse
controlador é simples e não corrige erros de localização causados pela
odometria; por isso o quadrado em malha aberta pode não fechar exatamente.
