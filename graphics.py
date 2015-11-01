from tkinter import *
from consts import *
from time import sleep




class Table:
    def tk_init(self):
        self.root = Tk()
##        self.root.geometry(str((self.w+1) * C_W) + 'x' + str((self.h+1) * C_H) + '+0+0')
        self.root.minsize((self.w + 1) * C_W, (self.h + 1) * C_H)
        self.canv = Canvas(self.root, bg = 'white')
        self.canv.pack(fill = BOTH, expand = 1)
    __init__ = tk_init
    def draw(self):
##        arr = self.table
        self.canv.delete('table')
        self.canv.delete('grid')
        for x_ in range(DAYS_COUNT):
            x = C_W + (x_ + 0.5) * HOURS_IN_DAY * C_W
            self.canv.create_text(x, 0.25 * C_H,
                 text = WEEK[x_], tag = 'table')
        for y in range(self.h):
            self.canv.create_text(0.5 * C_W, (y + 1.5) * C_H, text = self.names[y], tag = 'table')
            for x in range(self.w):
                if y == 0:
                    self.canv.create_text((x+1.5) * C_W, (y+0.75) * C_H,
                         text = str((x % HOURS_IN_DAY) + 1), tag = 'table')
                text = ''
                if self.table[y][x] != None:
                    text = ''.join(map(str, [self.table[y][x].c, '   ', self.table[y][x].l, '\n', self.table[y][x].s]))
                    self.canv.create_rectangle((x+1) * C_W, (y+1) * C_H, (x+2) * C_W, (y+2) * C_H,
                                               fill = PAL[self.table[y][x].c - 5], width = 0, tag = 'table')
                self.canv.create_text((x+1.5) * C_W, (y+1.5) * C_H, text = text, tag = 'table', justify = 'center')
        for y in range(self.h + 2):
            self.canv.create_line(0, y * C_H, (self.w + 1) * C_W, y * C_H, width = 2, tag = 'grid')
        self.canv.create_line(C_W, C_H/2, (self.w + 1) * C_W, C_H/2, width = 2, tag = 'grid')
        for x in range(self.w + 2):
            if (x-1) % HOURS_IN_DAY:
                y0 = C_H / 2
                width = 2
            else:
                y0 = 0
                width = 4
            self.canv.create_line(x * C_W, y0, x * C_W, (self.h + 1) * C_H, width = width, tag = 'grid')
    def labeldraw(self, x_, y_, info = 0, item = 0):
        tag = ('label', 'label_' + str(item))
        self.canv.delete(tag[1])
        x, y = (x_ + 1.5) * C_W, (y_ + 1.5) * C_H
        r = 8
        if info:
            fill = PAL[item]
        else:
            fill = 'white'
        self.canv.create_oval(x-r, y-r, x+r, y+r,
                              fill = PAL[item], outline = 'white', width = 3, tag = tag)
        self.canv.create_rectangle(x, y, x + 15, y + 15,
                                   fill=fill, outline = 'white', width = 3, tag = tag)
        self.root.update()
        if item == 2:
            self.root.after(int(SLEEP_TIMES[item] * 2000), lambda: self.canv.delete(tag[1]))
            if info:
                sleep(SLEEP_TIMES[item])
        sleep(SLEEP_TIMES[item])
