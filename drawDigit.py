import pygame
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from tkinter import messagebox


class pixel():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (255, 255, 255)
        self.neighbours = []


    def round_pixs(self, x, y, width, height):
        round_x = round(x)
        round_y = round(y)
        round_width = round(x - round_x + width)
        round_height = round(y - round_y + height)
        return pygame.Rect(round_x, round_y, round_width, round_height)


    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.round_pixs(self.x, self.y, self.width, self.height)) 


    def get_neighbours(self, g):
        # Get the neighbours of each pixel in the grid, this is used for drawing thicker lines
        j = self.x // 20 # the var i is responsible for denoting the current col value in the grid
        i = self.y // 20 # the var j is responsible for denoting thr current row value in the grid
        rows = 28
        cols = 28

        # Horizontal and vertical neighbors
        if i < cols - 1:  # Right
            self.neighbours.append(g.pixels[i + 1][j])
        if i > 0:  # Left
            self.neighbours.append(g.pixels[i - 1][j])
        if j < rows - 1:  # Up
            self.neighbours.append(g.pixels[i][j + 1])
        if j > 0:  # Down
            self.neighbours.append(g.pixels[i][j - 1])

        # Diagonal neighbors
        if j > 0 and i > 0:  # Top Left
            self.neighbours.append(g.pixels[i - 1][j - 1])

        if j + 1 < rows and i > -1 and i - 1 > 0:  # Bottom Left
            self.neighbours.append(g.pixels[i - 1][j + 1])

        if j - 1 < rows and i < cols - 1 and j - 1 > 0:  # Top Right
            self.neighbours.append(g.pixels[i + 1][j - 1])

        if j < rows - 1 and i < cols - 1:  # Bottom Right
            self.neighbours.append(g.pixels[i + 1][j + 1])

    

class grid():
    pixels = []

    def __init__(self, row, col, width, height):
        self.rows = row
        self.cols = col
        self.width = width
        self.height = height
        self.generate_pixels()
        pass

    def draw(self, surface):
        for row in self.pixels:
            for col in row:
                col.draw(surface)
        
    
    def generate_pixels(self):
        x_gap = self.width // self.cols
        y_gap = self.height // self.rows
        self.pixels = []

        for r in range(self.rows):
            self.pixels.append([])
            for c in range(self.cols):
                self.pixels[r].append(pixel(x_gap * c, y_gap * r, x_gap, y_gap))
        
        for r in range(self.rows):
            for c in range(self.cols):
                self.pixels[r][c].get_neighbours(self)


    def clicked(self, pos):
        g1 = pos[0] // self.pixels[0][0].width
        g2 = pos[1] // self.pixels[0][0].height
        return self.pixels[g2][g1]


    def convert_pygame_drawing(self):
        digit_to_classify = self.pixels
        newMatrix = [[] for _ in range(len(digit_to_classify))]

        for i in range(len(digit_to_classify)):
            for j in range(len(digit_to_classify[i])):
                if digit_to_classify[i][j].color == (0, 0, 0):
                    newMatrix[i].append(1)
                else:
                    newMatrix[i].append(0)


        drawn_digit = np.zeros((1, 28, 28, 1))
        for row in range(28):
            for x in range(28):
                drawn_digit[0][row][x] = newMatrix[row][x]

        return drawn_digit



def guess(digit_to_classify, model):
    correct_preds = 0
    incorrect_preds = 0
    predictions = model.predict(digit_to_classify)
    t = np.argmax(predictions[0])
    window = Tk()
    window.withdraw()
    MsgBox = messagebox.askquestion("Prediction", "Is the entered digit {}?".format(t))
    if MsgBox == 'yes':
        correct_preds += 1
    else:
        incorrect_preds += 1
    window.destroy()
    return correct_preds, incorrect_preds


def main():
    model = tf.keras.models.load_model('mnist30ep.h5')
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                digit_to_classify = g.convert_pygame_drawing()
                guess(digit_to_classify, model)
                g.generate_pixels()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                clicked = g.clicked(pos)
                clicked.color = (0,0,0)
                for neighbour in clicked.neighbours:
                    neighbour.color = (0,0,0)
            if pygame.mouse.get_pressed()[2]:   # add custom erasing 
                g.generate_pixels()

        g.draw(win)
        pygame.display.update()

pygame.init()
width = height = 560
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Number Guesser")
g = grid(28, 28, width, height)

main()


pygame.quit()
quit()


