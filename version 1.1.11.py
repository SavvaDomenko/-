import pygame
import matplotlib.pyplot as plt
import time 

from math import pi, sin, cos, atan2

HEIGHT = 700
WIDTH = 1300


win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pendulum Simulation")

objects_group = []

pygame.font.init()

debug_font = pygame.font.SysFont('Bauhuas 93', 30)
hint_font = pygame.font.SysFont('Bauhaus 93', 26)


# rendering the text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    win.blit(img, (x, y))


# setting the suspension point
class Origin:
    def __init__(self, x, y, color=(26, 23, 18)):
        self.x = x
        self.y = y
        self.radius = 15
        self.color = color

    def draw(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
##########################################################################################


k = 0.1  # stiffness coefficient
m = 1.0
gravity = 9.81
dt = 1e-3
gamma = 0.5  # viscosity coefficient

checkpoint = time.time()


def show_bar(screen):
    chart_image = pygame.image.load("bar_chart.png")  # load the image
    screen.blit(chart_image, (25, 120))


def draw_bar_chart(x, y):
    plt.figure(figsize=(4, 3))
    plt.plot(x, y)
    plt.title("angle(time)")
    plt.savefig("bar_chart.png")  # save the chart as an image
    plt.close()
    

# our weight
class Ball:
    
    def __init__(self, rd, angle, length, color=(224, 36, 1)):
        self.rd = rd
        self.angle = angle
        self.radius = 50
        self.color = color
        # setting the suspension point
        self.origin = Origin(WIDTH // 2, HEIGHT // 3)
        self.angle_velocity = .1
        self.angle_acceleration = 0
        self.rd_acceleration = 0
        self.len = length
        self.timer = 0
        self.rd_velocity = 0
        self.x = self.rd * sin(self.angle) + self.origin.x
        self.y = self.rd * cos(self.angle) + self.origin.y
        self.angle_history = []
        self.time_marks = []

    # processing the differential equation
    def math_update(self):
        for i in range(100):
            self.angle_acceleration = (-1 * gravity * sin(self.angle) - 2 * self.rd_velocity * self.angle_velocity) /\
                                      self.rd - gamma * self.angle_velocity
            self.rd_acceleration = \
                self.angle_velocity ** 2 * self.rd_velocity + gravity * cos(self.angle) - \
                k/m * (self.rd - self.len) - gamma * self.rd_velocity
            
            self.angle_velocity += self.angle_acceleration * dt
            self.rd_velocity += self.rd_acceleration * dt

            self.angle += self.angle_velocity * dt
            self.rd += self.rd_velocity * dt

            self.angle_history.append(self.angle)
            self.time_marks.append(time.time() - checkpoint)

            if len(self.angle_history) > 0 and len(self.angle_history) % 1000 == 0:
                draw_bar_chart(self.time_marks, self.angle_history)
            elif len(self.angle_history) % 9999 == 0:
                del self.angle_history[:2000]
                del self.time_marks[:2000]

            self.x = self.rd * sin(self.angle) + self.origin.x
            self.y = self.rd * cos(self.angle) + self.origin.y

    def draw(self):
        self.timer += 1

        self.origin.draw()

        n = 15  # the number of turns of the spring
        last_point_coord0 = (self.origin.x, self.origin.y)
        last_point_coord = (self.origin.x, self.origin.y)
        for i in range(1, n):
            point_y0 = self.origin.y + (-self.origin.y + self.y) * i / n
            point_x0 = self.origin.x + (-self.origin.x + self.x) * i / n

            delta = ((point_y0 - last_point_coord0[1]) ** 2 + (point_x0 - last_point_coord0[0]) ** 2) ** 0.5

            point_y = point_y0 + (-1) ** (i + 1) * sin(self.angle) * (60 ** 2 - delta ** 2) ** 0.5
            point_x = point_x0 + (-1) ** i * cos(self.angle) * (60 ** 2 - delta ** 2) ** 0.5

            pygame.draw.line(win, (26, 23, 18), last_point_coord, (point_x, point_y), 8)

            last_point_coord0 = (point_x0, point_y0)
            last_point_coord = (point_x, point_y)

        pygame.draw.line(win, (26, 23, 18), last_point_coord, (self.x, self.y), 8)
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        
        show_bar(win)

        draw_text(f"Current gravity: {gravity}", debug_font, (25, 25, 25), WIDTH // 2, 30)
        draw_text(f"Current acceleration: {self.angle_acceleration}", debug_font, (25, 25, 25), WIDTH // 2, 60)
        draw_text(f"Current momentum: {self.angle_velocity}", debug_font, (25, 25, 25), WIDTH // 2, 90)
        draw_text(f"Press up or down key to change length! ", hint_font, (25, 25, 25), 50, 30)
        draw_text(f"Current length: {self.len} ", hint_font, (25, 25, 25), 50, 60)
        draw_text(f"Current time: {self.timer} ", hint_font, (25, 25, 25), 50, 80)


class Pendulum(Ball):
    def __init__(self, rd, angle, length):
        Ball.__init__(self, rd, angle, length)


def main():
    global gamma
    black = (0, 0, 0)
    red = (255, 0, 0)
    slider_x = 50
    slider_y = 500
    slider_width = 200
    slider_height = 20
    slider_pos = slider_x + ((gamma - 0) * (slider_width - 10) / 1)

    slider_rect = pygame.Rect(slider_pos, slider_y, 10, slider_height)
    slider_dragging = False

    run = True
    clock = pygame.time.Clock()

    pendulum = Pendulum(450, pi/4, 294.4)

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
            
            # mouse capture
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if slider_rect.collidepoint(event.pos):
                    slider_dragging = True
            # checking whether the mouse was pressed within the ball
                if pendulum.x - pendulum.radius < event.pos[0] < pendulum.x + pendulum.radius and \
                        pendulum.y - pendulum.radius < event.pos[1] < pendulum.y + pendulum.radius:
                    dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                slider_dragging = False
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
            # if the mouse is clamped, update the position of the ball
            pos_m = pygame.mouse.get_pos()
            
            pendulum.x = pos_m[0]
            pendulum.y = pos_m[1]
            pendulum.rd = ((pendulum.x - pendulum.origin.x) ** 2 + (pendulum.y - pendulum.origin.y) ** 2) ** 0.5
            pendulum.angle = atan2((pendulum.x - pendulum.origin.x), (pendulum.y - pendulum.origin.y))
            # atan2() returns the angle based on orientation
            pendulum.rd_velocity = (dx ** 2 + dy ** 2) ** 0.5
            pendulum.angle_velocity = (dy*cos(pendulum.angle) - dx * sin(pendulum.angle)) / pendulum.rd       
                
        else:
            pendulum.math_update()
        pendulum.draw()

        # draw slider bar
        pygame.draw.rect(win, black, (slider_x, slider_y, slider_width, slider_height), 2)
        pygame.draw.rect(win, red, slider_rect)

        # display gravity value
        gamma_text = debug_font.render(f'Viscosity: {gamma:.2f}', True, black)
        win.blit(gamma_text, (50, 450))

        pygame.display.flip()
        clock.tick(30)
        pygame.display.update()


main()
