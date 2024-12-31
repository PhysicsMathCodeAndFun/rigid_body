import pygame
import sys
import random
import math


def draw_arrow(screen, color, start, end, arrow_length=30, arrow_angle=30):
    if not(start[0] == end[0] and start[1] == end[1]):
        pygame.draw.line(screen, color, start, end, 3)
        angle = math.atan2(end[1] - start[1], end[0] - start[0])
        x1 = end[0] - arrow_length * math.cos(angle - math.radians(arrow_angle))
        y1 = end[1] - arrow_length * math.sin(angle - math.radians(arrow_angle))
        x2 = end[0] - arrow_length * math.cos(angle + math.radians(arrow_angle))
        y2 = end[1] - arrow_length * math.sin(angle + math.radians(arrow_angle))
        pygame.draw.line(screen, color, end, (x1, y1), 3)
        pygame.draw.line(screen, color, end, (x2, y2), 3)
        

pygame.init()
info = pygame.display.Info()
w, h = info.current_w, info.current_h
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
pygame.display.set_caption('physics, math, code & fun')

pygame.mixer.init()
beep = pygame.mixer.Sound("beep.mp3")
font = pygame.font.SysFont('Arial', 50)
clock = pygame.time.Clock()

colors = []
delta_time = 0.0
dt = 0.01
t = 0

X_k = []
X_k_0 = []
U_k = []

R = 400

X_c_0 = [w // 2, h // 2]
X_c = [w // 2, h // 2]
U_c = [0,0]
Theta_c = 0
Omega_c = 0
F = [0,0]
M = 1.0
I = 0.5 * M * R**2
T_z = 0.0


angle = 0
for n in range(0, 1000):
    x,y = random.uniform(w // 2 - R, w // 2 + R), random.uniform(h // 2 - R, h // 2 + R)
    r = math.sqrt((x-X_c_0[0])**2 + (y-X_c_0[1])**2)  
    if r <= R:         
        X_k.append([x,y])
        X_k_0.append([x,y])
        U_k.append([0,0])   
        colors.append((random.randint(0,255), random.randint(0,255), random.randint(0,255)))


def Update(screen):
    global delta_time
    global dt
    global t
    global h,w
    global X_c, U_c, Theta_c, Omega_c, F, X_k, M, I, T_z, colors
    
    
    X_c = [X_c[0] + dt * U_c[0], X_c[1] + dt * U_c[1]]
    Theta_c += dt * Omega_c
    
    U_c = [U_c[0] + dt * F[0] / M, U_c[1] + dt * F[1] / M]
    Omega_c = Omega_c + dt * T_z / I
    
    for k in range(len(X_k)):
        X_k[k][0] = X_c[0] + math.cos(Theta_c) * (X_k_0[k][0] - X_c_0[0]) - math.sin(Theta_c) * (X_k_0[k][1] - X_c_0[1])
        X_k[k][1] = X_c[1] + math.sin(Theta_c) * (X_k_0[k][0] - X_c_0[0]) + math.cos(Theta_c) * (X_k_0[k][1] - X_c_0[1])
        
        U_k[k][0] = U_c[0] - math.sin(Theta_c) * (X_k_0[k][0] - X_c_0[0]) - math.cos(Theta_c) * (X_k_0[k][1] - X_c_0[1])
        U_k[k][1] = U_c[1] + math.cos(Theta_c) * (X_k_0[k][0] - X_c_0[0]) - math.sin(Theta_c) * (X_k_0[k][1] - X_c_0[1])

        pygame.draw.circle(screen, colors[k], X_k[k], 10)
    
    
    draw_arrow(screen, (0, 0, 255), X_c, [X_c[0] + 50*F[0], X_c[1] + 50*F[1]])

    
    
    if X_c[0] + R >= w or X_c[0] - R <= 0:
        U_c[0] = -U_c[0]
        F[0] = -F[0]
        beep.play()
    if X_c[1] + R >= h or X_c[1] - R <= 0:
        U_c[1] = -U_c[1]
        F[1] = -F[1]
        beep.play()
        
    delta_time = clock.tick(60) / 1000
    pygame.display.flip()
    t += 1
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP]:
        T_z += 10.0
    if keys[pygame.K_DOWN]:
        T_z -= 10.0
        
    if keys[pygame.K_w]:
        F[1] -= 0.1
    if keys[pygame.K_s]:
        F[1] += 0.1
    if keys[pygame.K_a]:
        F[0] -= 0.1
    if keys[pygame.K_d]:
        F[0] += 0.1
    
isEnd = False
while not isEnd:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isEnd = True
            
    screen.fill((0,0,0))       
    Update(screen)
    
pygame.quit()
sys.exit()
