import tkinter
from tkinter import *
import random
import time


def main():
    tk = Tk()
    tk.title('Pong Game')
    tk.resizable(0, 0)
    tk.wm_attributes('-topmost', 1)
    canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
    canvas.pack()
    tk.update()

    score = Score(canvas, 'green')
    paddle = Paddle(canvas, 'blue')
    ball = Ball(canvas, paddle, score, 'red')
    game_over_text = canvas.create_text(250, 200, text='GAME OVER', font=('Verdana', 50), state='hidden')
    game_over = False

    while not game_over:
        if not ball.hit_bottom and paddle.started:
            ball.draw()
            paddle.draw()
        if ball.hit_bottom:
            canvas.itemconfig(game_over_text, state='normal')
            game_over = True
        tk.update()
        time.sleep(0.01)
    time.sleep(3)


class Ball:
    def __init__(self, canvas, paddle, score, color):
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def hit_paddle(self, position):
        paddle_position = self.canvas.coords(self.paddle.id)
        if position[2] >= paddle_position[0] and position[0] <= paddle_position[2]:
            if paddle_position[1] <= position[3] <= paddle_position[3]:
                self.x += self.paddle.x
                self.score.hit()
                return True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        position = self.canvas.coords(self.id)
        if position[1] <= 0:
            self.y = 3
        if position[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(position):
            self.y = -3
        if position[0] <= 0:
            self.x = 3
        if position[2] >= self.canvas_width:
            self.x = -3


class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.started = False
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<Button-1>', self.start_game)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        position = self.canvas.coords(self.id)
        if position[0] <= 0:
            self.x = 0
        elif position[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, event):
        self.x = -2

    def turn_right(self, event):
        self.x = 2

    def start_game(self, event):
        self.started = True


class Score:
    def __init__(self, canvas, color):
        self.score = 0
        self.canvas = canvas
        self.id = canvas.create_text(450, 10, text=self.score, font=('Verdana', 20), fill=color)

    def hit(self):
        self.score += 1
        self.canvas.itemconfig(self.id, text=self.score)

if __name__ == '__main__':
    main()