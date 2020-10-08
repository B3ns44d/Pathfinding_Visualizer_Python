from tkinter import *
from random import randrange
import time

#
width, height = 400, 400
w = 40
rows, cols = int(height/w), int(width/w)
grid = [[[] for c in range(cols)] for r in range(rows)]  #using list comprehensions to declare 2d array
current = 0
stack = []

solve = []
backtrack = []
#

window = Tk()
window.title('Maze Game!')
canvas = Canvas(window, width=width, height=height, bg='white')
canvas.pack()


class Cell:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.walls = [True, True, True, True]  #[top, right, bottom, left]
        self.visited = False
        self.tl = self.rl = self.bl = self.ll = 0

        self.choose = False

        self.rect = 0

    def show(self):
        x = self.i * w
        y = self.j * w
        #if self.walls[0]:
        self.tl = canvas.create_line(x,    y,    x+w,  y, fill='blue', width=2)     #draw top line
        #if self.walls[1]:
        self.rl = canvas.create_line(x+w, y,    x+w , y+w, fill='blue', width=2)  #draw right line
        #if self.walls[2]:
        self.bl = canvas.create_line(x+w, y+w, x,     y+w, fill='blue', width=2)  #draw bottom line
        #if self.walls[3]:
        self.ll = canvas.create_line(x,    y+w, x,     y, fill='blue', width=2)     #draw left line

    def draw_visited(self):
        x = self.i * w
        y = self.j * w
        if self.visited:
            self.rect = canvas.create_rectangle(x+9, y+9, x+w-9, y+w-9, fill='white', outline='')
            window.update()
            #time.sleep(0.05)

    def highlight(self):
        x = self.i * w
        y = self.j * w
        canvas.create_rectangle(x+9, y+9, x+w-9, y+w-9, fill='#f7df2e', outline='', tags='rect')
        window.update()
        #time.sleep(0.05)

    def check_neighbors(self, s=False):
        neighbors = []

        if not edge(self.i-1, self.j):
            top = grid[self.i-1][self.j]
            if not top.visited:
                neighbors.append(top)

        if not edge(self.i, self.j+1):
            right = grid[self.i][self.j+1]
            if not right.visited:
                neighbors.append(right)
        if not edge(self.i+1, self.j):
            bottom = grid[self.i+1][self.j]
            if not bottom.visited:
                neighbors.append(bottom)
        if not edge(self.i, self.j-1):
            left = grid[self.i][self.j-1]
            if not left.visited:
                neighbors.append(left)

        if len(neighbors) > 0:
            return neighbors[randrange(len(neighbors))]
        else:
            return False


def edge(i, j):
    if i<0 or j<0 or i>= rows or j>= cols:
        return True
    return False


def setup():
    global current

    for i in range(rows):
        for j in range(cols):
            grid[i][j] = Cell(i, j)

    current = grid[0][0]
    current.visited = True


def draw():
    global current

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j].show()

    while True:
        current.highlight()
        current.draw_visited()

        # STEP 1
        next_cell = current.check_neighbors()
        if next_cell:

            # STEP 2
            stack.append(current)
            solve.append(current)

            # STEP 3
            remove_walls(current, next_cell) #######

            # STEP 4
            current = next_cell
            current.visited = True

        elif len(stack) > 0:
            current = stack.pop()
            backtrack.append(current)
        else:
            break


def remove_walls(c, n):
    y = c.i - n.i
    x = c.j - n.j
    if x == 0:
        if y == -1:
            canvas.delete(c.rl)
            canvas.delete(n.ll)
            c.walls[1] = False
            n.walls[3] = False
            window.update()
        elif y == 1:
            canvas.delete(c.ll)
            canvas.delete(n.rl)
            c.walls[3] = False
            n.walls[1] = False
            window.update()

    if y == 0:
        if x == -1:
            canvas.delete(c.bl)
            canvas.delete(n.tl)
            c.walls[2] = False
            n.walls[0] = False
            window.update()
        elif x == 1:
            canvas.delete(c.tl)
            canvas.delete(n.bl)
            c.walls[0] = False
            n.walls[2] = False
            window.update()
            #print(c.__dict__)

def draw_solve():
    global current
    solve.reverse()
    backtrack.reverse()
    current = solve.pop()

    while True:
        i = current.i
        j = current.j

        if i == rows-1 and j == cols-1:
            current.highlight()
            break

        if not current.choose:
            current.highlight()
            current.choose = True
            current = solve.pop()
            window.update()
            time.sleep(0.1)

        elif current.choose:
            current.draw_visited()
            current = backtrack.pop()
            window.update()
            time.sleep(0.1)

if __name__ == '__main__':
    setup()
    draw()
    button = Button(window, text='Show Solve!', command=draw_solve).pack()

    def change(event):
        print('Yes!!')
        a = canvas.itemconfigure(current.rect, fill='green')

        canvas.update()
        window.update()
        b = canvas.itemcget(current.rect, "fill")
        print('B', b)
    d = canvas.bind('<Button-1>', change)
    print('I am bind d = ', d)
    Label(window, text='Made by: Ali Mahmoud', fg='red', bg='white').pack(side=RIGHT)
    print(len(solve))
    print(solve)
    print(len(backtrack))

    window.mainloop()