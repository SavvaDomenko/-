import pygame
import matplotlib.pyplot as plt 
import numpy as np
import time 

from math import pi, sin, cos, floor, atan2

height = 700
width = 1100


win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pendulum Simulation")

objects_group = []

pygame.font.init()

debug_font = pygame.font.SysFont('Bauhuas 93', 30)
hint_font = pygame.font.SysFont('Bauhaus 93', 26)


# отрисовка текста
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    win.blit(img,(x, y))

# Задаем точку подвеса
class Origin():
    def __init__(self, x, y, color=(26, 23, 18)):
        self.x = x
        self.y = y
        self.radius = 15
        self.color = color

    def draw(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
##########################################################################################


k = 0.1
m = 1.0
gravity = 9.81
dt = 1e-3

# коэффицент вязкости 

angle_history = []
time_marks = []
checkpoint = time.time()
points = 0
shown=False 

def show_bar(screen):
    chart_image = pygame.image.load("bar_chart.png")  # Load the image
    screen.blit(chart_image, (50, 50))

def draw_bar_chart(screen,x,y):
    plt.figure(figsize=(4, 3))
    plt.plot(x,y)
    plt.savefig("bar_chart.png")  # Save the chart as an image
    plt.close()
    

# наш грузик
class Ball():
    
    def __init__(self, rd, angle, length, color=(224, 36, 1)):
        self.rd = rd
        self.angle = angle
        self.radius = 50
        self.color = color
        # задаем положение нашей точки подвеса
        self.origin = Origin(width // 2, height//3)
        self.angle_velocity = .1
        self.angle_acceleration = 0
        self.rd_acceleration = 0
        self.len = length
        self.timer = 0
        self.rd_velocity = 0
        self.x = self.rd * sin(self.angle) + self.origin.x
        self.y = self.rd * cos(self.angle) + self.origin.y

    # Обработка диф уравнения
    def math_update(self):
        global points
        global shown
        global angle_history
        global time_marks
        # сто тиков, но отрисовывает один
        for i in range(100):
            self.angle_acceleration = (-1 * gravity * sin(self.angle) -  2 *  self.rd_velocity * self.angle_velocity) /  self.rd - gamma * self.angle_velocity
            self.rd_acceleration = self.angle_velocity ** 2 * self.rd_velocity + gravity * cos(self.angle) - k/m * (self.rd - self.len) - gamma * self.rd_velocity
            
            self.angle_velocity += self.angle_acceleration * dt
            self.rd_velocity += self.rd_acceleration * dt

            self.angle += self.angle_velocity * dt
            self.rd += self.rd_velocity * dt
            angle_history.append(self.angle)
            time_marks.append(time.time()-checkpoint)
            if points == 2500:
                draw_bar_chart(win,time_marks, angle_history)
            if points == 5000:
                draw_bar_chart(win,time_marks, angle_history)
            if points == 7500:
                draw_bar_chart(win,time_marks, angle_history)
            if points > 10000:
                time_marks=[]
                angle_history=[]
                points=0
            points+=1
            #if points<1 and not shown:
            #    shown=True
            #    plt.plot(time_marks, angle_history)
            #    plt.show()
            self.x = self.rd * sin(self.angle) + self.origin.x
            self.y= self.rd * cos(self.angle) + self.origin.y

    def draw(self):
        self.timer += 1

        self.origin.draw()
        pygame.draw.line(win, (26, 23, 18), (self.origin.x, self.origin.y), (self.x, self.y), 8)
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        
        show_bar(win)
        #поменять
        draw_text(f"Current gravity: {gravity}", debug_font, (25,25,25), width // 2, 30)
        draw_text(f"Current acceleration: {self.angle_acceleration}", debug_font, (25,25,25), width // 2, 60)
        draw_text(f"Current momentum: {self.angle_velocity}", debug_font, (25,25,25), width // 2, 90)
        draw_text(f"Press up or down key to change length! ", hint_font, (25,25,25), 10, 30)
        draw_text(f"Current length: {self.len} ", hint_font, (25,25,25), 10, 60)
        draw_text(f"Current time: {self.timer} ", hint_font, (25,25,25), 10, 80)

# class viscosity_Slider(self): 
#     self.slider_x = 50
#     self.slider_y = 500
#     slider_width = 200
#     slider_height = 20
#     slider_pos = slider_x + ((gravity - 1) * (slider_width - 10) / 19)  # Calculate initial slider position
#     slider_rect = pygame.Rect(slider_pos, slider_y, 10, slider_height)
#     slider_dragging = False

# slider_x = 50
# slider_y = 500
# slider_width = 200
# slider_height = 20
# slider_pos = slider_x + ((gravity - 1) * (slider_width - 10) / 19)  # Calculate initial slider position
# slider_rect = pygame.Rect(slider_pos, slider_y, 10, slider_height)
# slider_dragging = False

# pygame.draw.rect(screen, BLACK, (slider_x, slider_y, slider_width, slider_height), 2)
# pygame.draw.rect(screen, RED, slider_rect)



class Pendulum(Ball):
    def __init__(self, rd, angle, length):
        Ball.__init__(self, rd, angle, length)

gamma=0.5

def main():
    global gamma

    BLACK = (0,0,0)
    RED = (255,0,0)
    slider_x = 50
    slider_y = 500
    slider_width = 200
    slider_height = 20
    slider_pos = slider_x + ((gamma - 0) * (slider_width - 10) / 1)

    slider_rect = pygame.Rect(slider_pos, slider_y, 10, slider_height)
    slider_dragging = False


   
    run = True
    clock = pygame.time.Clock()

    # p_origin = Origin(width // 2, height // 2 - 200)
    pendulum = Pendulum(450, pi/4, 294.4)
    # objects_group.append(p_origin)
    objects_group.append(pendulum)

    dragging = False
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                run = False
                pygame.quit()
            if key[pygame.K_UP]:
                pendulum.len -= 10
            if key[pygame.K_DOWN]:
                pendulum.len += 10
            if key[pygame.K_r]:
                # reset pendulum position, physics
                pendulum.angle_velocity = .1
                pendulum.angle_acceleration = 0
                pendulum.angle = pi/4
                pendulum.timer = 0
          
            
           # Захват мыши      
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if slider_rect.collidepoint(event.pos):
                    slider_dragging = True
            # Проверка, была ли нажата мышь в пределах шарика
                if pendulum.x - pendulum.radius < event.pos[0] < pendulum.x + pendulum.radius and \
                        pendulum.y - pendulum.radius < event.pos[1] < pendulum.y + pendulum.radius:
                    dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                slider_dragging = False
                  #i want to play with velocity
            elif event.type == pygame.MOUSEMOTION:
                if slider_dragging:
                    slider_rect.x = max(slider_x, min(slider_x + slider_width - 10, event.pos[0]))
                    gamma = 0 + ((slider_rect.x - slider_x) / (slider_width - 10)) * 1
                    print(gamma)
                dx, dy = event.rel
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if slider_rect.collidepoint(event.pos):
                    slider_dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                slider_dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if slider_dragging:
                    slider_rect.x = max(slider_x, min(slider_x + slider_width - 10, event.pos[0]))
                    gamma = 0 + ((slider_rect.x - slider_x) / (slider_width - 10)) * 1
                
        win.fill((205, 206, 205))
        
        if dragging:
            # Если мышь зажата, обновляем позицию шарика
            pos_m = pygame.mouse.get_pos() # massiv
            
            pendulum.x = pos_m[0]
            pendulum.y = pos_m[1]
            pendulum.rd = ((pendulum.x - pendulum.origin.x)** 2 + (pendulum.y - pendulum.origin.y)** 2)**0.5
            pendulum.angle = atan2 ((pendulum.x - pendulum.origin.x), (pendulum.y - pendulum.origin.y)) # atan2 вернет угол с учетом ориентации
            pendulum.rd_velocity = ((dx) ** 2 + (dy) ** 2) ** 0.5
            pendulum.angle_velocity = (dy*cos(pendulum.angle) - dx * sin(pendulum.angle)) / pendulum.rd       
                
        else:
            pendulum.math_update()
        pendulum.draw()

         # Draw slider bar
        pygame.draw.rect(win, BLACK, (slider_x, slider_y, slider_width, slider_height), 2)
        pygame.draw.rect(win, RED, slider_rect)

        # Display gravity value
        gamma_text = debug_font.render(f'Viscosity: {gamma:.2f}', True, BLACK)
        win.blit(gamma_text, (50, 450))


        
        pygame.display.flip()
        clock.tick(30)
        pygame.display.update()
            
        
        
        #update(win, objects_group)

main()



# Нарисовать нормальную пружину (гармошку), а не просто линия
# Добавить вязкую среду (с ползунком контроля), это для затухания колебаний, 
# Можно добавить след маятника (чтоб стирался не сразу)
# выводить графики зависимости (например амплитуды разных маятников от времени) (частоты от времени)
