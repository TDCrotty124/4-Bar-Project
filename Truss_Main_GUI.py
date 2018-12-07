import sys
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtWidgets import QFileDialog,QMessageBox
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

from Truss_Design_ui import Ui_Dialog
from Truss_Class import Truss

class main_window(QDialog):
    def __init__(self):
        super(main_window,self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.assign_widgets()

        #define two data items
        self.truss = None
        self.filename = None
        # self.filename =

        self.show()

    def assign_widgets(self):
        self.ui.pushButton_2.clicked.connect(self.ExitApp)
        self.ui.pushButton.clicked.connect(self.GetTruss)

    def GetTruss(self):

        # get the filename using the OPEN dialog
        self.filename = QFileDialog.getOpenFileName()[0]
        if len(self.filename)==0:
            no_file()
            return
        self.ui.textEdit_filename.setText(self.filename)
        app.processEvents()


        # Read the file
        f1 = open(self.filename, 'r')  # open the file for reading
        data = f1.readlines()  # read the entire file as a list of strings
        f1.close()  # close the file  ... very important

        self.truss = Truss()    # create a wing instance (object)

        t = self.truss  # a shorter name for convenience

        t.ReadTrussData(data)

        rpt = t.GenerateReport()

        #put the report in the large TextBox
        self.ui.textEdit_DesignReport.setText(rpt)

        # Fill the small text boxes
        self.ui.lineEdit_linkname.setText('{:.2f}'.format(self.truss.linkname))
        self.ui.lineEdit_Node1Name.setText('{:.2f}'.format(self.truss.Node1Name))
        self.ui.lineEdit_Node2Name.setText('{:.2f}'.format(self.truss.Node2Name))
        self.ui.lineEdit_LinkLength.setText('{:.2f}'.format(self.truss.LinkLength))



    def ExitApp(self):
        app.exit()

def no_file():
    msg = QMessageBox()
    msg.setText('There was no file selected')
    msg.setWindowTitle("No File")
    retval = msg.exec_()
    return None

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
    sys.exit(app.exec_())

    #if a filename exists at the beginning of the program..open it
    #...to save time in the debugging cycle
    # name = main_win.filename
    # if name is not None:
    #     main_win.GetTruss(name = main_win.filename)

    sys.exit(app.exec_())


