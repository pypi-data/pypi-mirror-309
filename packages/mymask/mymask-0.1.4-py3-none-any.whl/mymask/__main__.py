from mymask.app import InteractiveSpectrumMaskApp
from PyQt5.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    main_window = InteractiveSpectrumMaskApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()