# standard PyQt5 imports
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtWidgets import QFileDialog, QMessageBox

# standard OpenGL imports
from OpenGL.GLUT import *

from Homeworks.HW10.OpenGL_2D_class import gl2D

# the ui created by Designer and pyuic
from FinalProject import Ui_Dialog
from FourBar_Class import Fourbar

# import the Problem Specific class
from DroneCatcher import DroneCatcher


class main_window(QDialog):
    def __init__(self):
        super(main_window, self).__init__()
        self.ui = Ui_Dialog()
        # setup the GUI
        self.ui.setupUi(self)

        # define any data (including object variables) your program might need
        self.mydrone = DroneCatcher()

        # create and setup the GL window object
        self.setupGLWindows()

        # and define any Widget callbacks (buttons, etc) or other necessary setup
        self.assign_widgets()

        # define two data items
        self.Fourbar = None
        self.filename = None
        # self.filename = "D:/Users/Dela/Documents/Dropbox/_Classes/_3403/__F18 - 3403/Homework/Homework 9 - Truss File/Solution and testing/Truss Design Input File 1.txt"

        # show the GUI
        self.show()

    def assign_widgets(self):  # callbacks for Widgets on your GUI
        self.ui.pushButton_Exit.clicked.connect(self.ExitApp)
        self.ui.horizontalSlider_zoom.valueChanged.connect(self.glZoomSlider)
        self.ui.pushButton_Select.clicked.connect(self.GetFourbar)
    # Widget callbacks start here

    def glZoomSlider(self):  # I used a slider to control GL zooming
        zoomval = float((self.ui.horizontalSlider_zoom.value()) / 200 + 0.25)
        self.glwindow1.glZoom(zoomval)  # set the zoom value
        self.glwindow1.glUpdate()  # update the GL image


    # Setup OpenGL Drawing and Viewing
    def setupGLWindows(self):  # setup all GL windows
        # send it the   GL Widget     and the drawing Callback function
        self.glwindow1 = gl2D(self.ui.openGLWidget, self.DrawingCallback)

        # set the drawing space:    xmin  xmax  ymin   ymax
        self.glwindow1.setViewSize(-10, 500, -10, 200, allowDistortion=False)


    def DrawingCallback(self):
        # this is what actually draws the picture
        if self.Fourbar is not None:
            self.Fourbar()
        # self.Fourbar.DrawTrussPicture()

    def GetFourbar(self):
        # get the filename using the OPEN dialog
        self.filename = QFileDialog.getOpenFileName()[0]
        if len(self.filename) == 0:
            no_file()
            return
        self.ui.filename.setText(self.filename)
        app.processEvents()

        # Read the file
        f1 = open(self.filename, 'r')  # open the file for reading
        data = f1.readlines()  # read the entire file as a list of strings
        f1.close()  # close the file  ... very important

        self.Fourbar = Fourbar()  # create a Truss instance (object)

        t = self.Fourbar  # a shorter name for convenience

        t.ReadFourBarData(data)

        # rpt = t.GenerateReport()

        # put the report in the large TextBox
        # self.ui.textEdit_Report.setText(rpt)

        # fill the small text boxes
        # self.ui.lineEdit_a0.setText(t.longestLink.name)
        # self.ui.lineEdit_a.setText(t.longestLink.node1.name)
        # self.ui.lineEdit_StartAngle.setText(t.longestLink.node2.name)
        # self.ui.lineEdit_EndAngle.setText('{:8.2f}'.format(t.longest))
        # self.ui.lineEdit_b0.setText(t.longestLink.node1.name)
        # self.ui.lineEdit_b.setText(t.longestLink.node1.name)
        # self.ui.MouseLocation.setText(t.longestLink.node1.name)

        #draw the picture
        # this makes sure the window of the GL is slightly bigger to allow the picture of the truss to be visible
        [xmin, xmax, ymin, ymax] = self.Fourbar.window
        dx = xmax - xmin
        dy = ymax - ymin
        xmin -= 0.05*dx
        xmax += 0.05*dx
        ymin -= 0.05*dy
        ymax += 0.05*dy
        self.glwindow1.setViewSize(xmin,xmax,ymin,ymax, allowDistortion=False)
        app.processEvents()
        # self.glwindow1.glUpdate()

    def ExitApp(self):
        app.exit()

# if no file is presented give message that no file was selected
def no_file():
    msg = QMessageBox()
    msg.setText('There was no file selected')
    msg.setWindowTitle("No File")
    retval = msg.exec_()
    return None

# if file is no valid type display message that file is bad
def bad_file():
    msg = QMessageBox()
    msg.setText('Unable to process the selected file')
    msg.setWindowTitle("Bad File")
    retval = msg.exec_()
    return None


if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    main_win = main_window()

    # if a filename exists at the beginning of the program .. open it
    # ... to save time in the debugging cycle
    name = main_win.filename
    if name is not None:
        main_win.GetFourbar(name=main_win.filename)

    sys.exit(app.exec_())
