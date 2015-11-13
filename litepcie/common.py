from litex.gen import *

from litex.soc.interconnect.stream import *
from litex.soc.interconnect.stream_packet import *

KB = 1024
MB = 1024*KB
GB = 1024*MB


def reverse_bytes(signal):
    n = (len(signal)+7)//8
    r = []
    for i in reversed(range(n)):
        r.append(signal[i*8:min((i+1)*8, len(signal))])
    return Cat(*r)


def reverse_bits(signal):
    n = len(signal)
    r = []
    for i in reversed(range(n)):
        r.append(signal[i])
    return Cat(*r)


@ResetInserter()
@CEInserter()
class Counter(Module):
    def __init__(self, *args, increment=1, **kwargs):
        self.value = Signal(*args, **kwargs)
        self.width = len(self.value)
        self.sync += self.value.eq(self.value+increment)


def get_bar_mask(size):
            mask = 0
            found = 0
            for i in range(32):
                if size%2:
                    found = 1
                if found:
                    mask |= (1 << i)
                size = size >> 1
            return mask

def phy_layout(dw):
    layout = [
        ("dat", dw),
        ("be",  dw//8)
    ]
    return EndpointDescription(layout, packetized=True)


def request_layout(dw):
    layout = [
            ("we",       1),
            ("adr",     32),
            ("len",     10),
            ("req_id",  16),
            ("tag",      8),
            ("dat",     dw),
            ("channel",  8),  # for routing
            ("user_id",  8)   # for packet identification
    ]
    return EndpointDescription(layout, packetized=True)


def completion_layout(dw):
    layout = [
            ("adr",    32),
            ("len",    10),
            ("last",    1),
            ("req_id", 16),
            ("cmp_id", 16),
            ("err",     1),
            ("tag",     8),
            ("dat",     dw),
            ("channel",  8),  # for routing
            ("user_id",  8)   # for packet identification
    ]
    return EndpointDescription(layout, packetized=True)


def interrupt_layout():
    return [("dat", 8)]


def dma_layout(dw):
    layout = [("data", dw)]
    return EndpointDescription(layout, packetized=True)
