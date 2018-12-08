import numpy as np

from OpenGL.GL import *

from OpenGL_2D_class import gl2DCircle

from copy import deepcopy

from math import *

from scipy.optimize import fsolve


class style:
    def __init__(self):
        self.name = None
        self.rgb = None
        self.width = None


# class values:
# #     def __init__(self):
# #         self.name = None
# #         self.
# #         self.angle = None


class Fourbar:
    def __init__(self, ):
        self.linestyle = []
        self.connections = []
        self.payload = []
        self.payloadx = []
        self.payloady = []
        self.positions = []
        self.boundary = []
        self.window = []  # an empty list of nodes

        self.p0 = None
        self.p1 = None
        self.p2 = None

        self.a0 = None
        self.b0 = None

        self.ha = None
        self.ka = None

        self.a0x = None
        self.a0y = None
        self.b0x = None
        self.b0y = None

        self.a1x = None
        self.a1y = None
        self.b1x = None
        self.b1y = None

        self.a2x = None
        self.a2y = None
        self.b2x = None
        self.b2y = None

        self.newx = None
        self.newy = None

        self.theta3 = None
        self.theta4 = None


        # data for animation
        # self.nframes = 121
        # self.dronepath = np.zeros([self.nframes, 2])
        # self.ballpath = np.zeros([self.nframes, 2])
        # self.tmax = 1.5 * self.ball_speed / self.gc
        # self.CalculateFlightPaths()



        # self.ra = 1
        #
        # self.hb = 2
        # self.kb = 1
        # self.rb = 0

        # self.centera = None
        # self.centerb = None

        # self.links = [] # an empty list of links
        # self.longest = -99999999
        # self.longestLink = None

    # Don't change anything in ReadTrussData
    def ReadFourBarData(self, data):  # reads data from text file
        # data is an array of strings, read from a Truss data file
        for line in data:  # loop over all the lines
            cells = line.strip().split(',')
            keyword = cells[0].lower()

            if keyword == 'title': self.title = cells[1].replace("'", "")
            if keyword == 'connections':
                for con in cells[1:]:
                    ans = float(con.replace("(", "").replace(")", ""))
                    self.connections.append(ans)

            if keyword == 'linestyle':
                this_name = [cells[1].replace("'", "").replace(" ", "")]
                ncells = len(cells)
                for cell in cells[2:]:
                    value = float(cell.replace("(", "").replace(")", ""))
                    this_name.append(value)
                self.linestyle.append(this_name)

            if keyword == 'payload':
                this_name = [cells[1].replace("'", "").replace(" ", "")]
                this_name.append(cells[2].replace(" ", ""))
                ncells = len(cells)
                for cell in cells[3:]:
                    value = float(cell.replace("(", "").replace(")", ""))
                    this_name.append(value)
                self.payload.append(this_name)

            if keyword == 'positions':
                for pos in cells[1:]:
                    ans = float(pos.replace("(", "").replace(")", ""))
                    self.positions.append(ans)

            if keyword == 'boundary':
                this_name = [cells[1].replace("'", "").replace(" ", "")]
                this_name.append(cells[2].replace(" ", ""))
                ncells = len(cells)
                for cell in cells[3:]:
                    value = float(cell.replace("(", "").replace(")", ""))
                    this_name.append(value)
                self.boundary.append(this_name)

            if keyword == 'window':
                for win in cells[1:]:
                    ans = float(win.replace("(", "").replace(")", ""))
                    self.window.append(ans)

        self.a0x = self.connections[0]
        self.a0y = self.connections[1]
        self.b0x = self.connections[2]
        self.b0y = self.connections[3]
        self.a0 = np.array([self.a0x, self.a0y])
        self.b0 = np.array([self.b0x, self.b0y])

    def Translation(self):
        p0x = self.positions[0]
        p0y = self.positions[1]
        p1x = self.positions[2]
        p1y = self.positions[3]
        theta1 = np.radians(self.positions[4])
        p2x = self.positions[5]
        p2y = self.positions[6]
        theta2 = np.radians(self.positions[7])
        p0 = np.array([p0x, p0y])
        p1 = np.array([p1x, p1y])
        p2 = np.array([p2x, p2y])

        self.a0 = np.array([self.a0x, self.a0y])
        self.b0 = np.array([self.b0x, self.b0y])

        # test = np.zeros((3,3))
        alldata = []
        for j in range(len(
                self.payload)):  # theres multiple sections of payloades so some how this line is supposed to sort through them
            vals = []
            for i in range(2, len(self.payload[j]) - 1,
                           2):  # this i is supposed to sort through the data once a payload row is selected
                # if i > 1 and i % 2 == 0: #and i < self.payload-2:                 # based on order, if its odd it should be an x... even should be y...
                x = self.payload[j][i]
                y = self.payload[j][i + 1]
                # vals.append((np.array([x,y])))
                vals.append([x, y])

            vals_numpy = np.array(vals)
            alldata.append(vals_numpy)

        self.p0 = deepcopy(alldata)
        self.p1 = deepcopy(alldata)
        self.p2 = deepcopy(alldata)

        self.a0 = deepcopy(self.a0)
        self.a1 = deepcopy(self.a0)
        self.a2 = deepcopy(self.a0)

        self.b0 = deepcopy(self.b0)
        self.b1 = deepcopy(self.b0)
        self.b2 = deepcopy(self.b0)

        # Translate to origin
        for i in range(len(self.p1)):
            for j in range(len(self.p1[i])):
                self.p1[i][j][0] -= p0x
                self.p1[i][j][1] -= p0y
                self.p2[i][j][0] -= p0x
                self.p2[i][j][1] -= p0y

        self.a1[0] -= p0x
        self.a1[1] -= p0y
        self.b1[0] -= p0x
        self.b1[1] -= p0y

        self.a2[0] -= p0x
        self.a2[1] -= p0y
        self.b2[0] -= p0x
        self.b2[1] -= p0y

        # Rotate
        rotate1 = [[np.cos(theta1), np.sin(theta1)], [-np.sin(theta1), np.cos(theta1)]]
        rotate2 = [[np.cos(theta2), np.sin(theta2)], [-np.sin(theta2), np.cos(theta2)]]

        for i in range(len(self.p1)):
            self.p1[i] = np.matmul(self.p1[i], rotate1)
            self.p2[i] = np.matmul(self.p2[i], rotate2)

        self.a1 = np.matmul(self.a1, rotate1)
        self.b1 = np.matmul(self.b1, rotate1)
        self.a2 = np.matmul(self.a2, rotate2)
        self.b2 = np.matmul(self.b2, rotate2)

        # Currently both at origin and rotated

        for i in range(len(self.p1)):
            for j in range(len(self.p1[i])):
                self.p1[i][j][0] += p1x
                self.p1[i][j][1] += p1y
                self.p2[i][j][0] += p2x
                self.p2[i][j][1] += p2y

        self.a1[0] += p1x
        self.a1[1] += p1y
        self.b1[0] += p1x
        self.b1[1] += p1y

        self.a2[0] += p2x
        self.a2[1] += p2y
        self.b2[0] += p2x
        self.b2[1] += p2y

        self.a1x = self.a1[0]
        self.a1y = self.a1[1]
        self.b1x = self.b1[0]
        self.b1y = self.b1[1]

        self.a2x = self.a2[0]
        self.a2y = self.a2[1]
        self.b2x = self.b2[0]
        self.b2y = self.b2[1]

        # math studd to calculate positions

        # newpayload.append(newpayloadxy)

    def ThreeBarCircle(self):
        # initial guesses
        self.ha = 1
        self.ka = 1
        self.ra = 1

        self.hb = 0
        self.kb = 0
        self.rb = 0

        def solve(vars, args):
            [h, k, r] = vars
            [x0, y0, x1, y1, x2, y2] = args

            a = sqrt(((x0 - h) ** 2) + ((y0 - k) ** 2)) - r
            b = sqrt(((x1 - h) ** 2) + ((y1 - k) ** 2)) - r
            c = sqrt(((x2 - h) ** 2) + ((y2 - k) ** 2)) - r

            return a, b, c

        vars = [self.ha, self.ka, self.ra]
        args = [self.a0[0], self.a0[1], self.a1[0], self.a1[1], self.a2[0], self.a2[1]]
        self.ha, self.ka, self.ra = fsolve(solve, vars, args=args)  # ha = x, ka = y, r = radius of circle

        vars = [self.hb, self.kb, self.rb]
        args = [self.b0[0], self.b0[1], self.b1[0], self.b1[1], self.b2[0], self.b2[1]]
        self.hb, self.kb, self.rb = fsolve(solve, vars, args=args)

        # self.l1 = self.ra
        # self.l2 = sqrt((self.b0x + self.a0x) ** 2 + (self.b0y + self.a0y) ** 2)
        # self.l3 = self.rb
        # self.l4 = sqrt((self.ha + self.hb) ** 2 + (self.ka + self.kb) ** 2)

        self.theta3 = atan2((self.a0y - self.ka), (self.a0x - self.ha)) * 180 / np.pi
        self.theta4 = atan2((self.a2y - self.ka), (self.a2x - self.ha)) * 180 / np.pi

    def CreateDraggingList(self):
        draglist= [[self.a0x, self.a0y],
                   [self.b0x, self.b0y]]
        return draglist


    def DraggingListItemChanged(self, x, y, draglist, index):
        if index == 0:  # A Connection
            self.a0x, self.a0y = [x, y]
            draglist[0] = [x, y]

        if index == 1:  # B Connection
            self.b0x, self.b0y = [x, y]
            draglist[1] = [x, y]

        self.Translation()
        self.ThreeBarCircle()

    # def draggingCallback(self, start):
    #     if start is True:
    #         draglist = self.fourbar.CreateDraggingList()
    #         near = 15
    #         self.glwindow1.g1StartDragging(self.draggingCallback, draglist, near, handlesize=.1, handlewidth=1,
    #                                        handlecolor=[1, 0, 1])
    #         self.ui.dragging.setChecked(False)
    #     elif start is False:
    #         self.glwindow1.glStopDragging()
    #         self.ui.dragging.setChecked(False)

    # def ShowConstruction(self, show)
    # if show is True...




    # Animation Stuff

    # def CalculateFlightPaths(self):
    #     # This to draw the picture and during animation!
    #     for frame in range(self.nframes):
    #         time = self.tmax * frame / self.nframes
    #
    #         dronex = self.drone_x - self.drone_speed * time
    #
    #         ballx = self.barrel_x + self.ball_v0x * time
    #         bally = self.barrel_y + self.ball_v0y * time - self.gc / 2 * time ** 2
    #
    #         self.dronepath[frame, :] = [dronex, self.drone_y]
    #         self.ballpath[frame, :] = [ballx, bally]
    #     # end  def
    #
    #     # finds frames for the payload to move through
    #
    # def ConfigureAnimationFrame(self, frame, nframes):
    #     self.drone_x = self.dronepath[frame, 0]
    #     self.ball_x = self.ballpath[frame, 0]
    #     self.ball_y = self.ballpath[frame, 1]
    #


    def DrawTrussPicture(self):
        # this is what actually draws the picture
        # using data to control what is drawn

        # begin drawing connected lines
        # use GL_LINE for drawing a series of disconnected lines
        # draws boundaries using self.boundary and self.linestyle with correct color and thickness
        for i in range(len(self.boundary)):
            for k in range(len(self.linestyle)):
                if self.boundary[i][1] == self.linestyle[k][0]:
                    red = self.linestyle[k][1]
                    green = self.linestyle[k][2]
                    blue = self.linestyle[k][3]
                    width = self.linestyle[k][4]
                    glColor3f(red, green, blue)
                    glLineWidth(width)
                    for j in range(2, len(self.boundary[i]) - 3, 2):
                        glBegin(GL_LINE_STRIP)
                        glVertex2f(self.boundary[i][j], self.boundary[i][j + 1])
                        glVertex2f(self.boundary[i][j + 2], self.boundary[i][j + 3])
                        glEnd()

        # glColor3f(1, .5, .3)  #
        # glLineWidth(1.5)
        # for i in range(0, len(self.connections) - 1, 2):
        #     gl2DCircle(self.connections[i], self.connections[i + 1], .015 * (abs(self.window[0]) + abs(self.window[1])),fill=True)

        # Draws the A and B points according p0, p1, p2 of payload
        glColor3f(1, .5, .3)  #
        glLineWidth(1.5)
        gl2DCircle(self.a0[0], self.a0[1], .015 * (abs(self.window[0]) + abs(self.window[1])), fill=True)

        glColor3f(1, .5, .3)  #
        glLineWidth(1.5)
        gl2DCircle(self.b0[0], self.b0[1], .015 * (abs(self.window[0]) + abs(self.window[1])), fill=True)

        glColor3f(0, 1, 0)  #
        glLineWidth(1.5)
        gl2DCircle(self.a1[0], self.a1[1], .015 * (abs(self.window[0]) + abs(self.window[1])), fill=True)

        glColor3f(0, 1, 0)  #
        glLineWidth(1.5)
        gl2DCircle(self.b1[0], self.b1[1], .015 * (abs(self.window[0]) + abs(self.window[1])), fill=True)

        glColor3f(1, 0, 0)  #
        glLineWidth(1.5)
        gl2DCircle(self.a2[0], self.a2[1], .015 * (abs(self.window[0]) + abs(self.window[1])), fill=True)

        glColor3f(1, 0, 0)  #
        glLineWidth(1.5)
        gl2DCircle(self.b2[0], self.b2[1], .015 * (abs(self.window[0]) + abs(self.window[1])), fill=True)

        # Draws the positions that the payload will go through
        glColor3f(.5, .5, .5)  #
        glLineWidth(1.5)
        for i in range(len(self.p0)):
            for j in range(0, len(self.p0[i]) - 1, 1):
                glBegin(GL_LINE_STRIP)
                glVertex2f(self.p0[i][j][0], self.p0[i][j][1])
                glVertex2f(self.p0[i][j + 1][0], self.p0[i][j + 1][1])
                glEnd()
                glBegin(GL_LINE_STRIP)
                glVertex2f(self.p1[i][j][0], self.p1[i][j][1])
                glVertex2f(self.p1[i][j + 1][0], self.p1[i][j + 1][1])
                glEnd()
                glBegin(GL_LINE_STRIP)
                glVertex2f(self.p2[i][j][0], self.p2[i][j][1])
                glVertex2f(self.p2[i][j + 1][0], self.p2[i][j + 1][1])
                glEnd()

        # Draws the actual payload with colored lines and the wheel
        for i in range(len(self.payload)):
            for k in range(len(self.linestyle)):
                if self.payload[i][1] == self.linestyle[k][0]:
                    red = self.linestyle[k][1]
                    green = self.linestyle[k][2]
                    blue = self.linestyle[k][3]
                    width = self.linestyle[k][4]
                    glColor3f(red, green, blue)
                    glLineWidth(width)
                    for j in range(2, len(self.payload[i]) - 3, 2):
                        glBegin(GL_LINE_STRIP)
                        glVertex2f(self.payload[i][j], self.payload[i][j + 1])
                        glVertex2f(self.payload[i][j + 2], self.payload[i][j + 3])
                        glEnd()

        # draws the links between the A and B connections and the arc that fsolve calculated
        glColor3f(0, 0, 0)  #
        glLineWidth(1.5)
        gl2DCircle(self.ha, self.ka, .02 * (abs(self.window[0]) + abs(self.window[1])), fill=True)

        glColor3f(0, 0, 0)  #
        glLineWidth(1.5)
        gl2DCircle(self.hb, self.kb, .02 * (abs(self.window[0]) + abs(self.window[1])), fill=True)

        glBegin(GL_LINE_STRIP)
        glColor3f(0, 0, 0)
        glVertex2f(self.ha, self.ka)
        glVertex2f(self.a0[0], self.a0[1])
        glEnd()

        glBegin(GL_LINE_STRIP)
        glColor3f(1, 1, 0)
        glVertex2f(self.hb, self.kb)
        glVertex2f(self.b0[0], self.b0[1])
        glEnd()

        # test for sports wing

        # glColor3f(.2, .8, 1)  #
        # glLineWidth(1.5)
        # gl2DCircle(4,1,.018,fill=True)
        #
        # glColor3f(.2, .8, 1)  #
        # glLineWidth(1.5)
        # gl2DCircle(4.3,1.7,.018,fill=True)
