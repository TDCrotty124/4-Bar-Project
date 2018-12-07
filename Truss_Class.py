import numpy as np


class Node:
    def __init__(self):
        self.name = None
        self.x = None
        self.y = None

class Link:
    def __init__(self):
        self.name = None
        self.node1name = None
        self.node2name = None
        self.node1 = None
        self.node2 = None
        self.length = None
        self.angle = None

class Truss:
    def __init__(self, ):
        self.title = None
        self.Sut = None
        self.Sy = None
        self.E = None
        self.FStatic = None
        self.nodes = [] # an empty list of nodes
        self.links = [] # an empty list of links
        self.longest = -99999999
        self.longestLink = None

    def ReadTrussData(self, data):
        #data is an array of strings, read from a Truss data file
        for line in data:       # this loops over all the lines
            cells = line.strip().split(',')
            keyword = cells[0].lower()

            if keyword == 'Title': self.title = cells[1].replace("'", "")
            if keyword == 'Static_Factor': self.FStatic = float(cells[1])
            if keyword == 'Distance_unit': self.title = cells[1].replace("'", "")
            if keyword == 'Force_unit': self.title = cells[1].replace("'", "")

            if keyword == 'Material':
                self.Sut = float(cells[1])
                self.Sy = float(cells[2])
                self.E = float(cells[3])

            # if keyword == 'Fatigue_factor': self.ff = float(cells[1])
            # if keyword == 'Static_Factor': self.FStatic = float(cells[1])
            # if keyword == 'Buckling_Factor': self.bf = float(cells[1])
            # if keyword == 'Min_Diameter': self.mdia = float(cells[1])

            if keyword == 'node':
                thisnode = Node()
                thisnode.name = cells[1].strip()
                thisnode.x = float(cells[2].strip())
                thisnode.y = float(cells[3].strip())
                self.nodes.append(thisnode)

            if keyword == 'link':
                thislink = Link()
                thislink.name = cells[1].strip()
                thislink.node1name = cells[2].strip()
                thislink.node2name = cells[3].strip()
                self.links.append(thislink)

            # if keyword == 'supports':
            #     Truss.name = [cells[1].replace("'", "")]
            #     self.node = float(cells[2])
            #     self.direction = float(cells[3])
            #
            # if keyword == 'loadset':
            #     self.Loadset.name = [cells[1].replace("'" , "")]
            #     this_load = [cells[1].replace("'", "")]
            #     ncells = len(cells)
            #     for cell in cells[2:]:
            #         value = float(cell.replace("(", "").replace(")", ""))
            #         this_load.append(value)
            #     self.list.append(this_load)
        #end for line
        self.UpdateLinks()


    def UpdateLinks(self):
            # think this is where the for loop that loops over links goes
            # finds the length and angle of each link
            #get the node info
        for link in self.links:
            for node in self.nodes:
                if node.name == link.node1name:
                    link.node1 = node
                if node.name == link.node2name:
                    link.node2 = node
            #next node
        #next link

        # get link lengths and angles
        # loop over all the links looking at their nodes and pythagorizing their X,Y locations
        self.longest = 0  #starting point for lengths longer than zero
        self.longestlink = None
        for link in self.links:         # loops all over the links
            x1 = link.length = link.node1.x     # saving the nodes within their values
            y1 = link.length = link.node1.y
            x2 = link.length = link.node2.x
            y2 = link.length = link.node2.y
            link.length = np.sqrt( (x2-x1)**2 + (y2-y1)**2)
            link.angle = np.arctan2((y2-y1),(x2-x1))

            if link.length > self.longest:
                self.longest = link.length
                self.longestLink = link
        #next link


    def GenerateReport(self):       # string

        rpt ='                       Truss Design Report\n'
        rpt+= '\nTitle: {}\n'.format(self.title)    # add something to the report
        rpt+= '\nStatic Factor of Safety: {:6.2f}'.format(self.FStatic)     # takes float value from self.FStatic and adds it into the report
        rpt+= '\nUltimate Strength: {:9.1f}'.format(self.Sut)
        rpt+= '\nYield Strength: {:9.1f}'.format(self.Sy)
        rpt+= '\nModulus of Elasticity: {:6.1f}'.format(self.E)
        rpt+= '\n\n'

        rpt += '------------ Link Summary -----------------'
        rpt+='\nLink (1)    (2)     Length      Angle\n'
        for link in self.links:
            rpt+='{:6}{:7}{:7}'.format(link.name, link.node1name, link.node2name, link.node1, link.node2, link.length, link.angle, )
            rpt+='{:7.2f}   '.format(link.length)
            rpt+='{:10.2f} \n'.format(link.angle)       # \n creates a new line
        rpt += '\n\n'

        return rpt
