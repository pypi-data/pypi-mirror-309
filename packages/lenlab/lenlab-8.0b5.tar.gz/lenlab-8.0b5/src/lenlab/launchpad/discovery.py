from importlib import metadata

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo

from ..message import Message
from ..singleshot import SingleShotTimer
from .launchpad import find_vid_pid
from .protocol import pack
from .terminal import Terminal


class Probe(QObject):
    result = Signal(Terminal)
    error = Signal(Message)

    def __init__(self, terminal: Terminal):
        super().__init__()

        self.terminal = terminal
        self.unsuccessful = False
        self.timer = SingleShotTimer(self.on_timeout)

    def start(self) -> None:
        self.terminal.error.connect(self.on_error)
        self.terminal.reply.connect(self.on_reply)

        # on_error handles the error case
        if self.terminal.open():
            self.timer.start()
            self.terminal.set_baud_rate(1_000_000)
            self.terminal.write(pack(b"knock"))

    @Slot(Message)
    def on_error(self, error: Message) -> None:
        self.timer.stop()
        self.terminal.close()
        # a terminal might send more than one error
        self.unsuccessful = True
        self.error.emit(error)

    @Slot(bytes)
    def on_reply(self, reply: bytes) -> None:
        self.timer.stop()

        if reply[0:4] == b"Lk\x00\x00":
            version = "8." + reply[4:8].strip(b"\x00").decode("ascii", errors="strict")
            if version == metadata.version("lenlab"):
                self.terminal.error.disconnect(self.on_error)
                self.terminal.reply.disconnect(self.on_reply)
                self.result.emit(self.terminal)
            else:
                self.terminal.close()
                self.unsuccessful = True
                self.error.emit(InvalidFirmwareVersion(version, metadata.version("lenlab")))
        else:
            self.terminal.close()
            self.unsuccessful = True
            self.error.emit(UnexpectedReply(self.terminal.port_name, reply))

    @Slot()
    def on_timeout(self) -> None:
        self.terminal.close()
        self.unsuccessful = True
        self.error.emit(Timeout(self.terminal.port_name))

    def cancel(self) -> None:
        if not self.unsuccessful:
            self.timer.stop()
            self.terminal.close()
            self.unsuccessful = True
            self.error.emit(Cancelled(self.terminal.port_name))


class Discovery(QObject):
    message = Signal(Message)
    result = Signal(Terminal)
    error = Signal(Message)

    probes: list[Probe]

    def discover(self):
        port_infos = QSerialPortInfo.availablePorts()
        matches = find_vid_pid(port_infos)
        if not matches:
            self.error.emit(NoLaunchpad())
            return

        self.start([Probe(Terminal(QSerialPort(port_info))) for port_info in matches])

    def start(self, probes: list[Probe]) -> None:
        self.probes = probes

        for probe in self.probes:
            probe.result.connect(self.result)
            probe.result.connect(self.on_result)
            probe.error.connect(self.message)
            probe.error.connect(self.on_error)
            probe.start()

    @Slot(Message)
    def on_result(self, result: Terminal) -> None:
        for probe in self.probes:
            if probe is not self.sender():
                probe.cancel()

    @Slot(Message)
    def on_error(self, error: Message) -> None:
        if all(probe.unsuccessful for probe in self.probes):
            self.error.emit(Nothing())


class InvalidFirmwareVersion(Message):
    english = """Invalid firmware version: {0}
        This Lenlab requires version {1}.
        Please write the current version to the Launchpad with the Programmer."""
    german = """Ungültige Firmware-Version: {0}
        Dieses Lenlab benötigt Version {1}.
        Bitte die aktuelle Version mit dem Programmierer auf das Launchpad schreiben."""


class UnexpectedReply(Message):
    english = "Unexpected reply on {0}: {1}"
    german = "Unerwartete Antwort auf {0}: {1}"


class Timeout(Message):
    english = "Probe timeout on {0}"
    german = "Probezeit abgelaufen auf {0}"


class NoLaunchpad(Message):
    english = "No Launchpad found"
    german = "Kein Launchpad gefunden"


class Cancelled(Message):
    english = "Cancelled on {0}"
    german = "Abgebrochen auf {0}"


class Nothing(Message):
    english = "Nothing found"
    german = "Nichts gefunden"
