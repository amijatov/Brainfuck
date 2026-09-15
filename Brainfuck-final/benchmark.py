#!/usr/bin/env python3
"""Benchmark fuer den optimierenden Brainfuck-Interpreter.

Gemessen wird ein einzelnes Programm in mehreren Konfigurationen. Neben der
unoptimierten Baseline und der vollen Optimierung wird jeweils genau eine
Optimierung abgeschaltet. Der Vergleich der Zeilen zeigt damit, was die
einzelne Optimierung beitraegt.

Die Laufzeit ist ein Durchschnitt. Die Uhr wird einmal vor dem ersten und
einmal nach dem letzten Durchlauf gelesen, das Ergebnis durch die Anzahl der
Durchläufe geteilt. Dadurch liefern auch sehr kurze Programme brauchbare
Werte.

Aufruf:

    python3 benchmark.py                        Einstellungen aus dem Abschnitt Argumente
    python3 benchmark.py benchmarks/Life.b      anderes Programm messen
    python3 benchmark.py benchmarks/Life.b 20   mit 20 Durchlaeufen
"""

import io
import os
import signal
import sys
import time

ORDNER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ORDNER)

from interpreter import run
from optimizer import PASSES
from pipeline import to_bytecode


# ============================== Argumente ==================================
# Diese Werte gelten, solange sie nicht auf der Kommandozeile überschrieben
# werden.

PROGRAMM = "benchmarks/optimierungstest2.b"   # zu messende Brainfuck-Datei
WIEDERHOLUNGEN = 1000                 # Durchlaeufe je Konfiguration
ZEITLIMIT = 0                             # Sekunden je Konfiguration, 0 = keins
BANDGROESSE = 30000                          # Bandgroesse des Interpreters

# Das Zeitlimit gilt einmal fuer die Uebersetzung und einmal fuer alle
# Durchlaeufe einer Konfiguration zusammen. Wird es waehrend der Durchlaeufe
# erreicht, zaehlt der Durchschnitt der bereits beendeten Durchlaeufe.
# ===========================================================================


class Zeitlimit(Exception):
    """Wird ausgeloest, wenn eine Messung das Zeitlimit erreicht."""


class zeitgrenze:
    """Bricht den umschlossenen Block nach ``sekunden`` ab. 0 schaltet ab."""

    def __init__(self, sekunden):
        self.sekunden = sekunden if hasattr(signal, "SIGALRM") else 0

    def __enter__(self):
        if self.sekunden > 0:
            self.vorherige = signal.signal(
                signal.SIGALRM, lambda nummer, rahmen: (_ for _ in ()).throw(Zeitlimit()))
            signal.setitimer(signal.ITIMER_REAL, self.sekunden)
        return self

    def __exit__(self, *fehlerinfo):
        if self.sekunden > 0:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, self.vorherige)
        return False


def konfigurationen():
    """Liefert die zu messenden Konfigurationen als (Name, Argumente)."""
    liste = [
        ("roh", dict(optimize=False, coalesce=False)),
        ("voll", dict(optimize=True, coalesce=True, passes=None)),
        ("ohne coalesce", dict(optimize=True, coalesce=False, passes=None)),
    ]
    for weggelassen in PASSES:
        uebrige = [name for name in PASSES if name != weggelassen]
        liste.append((f"ohne {weggelassen}",
                      dict(optimize=True, coalesce=True, passes=uebrige)))
    return liste


def uebersetze(quelltext, argumente):
    """Uebersetzt den Quelltext und misst die dafuer benoetigte Zeit."""
    beginn = time.perf_counter()
    try:
        with zeitgrenze(ZEITLIMIT):
            bytecode = to_bytecode(quelltext, **argumente)
    except Zeitlimit:
        return None, ZEITLIMIT
    return bytecode, time.perf_counter() - beginn


def miss_laufzeit(bytecode, eingabe):
    """Fuehrt den Bytecode mehrfach aus und liefert die mittlere Laufzeit.

    Die Uhr wird nur einmal vor dem ersten und einmal nach dem letzten
    Durchlauf gelesen. Zurueckgegeben werden mittlere Laufzeit, Ausgabe des
    letzten vollstaendigen Durchlaufs und ein Status.
    """
    fertig = 0
    letzte = None
    beginn = time.perf_counter()
    try:
        with zeitgrenze(ZEITLIMIT):
            for _ in range(WIEDERHOLUNGEN):
                puffer = io.BytesIO()
                run(bytecode, tape_size=BANDGROESSE,
                    inp=io.BytesIO(eingabe), out=puffer)
                fertig += 1
                letzte = puffer
    except Zeitlimit:
        ende = time.perf_counter()
        if fertig == 0:
            return None, b"", "Zeitlimit"
        return ((ende - beginn) / fertig, letzte.getvalue(),
                f"Zeitlimit nach {fertig} von {WIEDERHOLUNGEN}")
    except RuntimeError as fehler:
        return None, b"", str(fehler)
    ende = time.perf_counter()
    return (ende - beginn) / fertig, letzte.getvalue(), "ok"


