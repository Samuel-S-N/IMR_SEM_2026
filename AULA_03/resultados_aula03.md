# Relatório Final - AULA 03: Sensores de Proximidade e Braitenberg

## 1. Resultados Encontrados nos Laboratórios

### Laboratório 1: Raycasting e Interseção com Obstáculos
Neste laboratório, validamos o comportamento básico de percepção espacial do robô. Os três feixes virtuais lançados à frente do robô calculam eficientemente a distância até as paredes ou retângulos. A detecção muda de cor para amarelo ao indicar uma colisão eminente dentro do alcance de 150px.
*(Insira aqui o print do Lab 01)*


### Laboratório 2: Rotação In-Place (Giro de 90°)
O robô executou uma rotação sobre o próprio eixo com sucesso utilizando o controle de velocidade angular de 0.5 rad/s. A parada foi precisa através da medição do ângulo acumulado (1.57 rad = 90º). Quando atingiu o objetivo, as velocidades foram zeradas e o robô imobilizou-se, demonstrando a importância do controle em loop aberto baseado no tempo/estado.
*(Insira aqui o print do Lab 02)*


### Laboratório 3: Percepção com Múltiplos Sensores de Feixe
O robô foi atualizado para utilizar 5 sensores simultâneos (de -60° até +60°) com alcance de 200px. A adição de um ruído gaussiano ($\mu=0$, $\sigma=2.0$) nas medições trouxe realismo à simulação, mostrando como dados sensoriais brutos sofrem flutuações e não são perfeitos, mesmo em instantes que o robô está parado de frente à parede.
*(Insira aqui o print do Lab 03)*


### Laboratório 4: Veículo de Braitenberg (Comportamento de Medo Puro)
O algoritmo de Braitenberg cruzado provocou o comportamento reativo desejado: o robô foge ativamente de obstáculos sem nenhum planejamento global. Acelerar a roda oposta ao sensor acionado cria torques que o viram para longe do perigo de maneira suave, e a regra de "inversão imediata" no sensor central < 40px preveniu colisões frontais secas.
*(Insira aqui o print do Lab 04)*


### Laboratório 5: Navegador Reativo Go-to-Goal com Desvio
Foi possível observar a fusão de dois comportamentos: Atração (força o robô a seguir até o ponto do clique) e Repulsão (força o robô a virar para o lado livre se a distância do obstáculo for < 60px). Quando o robô encontrava o obstáculo pelo caminho, o controle de emergência sobrepunha a velocidade angular necessária para contorná-lo, retornando ao alvo principal assim que o perigo saia do alcance crítico.
*(Insira aqui o print do Lab 05)*

---

## 2. Exercício de Maior Dificuldade

O exercício mais complexo de ser compreendido foi o **Laboratório 5 (Navegador Reativo Go-to-Goal com Desvio)**. 
**Motivo:** Este exercício exigiu não apenas o entendimento isolado da atração (Go-to-Goal) ou da repulsão (Braitenberg), mas a correta orquestração/arbitragem entre esses dois modos (Subsumption-like architecture). Equacionar os ganhos proporcionais ($K_{obs}$, $K_{theta}$, e $K_v$) de forma que o robô não entrasse em loops infinitos (ex: ficar preso num canto oscilando entre ir pro alvo e desviar da parede) requer ajuste empírico e compreensão sólida de composição de vetores/velocidades virtuais.

---

## 3. Impressões Gerais sobre as Dificuldades Técnicas

Até este momento da disciplina, as principais dificuldades na compreensão dos algoritmos de Robôs Inteligentes Móveis concentram-se na transição do "mundo ideal" para o "mundo reativo contínuo":
1. **Modelagem Cinematográfica x Controle Discreto:** Converter velocidades lineares e angulares reais em posições através da integração de Euler ($x = x + v \cdot \cos(\theta) \cdot dt$) fica vulnerável ao FPS da aplicação.
2. **Ruído Sensorial:** Como visto no Lab 3, depender de medições únicas e flutuantes para controle reativo (sem o uso de filtros como o de Kalman ou Médias Móveis) pode causar vibrações indesejadas no controle dos motores.
3. **Mínimos Locais:** Na arquitetura puramente reativa apresentada (Braitenberg e Campos Potenciais Simplificados), o robô tende a falhar ou travar em buracos no formato de "U", um dos clássicos problemas de algoritmos sem mapa global da área, sendo muito interessante observar isso acontecendo na prática.
