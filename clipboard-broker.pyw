import sys
import pyperclip
import keyboard
import time
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal
import dialog

class MainWindow(QMainWindow,dialog.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.hotkeys.addItems(['ctrl+j','ctrl+o','ctrl+k','ctrl+m','Ctrl+L'])
        self.setWindowTitle("Clipboard➔"+"DeepL")
        self.clip_monitor=ClipboardMonitor()
        self.clip_monitor.start()
        self.clip_monitor.clipboard_changed.connect(self.on_clipboard_changed)

    def on_clipboard_changed(self,data):
        self.activateWindow()
        self.clipboard.setFocus()
        self.clipboard.setPlainText(data)
        self.clipboard.selectAll()
        param = self.hotkeys.currentText()
        keyboard.press(param)
        keyboard.call_later(keyboard.release, (str(param),), delay=0.8)

class ClipboardMonitor(QtCore.QThread):
    clipboard_changed = pyqtSignal(object)
    def __init__(self, parent=None, **kargs):
        QtCore.QThread.__init__ (self, parent = None)
        self.setParent(parent)
    def run(self):
        clipboard = pyperclip.paste()
        while(True):
            time.sleep(0.1)
            value = pyperclip.paste()
            if clipboard  == value:
                continue
            else:
                clipboard = value
                self.clipboard_changed.emit(value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()