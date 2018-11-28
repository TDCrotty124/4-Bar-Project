import numpy as np

from OpenGL.GL import *

from Homeworks.HW10.OpenGL_2D_class import gl2DCircle


class style:
    def __init__(self):
        self.name = None
        self.rgb = None
        self.width = None

# class Link:
#     def __init__(self):
#         self.name=None
#         self.node1name=None
#         self.node2name=None
#         self.node1 = None
#         self.node2 = None
#         self.length=None
#         self.angle=None


class Fourbar:
    def __init__(self, ):
        self.linestyle = []
        self.connections = []
        self.payload = []
        self.positions = []
        self.boundary = []
        self.window = [] # an empty list of nodes
        # self.links = [] # an empty list of links
        # self.longest = -99999999
        # self.longestLink = None


    # Don't change anything in ReadTrussData
    def ReadTrussData(self, data):      # reads data from text file
        #data is an array of strings, read from a Truss data file
        for line in data:  # loop over all the lines
            cells = line.strip().split(',')
            keyword = cells[0].lower()

            if keyword == 'title': self.title = cells[1].replace("'", "")
            if keyword == 'connections':
                for con in cells[2:]:
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
                ncells = len(cells)
                for cell in cells[3:]:
                    value = float(cell.replace("(", "").replace(")", ""))
                    this_name.append(value)
                self.payload.append(this_name)

            if keyword == 'positions':
                for pos in cells[2:]:
                    ans = float(pos.replace("(", "").replace(")", ""))
                    self.positions.append(ans)

            if keyword == 'boundary':
                this_name = [cells[1].replace("'", "").replace(" ", "")]
                ncells = len(cells)
                for cell in cells[3:]:
                    value = float(cell.replace("(", "").replace(")", ""))
                    this_name.append(value)
                self.boundary.append(this_name)

            if keyword == 'window':
                for win in cells[2:]:
                    ans = float(win.replace("(", "").replace(")", ""))
                    self.positions.append(ans)


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
        self.UpdateLinks()

    # Add 1 more thing which is the viewing size
    def UpdateLinks(self):
        #get the node info
        for link in self.links:
            for node in  self.nodes:
                if node.name == link.node1name:
                    link.node1 = node
                if node.name == link.node2name:
                    link.node2 = node
            #next node
        #next link

        #get link lengths and angles
        self.longest = -99999999
        self.longestLink = None
        for link in self.links:
            x1=link.length = link.node1.x
            y1=link.length = link.node1.y
            x2=link.length = link.node2.x
            y2=link.length = link.node2.y
            link.length = np.sqrt( (x2-x1)**2 + (y2-y1)**2)
            link.angle = np.arctan2((y2-y1),(x2-x1))

            if link.length > self.longest:
                self.longest = link.length
                self.longestLink = link

            # we must create a value to compare to nodes to make sure we are receiving the max and min x&y values
            xmin = 100000
            ymin = 100000
            xmax = -100000
            ymax = -100000

            for node in self.nodes:    # for loop that sets node.x and node.y to its max and min values to create a certain size for the GL
                if node.x > xmax:
                    xmax = node.x
                if node.x < xmin:
                    xmin = node.x
                if node.y > ymax:
                    ymax = node.y
                if node.y < ymin:
                    ymin = node.y




            self.drawingsize = [xmin, xmax, ymin, ymax]
        #next link

    # # Don't change anything in GenerateReport
    #   creates the
    # def GenerateReport(self):
    #
    #     rpt ='                      Truss Design Report\n'
    #     rpt+= '\nTitle: {}\n'.format(self.title)
    #     rpt+= '\nStatic Factor of Safety: {:6.2f}'.format(self.FStatic)
    #     rpt+= '\nUltimate Strength: {:9.1f}'.format(self.Sut)
    #     rpt+= '\nYield Strength: {:9.1f}'.format(self.Sy)
    #     rpt+= '\nModulus of Elasticity: {:6.1f}'.format(self.E)
    #     rpt += '\n\n'
    #
    #
    #
    #     rpt += '------------------- Link Summary -------------------------\n'
    #     rpt+='\nLink (1)    (2)      Length      Angle\n'
    #     for link in self.links:
    #         rpt+='{:6}{:7}{:7}'.format(link.name, link.node1name, link.node2name)
    #         rpt+='{:7.2f}  '.format(link.length)
    #         rpt+='{:10.2f}  \n'.format(link.angle)
    #     rpt += '\n\n'
    #
    #     return rpt



    # Contains all the drawing commands for drawing the link lines
        # and the nodes as circles
    def DrawTrussPicture(self):

    # for loop for nodes

    # for loop for links


        # this is what actually draws the picture
        # using data to control what is drawn


        glColor3f(0, 0.4, 0.9)  # Changes the color of the circle nodes
        glLineWidth(1.5)        # controls the width of the line trusses
        radius = self.longestLink.length / 25       # allows the radius of your circle to format and display correctly as the lengths of the trusses will vary with text files
        for N in range(len(self.nodes)):    # loops over all nodes and pulls the x and y values from each node
            gl2DCircle(self.nodes[N].x, self.nodes[N].y, radius, fill=True)     # creates a circle for the node

        # for loop here
        glColor3f(0, 1, 0.8)    # changes the color of the truss lines
        for L in range(len(self.links)):        # loop that runs over all of the links
            glBegin(GL_LINE_STRIP)  # begin drawing connected lines
            glVertex2f(self.links[L].node1.x, self.links[L].node1.y)    # pulls the location of the node1 and
            glVertex2f(self.links[L].node2.x, self.links[L].node2.y)    # draws a line from there to node2. These lines create the trusses in the drawing
            glEnd()

