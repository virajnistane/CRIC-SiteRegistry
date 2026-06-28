from PyQt6.QtWidgets import QApplication

from desktop.widgets.main_window import MainWindow


def test_main_window_constructs(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    assert window.windowTitle() == "CRIC Site Registry Desktop Client"