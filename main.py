import sys
from PyQt5.QtWidgets import QApplication, QWidget
import mainwidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QWidget()
    ui = mainwidget.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())