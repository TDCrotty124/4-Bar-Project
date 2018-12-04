import numpy as np

from OpenGL.GL import *

from Homeworks.HW10.OpenGL_2D_class import gl2DCircle

from copy import deepcopy

class style:
    def __init__(self):
        self.name = None
        self.rgb = None
        self.width = None

class Fourbar:
    def __init__(self, ):
        self.linestyle = []
        self.connections = []
        self.payload = []
        self.payloadx = []
        self.payloady = []
        self.positions = []
        self.boundary = []
        self.window = [] # an empty list of nodes

        self.p0 = None
        self.p1 = None
        self.p2 = None
        # self.links = [] # an empty list of links
        # self.longest = -99999999
        # self.longestLink = None


    # Don't change anything in ReadTrussData
    def ReadFourBarData(self, data):      # reads data from text file
        #data is an array of strings, read from a Truss data file
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
                this_name.append(cells[2].replace(" ",""))
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

    def Translation(self):
        p0x = self.positions[0]
        p0y = self.positions[1]
        p1x = self.positions[2]
        p1y = self.positions[3]
        theta1 = np.radians(self.positions[4])
        p2x = self.positions[5]
        p2y = self.positions[6]
        theta2 = np.radians(self.positions[7])
        p0= np.array([p0x,p0y])
        p1= np.array([p1x,p1y])
        p2 = np.array([p2x,p2y])

        # test = np.zeros((3,3))
        alldata = []
        for j in range(len(self.payload)):    # theres multiple sections of payloades so some how this line is supposed to sort through them
            vals = []
            for i in range(2,len(self.payload[j]) - 1,2):  # this i is supposed to sort through the data once a payload row is selected
                #if i > 1 and i % 2 == 0: #and i < self.payload-2:                 # based on order, if its odd it should be an x... even should be y...
                x = self.payload[j][i]
                y = self.payload[j][i+1]
                #vals.append((np.array([x,y])))
                vals.append([x,y])

            vals_numpy = np.array(vals)
            alldata.append(vals_numpy)


        self.p0 = deepcopy(alldata)
        self.p1 = deepcopy(alldata)
        self.p2 = deepcopy(alldata)

        #Translate to origin
        for i in range(len(self.p1)):
            for j in range(len(self.p1[i])):
                self.p1[i][j][0] -= p0x
                self.p1[i][j][1] -= p0y
                self.p2[i][j][0] -= p0x
                self.p2[i][j][1] -= p0y

        #Rotate
        rotate1 = [[np.cos(theta1), np.sin(theta1)], [-np.sin(theta1), np.cos(theta1)]]
        rotate2 = [[np.cos(theta2), np.sin(theta2)], [-np.sin(theta2), np.cos(theta2)]]

        for i in range(len(self.p1)):
            self.p1[i] = np.matmul(self.p1[i],rotate1)
            self.p2[i] = np.matmul(self.p2[i],rotate2)
        #Currently both at origin and rotated

        for i in range(len(self.p1)):
            for j in range(len(self.p1[i])):
                self.p1[i][j][0] += p1x
                self.p1[i][j][1] += p1y
                self.p2[i][j][0] += p2x
                self.p2[i][j][1] += p2y


                    # math studd to calculate positions

                    # newpayload.append(newpayloadxy)

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
                    for j in range(2,len(self.boundary[i])-3,2):
                        glBegin(GL_LINE_STRIP)
                        glVertex2f(self.boundary[i][j], self.boundary[i][j+1])
                        glVertex2f(self.boundary[i][j+2], self.boundary[i][j+3])
                        glEnd()

        glColor3f(0, 0, 0)  #
        glLineWidth(1.5)
        for i in range(0,len(self.connections)-1,2):
            gl2DCircle(self.connections[i], self.connections[i+1], .03*(abs(self.window[0])+abs(self.window[1])), fill=True)

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

        for i in range(len(self.payload)):
            for k in range(len(self.linestyle)):
                if self.payload[i][1] == self.linestyle[k][0]:
                    red = self.linestyle[k][1]
                    green = self.linestyle[k][2]
                    blue = self.linestyle[k][3]
                    width = self.linestyle[k][4]
                    glColor3f(red, green, blue)
                    glLineWidth(width)
                    for j in range(2,len(self.payload[i])-3,2):
                        glBegin(GL_LINE_STRIP)
                        glVertex2f(self.payload[i][j], self.payload[i][j+1])
                        glVertex2f(self.payload[i][j+2], self.payload[i][j+3])
                        glEnd()









