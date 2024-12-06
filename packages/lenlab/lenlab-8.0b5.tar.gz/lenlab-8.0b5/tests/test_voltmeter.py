from lenlab.launchpad.protocol import pack
from lenlab.launchpad.terminal import Terminal
from lenlab.spy import Spy


def test_voltmeter(firmware, terminal: Terminal):
    print("")

    spy = Spy(terminal.reply)
    terminal.write(pack(b"vstrt"))
    reply = spy.run_until_single_arg(timeout=1500)
    assert reply is not None
    assert reply[0:2] == b"Lv"
    assert reply[4:8] == b"next"
    print(reply)

    for i in range(2):
        spy = Spy(terminal.reply)
        terminal.write(pack(b"vnext"))
        reply = spy.run_until_single_arg(timeout=1500)
        assert reply is not None, str(i)
        assert reply[0:2] == b"Lv"
        assert reply[4:8] == b"next"
        print(reply)

    spy = Spy(terminal.reply)
    terminal.write(pack(b"vstop"))
    reply = spy.run_until_single_arg(timeout=1500)
    assert reply is not None
    assert reply[0:2] == b"Lv"
    assert reply[4:8] == b"last"
    print(reply)