def lies_nebendatei(pfad, endung):
    """Liest ``<name><endung>`` neben dem Programm oder liefert None."""
    nachbar = os.path.splitext(pfad)[0] + endung
    if not os.path.exists(nachbar):
        return None
    with open(nachbar, "rb") as datei:
        return datei.read()


def main():
    global PROGRAMM, WIEDERHOLUNGEN

    if len(sys.argv) > 1:
        if sys.argv[1] in ("-h", "--help"):
            print(__doc__)
            return
        PROGRAMM = sys.argv[1]
    if len(sys.argv) > 2:
        WIEDERHOLUNGEN = int(sys.argv[2])

    pfad = PROGRAMM if os.path.isabs(PROGRAMM) else os.path.join(ORDNER, PROGRAMM)
    if not os.path.exists(pfad):
        print(f"Datei nicht gefunden: {pfad}")
        return

    with open(pfad, encoding="utf-8", errors="replace") as datei:
        quelltext = datei.read()
    eingabe = lies_nebendatei(pfad, ".in") or b""
    referenzdatei = lies_nebendatei(pfad, ".out")

    print(f"{os.path.basename(pfad)}  "
          f"{len(quelltext)} Zeichen Quelltext, {len(eingabe)} Byte Eingabe")
    print(f"{WIEDERHOLUNGEN} Durchlaeufe je Konfiguration, "
          f"Zeitlimit {ZEITLIMIT:g} s, Band {BANDGROESSE} Zellen")
    print()
    print(f"{'Konfiguration':<16}{'Instr.':>10}{'vs roh':>9}"
          f"{'Uebers. [s]':>13}{'Lauf [s]':>13}{'Speedup':>9}  Status")
    print("-" * 82)

    instr_roh = None
    zeit_roh = None
    # Verglichen wird gegen die erste Konfiguration, die vollstaendig
    # durchlief. Das ist im Regelfall roh; laeuft roh in das Zeitlimit,
    # uebernimmt die naechste vollstaendige Konfiguration diese Rolle.
    vergleich = None
    vergleichsname = None

    for name, argumente in konfigurationen():
        bytecode, uebersetzungszeit = uebersetze(quelltext, argumente)
        if bytecode is None:
            print(f"{name:<16}{'-':>10}{'-':>9}{'>' + format(ZEITLIMIT, '.3f'):>13}"
                  f"{'-':>13}{'-':>9}  Uebersetzung ueber Zeitlimit")
            continue

        laufzeit, ausgabe, status = miss_laufzeit(bytecode, eingabe)

        if name == "roh":
            instr_roh, zeit_roh = len(bytecode), laufzeit

        if laufzeit is not None:
            if vergleich is None:
                vergleich, vergleichsname = ausgabe, name
            elif ausgabe != vergleich:
                status = f"AUSGABE WEICHT VON {vergleichsname} AB"

        anteil = "-" if not instr_roh else f"{100.0 * len(bytecode) / instr_roh:.1f} %"
        lauf = "-" if laufzeit is None else f"{laufzeit:.6f}"
        if laufzeit and zeit_roh:
            speedup = f"{zeit_roh / laufzeit:.1f}x"
        else:
            speedup = "-"

        print(f"{name:<16}{len(bytecode):>10}{anteil:>9}"
              f"{uebersetzungszeit:>13.3f}{lauf:>13}{speedup:>9}  {status}")

    print()
    if referenzdatei is None:
        print("Keine Referenzdatei zum Vergleich vorhanden.")
    elif vergleich is None:
        print("Referenzdatei nicht geprueft, keine Konfiguration lief vollstaendig durch.")
    elif vergleich == referenzdatei:
        print(f"Ausgabe stimmt mit der Referenzdatei ueberein "
              f"({len(vergleich)} Byte, verglichen mit {vergleichsname}).")
    else:
        print(f"ACHTUNG Ausgabe weicht von der Referenzdatei ab. "
              f"{vergleichsname} erzeugt {len(vergleich)} Byte, "
              f"Datei hat {len(referenzdatei)} Byte.")

    print()
    print("roh           = ohne Aggregation im Parser und ohne Optimierungspaesse")
    print("voll          = alle Optimierungen eingeschaltet")
    print("ohne coalesce = Aggregation im Parser abgeschaltet")
    print("ohne X        = Optimierungspass X abgeschaltet")
    print("Speedup       = Laufzeit roh geteilt durch Laufzeit dieser Konfiguration")


if __name__ == "__main__":
    main()
