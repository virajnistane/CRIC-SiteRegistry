from __future__ import annotations

import asyncio
import sys

from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop

from desktop.widgets.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()

    with loop:
        loop.create_task(window.load_sites())
        loop.run_forever()


if __name__ == "__main__":
    main()