from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

import pyaudio

from apscheduler.schedulers.qt import QtScheduler
from src.ui.main_window import Ui_MainWindow


class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.setWindowFlags(qtc.Qt.WindowCloseButtonHint)
        self.setWindowIcon(qtg.QIcon('./src/ressource/icon.png'))
        self.setFixedSize(130, 60)

        self.offButton.setChecked(True)
        self.onButton.toggled.connect(self.on_off_toggle)
        self.timerSpinBox.setValue(10)

        self.scheduler = QtScheduler()

        self.tray = qtw.QSystemTrayIcon(self)
        self.tray.setIcon(qtg.QIcon('./src/ressource/icon.png'))
        self.tray.setToolTip('BT keep Alive')
        quit_action = qtw.QAction("Exit", self)
        quit_action.triggered.connect(qtw.qApp.quit)
        tray_menu = qtw.QMenu()
        tray_menu.addAction(quit_action)
        self.tray.setContextMenu(tray_menu)
        self.tray.show()
        self.tray.activated.connect(self.on_systray_activated)

    def on_systray_activated(self, reason):
        if self.isVisible() and reason != qtw.QSystemTrayIcon.Context:
            self.hide()
        elif not self.isVisible() and reason != qtw.QSystemTrayIcon.Context:
            self.show()
            self.activateWindow()

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def on_off_toggle(self):
        if self.offButton.isChecked():
            self.timerSpinBox.setEnabled(True)
            self.scheduler.shutdown()
        else:
            self.timerSpinBox.setEnabled(False)
            self.scheduler.add_job(self.play_sound, 'interval',
                                   seconds=self.timerSpinBox.value() * 60)
            self.scheduler.start()

    def play_sound(self):
        p = pyaudio.PyAudio()
        WAVEDATA = ' '
        stream = p.open(format=p.get_format_from_width(
            1), channels=1, rate=11000, output=True)
        stream.write(WAVEDATA)
        stream.stop_stream()
        stream.close()
        p.terminate()


app = qtw.QApplication([])
main_window = MainWindow()
main_window.show()
app.exec_()
