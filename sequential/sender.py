import asyncio
from datetime import datetime
from typing import Callable

from bytes2bits import bytes2bits
from datastructs import Trit


def send_trit(trit: Trit, state: Callable[[bool], None]):
    CODES = ((LOW, HIGH), (HIGH, LOW), (HIGH, HIGH))
    code = CODES[trit.value]
    for signal in code:
        state(signal)


LOW = False
HIGH = True


class TritpackSender:
    def __init__(
        self,
        change_out_signal_state: Callable[[bool], None],
        freq: float,
    ):
        # init instance
        self.change_out_signal_state = change_out_signal_state
        self.window = 1 / freq

        # prepare state
        change_out_signal_state(LOW)
        self.last_sent = datetime.now()

    async def send(self, packet: bytes):
        # assert carring signal is now set to LOW
        # ensure two windows with LOW signal
        await asyncio.sleep(2 * self.window - (datetime.now() - self.last_sent).seconds)

        # convert bits to trits using inforamtional redundancy for validation
        bits = bytes2bits(packet)
        trits = [] * len(bits)

        # ensure exiting with correct state
        self.change_out_signal_state(LOW)
        self.last_sent = datetime.now()
