from tkinter import *
from RObjects import Node
from RouteAlgorithms import *


root = Tk()
class Window():
    def __init__(self, root):
        self.Nodes=[]
        self.WIDTH = 800
        self.HEIGHT = 800
        self.scaleX, self.scaleY = 2, 2
        self.zoominrate = 1.3
        self.zoomoutrate = 0.7
        self.moverate = 50
        self.depth = 0
        self.maxdepth = 10
        self.canvas = Canvas(root,width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack(fill=BOTH, expand=1)
        self.focusX, self.focusY = self.WIDTH//2, self.HEIGHT//2
        self.Points = []
        self.display_route = False
        self.linewidth = 0.05
         ##############################################################
        self.button1 = Button(text='Show Route', command = self.enableshowroute, bd=1, fg='darkblue')
        self.button1.pack(fill=BOTH, expand=1)
        self.button1.place(x=700,y=700)
        ###############################################################
        self.button1 = Button(text='Hide Route', command = self.disableshowroute, bd=1, fg='darkblue')
        self.button1.pack(fill=BOTH, expand=1)
        self.button1.place(x=700,y=730)
        ###############################################################
        self.algorithm = StringVar(root)
        self.algorithm.set("NerestNeighbor")
        self.algorithms_dropdown = OptionMenu(root, self.algorithm, "2-Opt", "NerestNeighbor", command=self.switchAlgorithm)
        self.algorithms_dropdown.config(bg='yellow', width=10)
        self.algorithms_dropdown.place(x=650, y=100)
        ################################################################
        self.deploy_button = Button(text = 'Deploy Algorithm', command=self.deployAlgorithm)
        self.deploy_button.pack(fill=BOTH, expand=1)
        self.deploy_button.place(x=650, y=130)
        ################################################################
        self.distance = 0
        self.distancedisplay = Label(text='total:'+str(self.distance), bd=1)
        self.distancedisplay.place(x=650,y=400)
        self._setupbind()

    def _drawCoordinate(self):
        self.canvas.create_line(0, self.HEIGHT//2, self.WIDTH, self.HEIGHT//2, arrow=LAST, width=1)
        self.canvas.create_line(self.WIDTH//2, 0, self.WIDTH//2, self.HEIGHT, arrow=FIRST, width=1)
    def _resetScale(self):
        self.scaleX = 1
        self.scaleY = 1
    def _setupbind(self):
        self.canvas.focus_set()
        self.canvas.bind('<Key>', self.key)

    def _tocenter(self):
        for point in self.Points:
            point.x = point.x*self.scaleX
            point.y = point.y*self.scaleY
            point.width *= self.scaleX
        self.linewidth*=self.scaleX//10
        self._resetScale()
        centerx = sum([p.x for p in self.Points], 0)//len(self.Points)
        centery = sum([p.y for p in self.Points], 0)//len(self.Points)
        for point in self.Points:
            point.x += self.focusX - centerx
            point.y += self.focusY - centery
            point.doupdate()

    def enableshowroute(self):
        if not self.display_route:
            self.showroute()
            self.display_route = True
    def disableshowroute(self):
        if self.display_route:
            self.canvas.delete('line')
            self.display_route = False
    def addText(self, text):
        self.canvas.create_text(100, 10, fill="darkblue",
                                font="Times 20 italic bold", text=str(text))
    
    def addNodes(self, Nodes, convert=True, append=False):
        Point.numbers = 0
        self.Nodes = Nodes
        if not append:
            self.Points = []
        for i in range(len(Nodes)):
            self.Points.append(Point(Nodes[i], self.canvas))

        if convert:
            for point in self.Points:
                point.x += self.WIDTH//2
                point.y += self.HEIGHT//2
                point.y *= -1
        
    def plot(self):
        self._tocenter()
        if self.display_route:
            self.showroute()

    def showroute(self):
        for i in range(len(self.Points)-1):
            self.canvas.create_line(
                self.Points[i].x, self.Points[i].y, self.Points[i+1].x, self.Points[i+1].y, arrow=LAST,
                width=self.linewidth, tags='line')

    def key(self, event):
        if event.char == 'z':
            self.scaleX *= self.zoominrate
            self.scaleY *= self.zoominrate
            self.depth += 1
            self.redraw()
        elif event.char == 'x':
            self.scaleX *= self.zoomoutrate
            self.scaleY *= self.zoomoutrate
            self.depth -= 1
            self.redraw()
        elif event.char == 'w':
            self.focusY += self.moverate
            self.redraw()
        elif event.char == 's':
            self.focusY -= self.moverate
            self.redraw()
        elif event.char == 'd':
            self.focusX -= self.moverate
            self.redraw()
        elif event.char == 'a':
            self.focusX += self.moverate
            self.redraw()

    def redraw(self, restorezoom=False):
        self.canvas.delete("all")
        if restorezoom:
            self.scaleX = self.zoominrate ** self.depth
            self.scaleY = self.zoominrate ** self.depth
            pass
        self.plot()

    def switchAlgorithm(self, value):
        self.algorithm = value
        print(self.algorithm)
        

    def deployAlgorithm(self):
        if self.algorithm == '2-Opt':
            self.Nodes = LocalSearch.Opt2Solve(self.Nodes)
            self.addNodes(self.Nodes)
        else:
            self.Nodes = NNRoute.Solve(self.Nodes)
            self.addNodes(self.Nodes)
        self.distance = round(SumDistance([node.loc for node in self.Nodes]), 6)
        self.distancedisplay.config(text="total: "+str(self.distance))
        self.redraw(restorezoom=True)


class Point():
    numbers = 0
    def __init__(self, Node, canvas):
        Point.numbers += 1
        self.r = 1
        self.x = Node.x
        self.y = Node.y
        self.name = Node.name
        self.x1, self.y1 = self.x+self.r, self.y+self.r
        self.x2, self.y2 = self.x-self.r, self.y-self.r
        self.width = 0.1
        self.canvas = canvas
        self.color = 'black'
        if Point.numbers == 1:
            self.color = 'blue'
            self.width *= 2
        self.oval = self.canvas.create_oval(
                    self.x1, self.y1, self.x2, self.y2, width=self.width,
                    fill='black', outline = self.color)
        self.canvas.tag_bind(self.oval, "<Enter>", self.on_enter)
        self.canvas.tag_bind(self.oval, "<Leave>", self.on_leave)
        self.tip = None

    def doupdate(self):
        self.x1, self.y1 = self.x+self.r, self.y+self.r
        self.x2, self.y2 = self.x-self.r, self.y-self.r
        self._redraw()
        self.canvas.tag_bind(self.oval, "<Enter>", self.on_enter)
        self.canvas.tag_bind(self.oval, "<Leave>", self.on_leave)

    def _redraw(self):
        self.oval = self.canvas.create_oval(
                    self.x1, self.y1, self.x2, self.y2, width=self.width,
                    fill='black', outline=self.color)
    def on_enter(self,event):
        self.tip = self.canvas.create_text(self.x, self.y-20, text=self.name, tags='displaycity')
        self.canvas.tag_bind(self.tip,"<Enter>", self.on_leave)
    def on_leave(self,event):
        self.canvas.delete(self.tip)