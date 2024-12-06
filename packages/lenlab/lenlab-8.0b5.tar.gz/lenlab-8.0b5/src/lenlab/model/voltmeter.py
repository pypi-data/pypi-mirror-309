from itertools import batched

from PySide6.QtCharts import QLineSeries
from PySide6.QtCore import QObject, Slot

from lenlab.launchpad.terminal import Terminal

from ..launchpad.protocol import pack


class Voltmeter(QObject):
    terminal: Terminal

    def __init__(self):
        super().__init__()
        self.ch1 = QLineSeries()
        self.ch1.setName("Channel 1")
        self.ch2 = QLineSeries()
        self.ch2.setName("Channel 2")

        self.offset = 0

        self.running = False
        self.stop_requested = False

    @property
    def channels(self):
        yield self.ch1
        yield self.ch2

    @Slot(Terminal)
    def set_terminal(self, terminal: Terminal):
        self.terminal = terminal
        self.terminal.reply.connect(self.on_reply)

    @Slot()
    def start(self):
        if not self.running:
            self.running = True
            self.stop_requested = False
            if i := self.ch1.count():
                self.offset = self.ch1.at(i - 1).x()
            else:
                self.offset = 0
            self.terminal.write(pack(b"vstrt"))

    @Slot()
    def stop(self):
        if self.running:
            self.stop_requested = True

    @Slot()
    def reset(self):
        if not self.running:
            self.ch1.clear()
            self.ch2.clear()

    @Slot(bytes)
    def on_reply(self, reply: bytes):
        if not reply.startswith(b"Lv"):
            return

        # ask for the next point
        if self.stop_requested:
            if reply[4:8] == b"last":
                self.running = False
            else:
                self.terminal.write(pack(b"vstop"))
        else:
            self.terminal.write(pack(b"vnext"))

        for point in batched(reply[8:], 8):
            time = int.from_bytes(point[:4], byteorder="little") + self.offset
            ch1 = int.from_bytes(point[4:6], byteorder="little") / 2**12 * 3.3
            ch2 = int.from_bytes(point[6:8], byteorder="little") / 2**12 * 3.3
            self.ch1.append(time, ch1)
            self.ch2.append(time, ch2)
