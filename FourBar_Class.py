import numpy as np

from OpenGL.GL import *

from OpenGL_2D_class import gl2DCircle


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



            # if keyword == 'node':
            #     thisnode=Node()
            #     thisnode.name = cells[1].strip()
            #     thisnode.x=float(cells[2].strip())
            #     thisnode.y=float(cells[3].strip())
            #     self.nodes.append(thisnode)
            #
            # if keyword == 'link':
            #     thislink = Link()
            #     thislink.name = cells[1].strip()
            #     thislink.node1name= cells[2].strip()
            #     thislink.node2name= cells[3].strip()
            #     self.links.append(thislink)

        #end for line
        # self.UpdateLinks()

    # Add 1 more thing which is the viewing size
    # def UpdateLinks(self):
    #     #get the node info
    #     # for link in self.links:
    #     #     for node in  self.nodes:
    #     #         if node.name == link.node1name:
    #     #             link.node1 = node
    #     #         if node.name == link.node2name:
    #     #             link.node2 = node
    #     #     #next node
    #     #next link
    #
    #     #get link lengths and angles
    #     # self.longest = -99999999
    #     # self.longestLink = None
    #     # for link in self.links:
    #     #     x1=link.length = link.node1.x
    #     #     y1=link.length = link.node1.y
    #     #     x2=link.length = link.node2.x
    #     #     y2=link.length = link.node2.y
    #     #     link.length = np.sqrt( (x2-x1)**2 + (y2-y1)**2)
    #     #     link.angle = np.arctan2((y2-y1),(x2-x1))
    #
    #         # if link.length > self.longest:
    #         #     self.longest = link.length
    #         #     self.longestLink = link
    #
    #     #     we must create a value to compare to nodes to make sure we are receiving the max and min x&y values
    #         xmin = 100000
    #         ymin = 100000
    #         xmax = -100000
    #         ymax = -100000
    #
    #         # for node in self.nodes:    # for loop that sets node.x and node.y to its max and min values to create a certain size for the GL
    #         #     if node.x > xmax:
    #         #         xmax = node.x
    #         #     if node.x < xmin:
    #         #         xmin = node.x
    #         #     if node.y > ymax:
    #         #         ymax = node.y
    #         #     if node.y < ymin:
    #         #         ymin = node.y
    #
    #
    #
    #
    #         self.drawingsize = [xmin, xmax, ymin, ymax]
    #     # next link

    def Translation(self):
        p0x = self.positions[0]
        p0y = self.positions[1]
        p1x = self.positions[2]
        p1y = self.positions[3]
        theta1 = self.positions[4]
        p2x = self.positions[5]
        p2y = self.positions[6]
        theta2 = self.positions[7]

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
        dp1 = ()




                    # math studd to calculate positions

                    # newpayload.append(newpayloadxy)
        # points = []
        # pointsx = []
        # pointsy = []
        # self.positions = []
        # p0x = self.positions[0]
        # p0y = self.positions[1]
        # p1x = self.positions[2]
        # p1y = self.positions[3]
        # theta1 = self.positions[4]
        # p2x = self.positions[5]
        # p2y = self.positions[6]
        # theta2 = self.positions[7]
        #
        # for point in range(len(points)):
        #     if point % 2 != 0:
        #         pointsx.append(point)
        #     else:
        #         pointsy.append(point)
        # deltaPx = p1x - p0x
        # deltaPy = p1y - p0y

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




