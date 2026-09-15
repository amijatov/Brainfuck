from dataclasses import dataclass


TRACKED_CELL_LIMIT = 512


@dataclass(frozen=True, slots=True)
class Interval:

    lo: int
    hi: int | None

    def __post_init__(self):
        """Prüft, ob die Intervallgrenzen gültig sind."""
        if self.hi is not None and self.lo > self.hi:
            raise ValueError(f"leeres Intervall [{self.lo}, {self.hi}]")

    def is_const(self):
        """Prüft, ob das Intervall genau einen Wert enthält."""
        return self.hi is not None and self.lo == self.hi

    def is_zero(self):
        """Prüft, ob das Intervall nur null enthält."""
        return self.lo == 0 and self.hi == 0

    def width(self):
        """Gibt die Intervallbreite zurück, sofern sie begrenzt ist."""
        return None if self.hi is None else self.hi - self.lo

    def without_zero(self):
        """Schließt null aus dem Intervall aus."""
        if self.hi == 0:
            raise ValueError("ein Nullintervall enthält keinen Nonzero-Wert")
        return Interval(max(1, self.lo), self.hi)

    def join(self, other):
        """Bildet das kleinste Intervall, das beide Intervalle umfasst."""
        hi = None if self.hi is None or other.hi is None else max(self.hi, other.hi)
        return Interval(min(self.lo, other.lo), hi)

    def leq(self, other):
        """Prüft, ob dieses Intervall im anderen enthalten ist."""
        if self.lo < other.lo:
            return False
        if other.hi is None:
            return True
        return self.hi is not None and self.hi <= other.hi

    def widen(self, other, top_hi, bottom_lo=0):
        """Erweitert wachsende Intervallgrenzen auf vorgegebene Grenzwerte."""
        lo = self.lo if other.lo >= self.lo else bottom_lo
        if self.hi is None:
            hi = None
        elif other.hi is not None and other.hi <= self.hi:
            hi = self.hi
        else:
            hi = top_hi
        return Interval(lo, hi)

    def __repr__(self):
        """Gibt die Intervallgrenzen als Text zurück."""
        return f"[{self.lo},{'inf' if self.hi is None else self.hi}]"


CELL_TOP = Interval(0, 255)
ZERO = Interval(0, 0)


def const_interval(value):
    """Erzeugt ein Intervall für einen einzelnen Bytewert."""
    value %= 256
    return Interval(value, value)


def wrap_add(interval, amount):
    """Addiert eine Zahl zu einem Byteintervall modulo 256."""
    width = interval.width()
    if width is None or width >= 255:
        return CELL_TOP
    lo = interval.lo + amount
    hi = interval.hi + amount
    if lo // 256 != hi // 256:
        return CELL_TOP
    return Interval(lo % 256, hi % 256)


def wrap_add_intervals(left, right):
    """Addiert zwei Byteintervalle modulo 256."""
    if left.width() is None or right.width() is None:
        return CELL_TOP
    lo = left.lo + right.lo
    hi = left.hi + right.hi
    if hi - lo >= 255 or lo // 256 != hi // 256:
        return CELL_TOP
    return Interval(lo % 256, hi % 256)


def wrap_multiply(interval, factor):
    """Multipliziert ein Byteintervall mit einem Faktor modulo 256."""
    factor %= 256
    if factor == 0:
        return ZERO
    if interval.width() is None:
        return CELL_TOP
    lo = factor * interval.lo
    hi = factor * interval.hi
    if hi - lo >= 255 or lo // 256 != hi // 256:
        return CELL_TOP
    return Interval(lo % 256, hi % 256)


