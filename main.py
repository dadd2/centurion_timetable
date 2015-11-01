from consts import *
from graphics import Table as tk_table
from random import randint


teachers = {}
def to_cnf(s): #this method is for reading a file
    a = s.split(':')
    return [int(a[0]), int(a[1]), a[2], int(a[3]), a[4]]
def to_elem(lst):
    a = lst[:]
    a.pop(1)
    return Hour(*a)
def to_prt(el):
    if el == None:
        return ''
    return el.str()
class Hour:
    def __init__(self, c, s, l, g):
        self.c = c #class
        self.s = s #subject
        self.l = l #level
        self.g = g #group
    def str(self):
        return ' '.join(map(str, [self.c, self.s, self.l, self.g]))
class Table(tk_table):
    plan = {}
    names = []
    table = [[]]
    w = HOURS_IN_DAY * DAYS_COUNT
    h = 0
    def __init__(self, filename = 'base.txt'):
        a = open(filename, 'r', encoding = 'utf-8')
        readed = a.read()
        print(readed)
        self.plan = dict(map(lambda s: [s.split()[0], list(map(to_cnf, s.split()[1:]))], readed.split('\n')[1:]))
        a.close()
        self.h = len(self.plan)
        self.names = list(self.plan)
        self.names.sort()
        self.table = [[None for i in range(self.w)] for j in range(self.h)]
        for name in self.names:
            for conf in self.plan[name]:
                for j in range(conf[1]):
                    i = 0
                    while self.table[self.names.index(name)][i] != None:
                        i += 1
                    self.table[self.names.index(name)][i] = to_elem(conf)
        self.tk_init()
        self.draw()
    def mainloop(self):
        self.root.mainloop()
    def save(self, filename = 'out.txt'):
        a = open(filename, 'w')
        print('\n'.join(map(lambda l: '\t'.join(map(to_prt, l)), self.table)), file = a)
        a.close()
    def yview(self, x, y_, tmp = None, direct = 1):
        if tmp == None:
            tmp = self.table[y_][x]
        if tmp == None:
            return 0
        if direct == 1:
            r = range(y_ - 1, -1, -1)
        else:
            r = range(y_ + 1, self.h)
        for y in r:
            if y != y_:
                if self.table[y][x] != None and self.table[y][x].c == tmp.c and self.table[y][x].s != tmp.s:
                    self.labeldraw(x, y, 1, 2)
                    return 1
                self.labeldraw(x, y, 0, 2)
        return 0
    def xsearch(self, x_, y, direct = 1):
        prebrokens = [x_]
        for x in range(self.w):
            if x != x_ and not self.yview(x, y, tmp = self.table[y][x_], direct=direct):
                if (self.table[y][x] == None  or not self.yview(x_, y, tmp = self.table[y][x], direct=direct)):
                    self.labeldraw(x, y, 1, 1)
                    return x
                else:
                    prebrokens = [x] + prebrokens
            else:
                self.labeldraw(x, y, 0, 1)
        return prebrokens[randint(0, len(prebrokens)-1)]
    def swap(self, x1, y1, x2, y2):
        self.table[y1][x1], self.table[y2][x2] = self.table[y2][x2], self.table[y1][x1]
    def sort(self):
        for y in range(1, self.h):
            for x in range(self.w):
                if self.yview(x, y, direct = 1):
                    self.labeldraw(x, y, 0, 0)
                    self.swap(x, y, self.xsearch(x, y, direct = 1), y)
                    self.draw()
                    self.labeldraw(x, y, 0, 0)
                else:
                    self.labeldraw(x, y, 1, 0)
                self.root.update()
        self.canv.delete('label')
#'''
#'''
t = Table()#'mac_base.txt')
def akt():
    t.sort()
    t.save()
t.root.after(100, akt)
#t.mainloop()
