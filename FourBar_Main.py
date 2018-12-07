# standard PyQt5 imports
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtWidgets import QFileDialog, QMessageBox

# standard OpenGL imports
from OpenGL.GLUT import *

from OpenGL_2D_class import gl2D

# the ui created by Designer and pyuic
from FinalProject import Ui_Dialog
from FourBar_Class import Fourbar

# import the Problem Specific class
from DroneCatcher import DroneCatcher

sys._excepthook = sys.excepthook
def exception_hook(exctype,value,traceback):
    print(exctype, value, traceback)
    sys. excepthook(exctype, value, traceback)
    sys.exit(1)

sys.excepthook = exception_hook


class main_window(QDialog):
    def __init__(self):
        super(main_window, self).__init__()
        self.ui = Ui_Dialog()
        # setup the GUI
        self.ui.setupUi(self)

        # define any data (including object variables) your program might need
        self.mydrone = DroneCatcher()
        self.fourbar = Fourbar

        # create and setup the GL window object
        self.setupGLWindows()

        # and define any Widget callbacks (buttons, etc) or other necessary setup
        self.assign_widgets()

        # define two data items
        self.fourbar = None
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


    def eventFilter(self, source, event):  # allow GL to handle Mouse Events
        self.glwindow1.glHandleMouseEvents(event)  # let GL handle the event
        return super(QDialog, self).eventFilter(source, event)


    # Setup OpenGL Drawing and Viewing
    def setupGLWindows(self):  # setup all GL windows
        # send it the   GL Widget     and the drawing Callback function
        self.glwindow1 = gl2D(self.ui.openGLWidget, self.DrawingCallback)

        # set the drawing space:    xmin  xmax  ymin   ymax
        self.glwindow1.setViewSize(-10, 500, -10, 200, allowDistortion=False)

        # Optional: Setup GL Mouse Functionality
        self.ui.openGLWidget.installEventFilter(self)  # to read mouse events
        self.ui.openGLWidget.setMouseTracking(True)  # to enable mouse events

        # OPTIONAL: to display the mouse location  - the name of the TextBox
        self.glwindow1.glMouseDisplayTextBox(self.ui.MouseLocation)



    def DrawingCallback(self):
        # this is what actually draws the picture
        if self.fourbar is not None:
            # Fourbar()
            self.fourbar.Translation()
            self.fourbar.ThreeBarCircle()
            self.fourbar.DrawTrussPicture()

            t = self.fourbar

            # fill the small text boxes
            # initial point A and point B
            self.ui.lineEdit_a0.setText('{:.2f}'.format(t.a0[0]) + " , " + '{:.2f}'.format(t.a0[1]))
            self.ui.lineEdit_b0.setText('{:.2f}'.format(t.a0[0]) + " , " + '{:.2f}'.format(t.a0[1]))

            # Black dots -- different positions as the black dots move
            self.ui.lineEdit_a.setText('{:.2f}'.format(t.ha) + " , " + '{:.2f}'.format(t.ka))
            self.ui.lineEdit_b.setText('{:.2f}'.format(t.hb) + " , " + '{:.2f}'.format(t.kb))

            # Angles that are calculated from fsolve theta3 and theta4
            self.ui.lineEdit_StartAngle.setText('{:.2f}'.format(t.positions[4]))
            self.ui.lineEdit_EndAngle.setText('{:.2f}'.format(t.positions[7]))




        self.glwindow1.glDraggingShowHandles()


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

        self.fourbar = Fourbar()  # create a Truss instance (object)

        t = self.fourbar  # a shorter name for convenience

        t.ReadFourBarData(data)

        # rpt = t.GenerateReport()

        # put the report in the large TextBox
        # self.ui.textEdit_Report.setText(rpt)






        # self.ui.lineEdit_a0.setText('{:.2f}'.format(t.centera))

        # self.ui.lineEdit_linkname.setText('{:.2f}'.format(self.truss.linkname))

        # self.ui.lineEdit_a0.setText(t.longestLink.name)
        # self.ui.lineEdit_a.setText(t.longestLink.node1.name)
        # self.ui.lineEdit_StartAngle.setText(t.longestLink.node2.name)
        # self.ui.lineEdit_EndAngle.setText('{:8.2f}'.format(t.longest))
        # self.ui.lineEdit_b0.setText(t.longestLink.node1.name)
        # self.ui.lineEdit_b.setText(t.longestLink.node1.name)
        # self.ui.MouseLocation.setText(t.longestLink.node1.name)

        #draw the picture
        # this makes sure the window of the GL is slightly bigger to allow the picture of the truss to be visible
        [xmin, xmax, ymin, ymax] = self.fourbar.window
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
