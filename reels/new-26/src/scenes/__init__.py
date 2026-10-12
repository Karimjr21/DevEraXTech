from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Reel:
    n: int
    slug: str
    dur: float
    draw: Callable
    audio: Callable
    meta: dict
    room: float = 0.18
    grain: int = 6
    qc: list = field(default_factory=list)
    push: float = 0.0  # seconds of slow camera push-in on the hook (0 = none)


REELS = {}


def reel(n, slug, dur, audio, meta, **kw):
    def deco(fn):
        REELS[n] = Reel(n, slug, dur, fn, audio, meta, **kw)
        return fn
    return deco


from . import a, b, c  # noqa: E402,F401  (registers the reels)
