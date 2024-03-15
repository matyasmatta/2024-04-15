import numpy as np 
import pygame
from time import time as timestamp
from statistics import mean

def generate_zero_array(length):
    return np.zeros(length)

def generate_random_array(length):
    return np.random.choice([-1, 1], size=length)

def simulate(iterations, items):
    array = generate_zero_array(items)
    for i in range(iterations):
        array += generate_random_array(items)
    return array


def graph_plot_1d(items=100):
    pygame.init()

    # set constants
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 400
    WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    # create screen window
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # define updater
    def update(array):
        array += generate_random_array(items)
        for item in array:
            pygame.draw.circle(screen, RED, (int(item)+(WINDOW_WIDTH/2),(WINDOW_HEIGHT/2)), 5)
        return array


    # running loop
    array = generate_zero_array(items)
    while True:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        array = update(array)
        pygame.display.flip()  

def graph_plot_2d(items=1000):
    pygame.init()

    # set constants
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 700
    WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0,0,255)
    GREEN = (0,255,0)
    HISTOGRAM_HEIGHT = WINDOW_WIDTH/5
    FONT_SIZE = int(round(WINDOW_WIDTH/20))
    FONT_COLOR = BLACK
    colour_list = None

    global font 
    font = pygame.font.SysFont(None, FONT_SIZE)

    # create screen window
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # define updater
    def update(array_x, array_y):
        nonlocal colour_list

        def subupdate(array):
            match BOUNDARY_MODE:
                case "bounce":
                    change_array = generate_random_array(items)
                    hypothetical_array = array + change_array
                    hypothetical_array = np.absolute(hypothetical_array)
                    after_division_array = hypothetical_array // BOUNDARY_LIMIT
                    positive_after_division_array = np.absolute(after_division_array)
                    if DYNAMIC_COLOURS:
                        for i, item in enumerate(positive_after_division_array.tolist()):
                            if item == 1:
                                colour_list[i] = GREEN if colour_list[i] != BLUE else BLUE
                    difference_array = ((positive_after_division_array*2)-1)*(-1)
                    final_array = difference_array*change_array
                    array += final_array
                    return array
                case "none":
                    array += generate_random_array(items)
                    return array
                case "stick":
                    change_array = generate_random_array(items)
                    hypothetical_array = array
                    hypothetical_array = np.absolute(hypothetical_array)
                    after_division_array = hypothetical_array // BOUNDARY_LIMIT
                    positive_after_division_array = np.absolute(after_division_array) - 1
                    positive_after_division_array -= 1
                    positive_after_division_array *= (-1)
                    if DYNAMIC_COLOURS:
                        for i, item in enumerate(positive_after_division_array.tolist()):
                            if item == 0:
                                colour_list[i] = GREEN
                    final_array = positive_after_division_array*change_array
                    array += final_array
                    return array
                case _:
                    array += generate_random_array(items)
                    return array

        
        array_x = subupdate(array_x)
        array_y = subupdate(array_y)
        array_x_list = array_x.tolist()
        array_y_list = array_y.tolist()



        for i, item in enumerate(colour_list):
            if item == GREEN:
                if array_x_list[i] == (0) and array_y_list[i] == (0):
                    colour_list[i] = BLUE

        for i, item in enumerate(array_x):
            pygame.draw.circle(screen, colour_list[i] if colour_list else RED, (int(item)+(WINDOW_WIDTH/2),array_y[i]+(WINDOW_HEIGHT/2)), 5)
        return array_x, array_y
    
    # define histogram
    def draw_histogram(array_x, bins=50):
        histogram = np.histogram(array_x, bins=bins, range=(-500, 500))[0]
        max_count = max(histogram)
        for i, count in enumerate(histogram):
            bar_height = (count / max_count) * HISTOGRAM_HEIGHT
            pygame.draw.rect(screen, BLUE, (i * (WINDOW_WIDTH // bins), WINDOW_HEIGHT - bar_height, WINDOW_WIDTH // bins, bar_height))
            pygame.draw.line(screen, BLACK, (10, WINDOW_HEIGHT-bar_height-2), (10, WINDOW_HEIGHT-2), 5)

            text = font.render(f'{max_count}', True, BLACK)
            text_rect = text.get_rect(bottomleft=(20, WINDOW_HEIGHT - 0.4*HISTOGRAM_HEIGHT))
            screen.blit(text, text_rect)



    # running loop
    array_x = generate_zero_array(items)
    array_y = generate_zero_array(items)
    if DYNAMIC_COLOURS: colour_list = [RED for _ in range(items)]
    epoch = int()
    performance_list = list()
    pass_list = list()
    while True:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if DYNAMIC_COLOURS:
            red_count, green_count, blue_count = int(), int(), int()
            for color in colour_list:
                if color == RED:
                    red_count += 1
                elif color == GREEN:
                    green_count += 1
                elif color == BLUE:
                    blue_count += 1

            sum = red_count+green_count+blue_count
            red_proportion = red_count/sum if sum != 0 else 0
            green_proportion = green_count/sum if sum != 0 else 0
            blue_proportion = blue_count/sum if sum != 0 else 0

        if DYNAMIC_COLOURS:
            pygame.draw.rect(screen, RED, (10, 10, 20, int(red_proportion * 0.1*WINDOW_HEIGHT)), 0)
            pygame.draw.rect(screen, GREEN, (40, 10, 20, int(green_proportion * 0.1*WINDOW_HEIGHT)), 0)
            pygame.draw.rect(screen, BLUE, (70, 10, 20, int(blue_proportion * 0.1*WINDOW_HEIGHT)), 0)

        array_x, array_y = update(array_x, array_y)
        draw_histogram(array_x)
        variance_x = np.var(array_x)
        variance_y = np.var(array_y)

        variance_text = font.render(f'Variance (x, y): {variance_x:.2f}, {variance_y:.2f}', True, FONT_COLOR)
        variance_rect = variance_text.get_rect(topright=(WINDOW_WIDTH - 10, 10))
        screen.blit(variance_text, variance_rect)

        epoch_text = font.render(f'Epoch (n): {epoch}', True, FONT_COLOR)
        epoch_rect = epoch_text.get_rect(topright=(WINDOW_WIDTH - 10, 50))
        screen.blit(epoch_text, epoch_rect)   

        try:
            period = pass_list[-1] - pass_list[-2]
            performance_list.append(period)
            if len(pass_list) > 3:
                pass_list[1:]

            def get_performance(performance_list):
                mean_performance = mean(performance_list)
                return 1/mean_performance

            performance_text = font.render(f'Performance (epoch/s): {round(get_performance(performance_list),2):.2f}', True, FONT_COLOR)
            performance_rect = performance_text.get_rect(topright=(WINDOW_WIDTH - 10, 90))
            screen.blit(performance_text, performance_rect)   
        except:
            pass

        epoch += 1
        pass_list.append(timestamp())
        pygame.display.flip()  

if __name__ == "__main__":
    global BOUNDARY_MODE, BOUNDARY_LIMIT, DYNAMIC_COLOURS
    BOUNDARY_MODE = "bounce"
    BOUNDARY_LIMIT = 150
    DYNAMIC_COLOURS = True # may impact performance
    SHOW_RETURNED = True
    graph_plot_2d()