class State:

    __slots__ = ("ptr", "cells", "default", "cur")

    def __init__(self, ptr, cells, default, cur=None):
        """Speichert die Zeigerposition und die Zellinformationen."""
        self.ptr = ptr
        self.cells = cells
        self.default = default
        self.cur = cur

    @classmethod
    def initial(cls):
        """Erzeugt den Anfangszustand mit Zeiger und Zellwerten bei null."""
        return cls(Interval(0, 0), {}, ZERO, ZERO)

    @classmethod
    def unknown(cls):
        """Erzeugt einen Zustand mit unbekannter Zeigerposition und Zellwerten."""
        return cls(Interval(0, None), {}, CELL_TOP, None)

    def copy(self):
        """Erzeugt eine Kopie des Zustands."""
        return State(self.ptr, dict(self.cells), self.default, self.cur)

    def _indices(self, offset):
        """Berechnet die möglichen absoluten Adressen eines relativen Offsets."""
        lo = self.ptr.lo + offset
        hi = None if self.ptr.hi is None else self.ptr.hi + offset
        return lo, hi

    def read_at(self, offset):
        """Liest den möglichen Zellwert an einem relativen Offset."""
        if offset == 0 and self.cur is not None:
            return self.cur

        lo, hi = self._indices(offset)
        if hi is not None and lo == hi:
            return self.cells.get(lo, self.default)

        result = self.default
        for index, value in self.cells.items():
            if index >= lo and (hi is None or index <= hi):
                result = result.join(value)
        return result

    def write_at(self, offset, value):
        """Aktualisiert die möglichen Zellwerte an einem relativen Offset."""
        if offset == 0:
            self.cur = value

        lo, hi = self._indices(offset)
        if hi is not None and lo == hi:
            if value == self.default:
                self.cells.pop(lo, None)
            else:
                self.cells[lo] = value
            return

        for index in list(self.cells):
            if index >= lo and (hi is None or index <= hi):
                self.cells[index] = self.cells[index].join(value)

        self.default = self.default.join(value)
        for index in [i for i, v in self.cells.items() if v == self.default]:
            self.cells.pop(index, None)

    def read(self):
        """Liest den möglichen Wert der aktuellen Zelle."""
        return self.read_at(0)

    def write(self, value):
        """Aktualisiert den möglichen Wert der aktuellen Zelle."""
        self.write_at(0, value)

    def move(self, amount):
        """Verschiebt die mögliche Zeigerposition."""
        if amount == 0:
            return

        lo = self.ptr.lo + amount
        hi = None if self.ptr.hi is None else self.ptr.hi + amount

        if hi is not None and hi < 0:
            self.ptr = Interval(0, None)
        else:
            self.ptr = Interval(max(0, lo), hi)
        self.cur = None

    def forget_pointer(self, lo, hi):
        """Setzt neue Zeigergrenzen und verwirft die aktuelle Zellinformation."""
        lower = 0 if lo is None else max(0, lo)
        upper = None if hi is None else max(lower, hi)
        self.ptr = Interval(lower, upper)
        self.cur = None

    def _combine(self, other, cell_operation, pointer_operation):
        """Verknüpft zwei Zustände mit den angegebenen Intervalloperationen."""
        default = cell_operation(self.default, other.default)
        cells = {}
        for index in self.cells.keys() | other.cells.keys():
            left = self.cells.get(index, self.default)
            right = other.cells.get(index, other.default)
            value = cell_operation(left, right)
            if value != default:
                cells[index] = value

        if self.cur is None or other.cur is None:
            cur = None
        else:
            cur = cell_operation(self.cur, other.cur)

        return State(pointer_operation(self.ptr, other.ptr), cells, default, cur)

    def join(self, other):
        """Fasst die Möglichkeiten beider Zustände zusammen."""
        return self._combine(other, Interval.join, Interval.join)

    def widen(self, other):
        """Vergröbert wachsende Zustandsinformationen für die Schleifenanalyse."""
        result = self._combine(
            other,
            lambda left, right: left.widen(right, 255),
            lambda left, right: left.widen(right, None, 0),
        )

        if len(result.cells) > TRACKED_CELL_LIMIT:
            merged = result.default
            for value in result.cells.values():
                merged = merged.join(value)
            result = State(result.ptr, {}, merged, result.cur)
        return result

    def leq(self, other):
        """Prüft, ob dieser Zustand mindestens so genau wie der andere ist."""
        if not self.ptr.leq(other.ptr) or not self.default.leq(other.default):
            return False

        for index in self.cells.keys() | other.cells.keys():
            left = self.cells.get(index, self.default)
            right = other.cells.get(index, other.default)
            if not left.leq(right):
                return False

        if other.cur is not None:
            if self.cur is None or not self.cur.leq(other.cur):
                return False
        return True

    def __eq__(self, other):
        """Prüft, ob beide Zustände übereinstimmen."""
        return (
            isinstance(other, State)
            and self.ptr == other.ptr
            and self.cells == other.cells
            and self.default == other.default
            and self.cur == other.cur
        )

    def __repr__(self):
        """Gibt die Zustandsinformationen als Text zurück."""
        return (
            f"State(ptr={self.ptr}, cur={self.cur}, "
            f"cells={self.cells}, default={self.default})"
        )
