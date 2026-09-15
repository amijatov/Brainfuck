# Optimierender Brainfuck-Interpreter

Der Interpreter liest Brainfuck-Quelltext, optimiert eine baumförmige
Zwischenrepräsentation und führt den daraus erzeugten Bytecode aus.
Die Zellen enthalten Bytewerte; gerechnet wird modulo 256.

## Voraussetzungen

- Python **3.10 oder neuer**.
- Nur die Python-Standardbibliothek; keine Installation mit `pip` erforderlich.

## Ausführen

Alle Befehle werden im Projektverzeichnis ausgeführt:

```sh
python3 main.py DATEI
```

Ein mitgeliefertes Beispiel starten:

```sh
python3 main.py test.bf
```

Programme mit Eingabedaten können diese über die Standardeingabe erhalten:

```sh
python3 main.py Tests/benchmarks/utm.b < Tests/benchmarks/utm.in
```

Weitere Beispielprogramme liegen in `Tests/benchmarks/`.

## Optionen

| Option | Wirkung |
| --- | --- |
| `--no-opt` | Deaktiviert die Optimierungspässe. Die Befehlsaggregation beim Parsen bleibt aktiv. |
| `--no-coalesce` | Deaktiviert die Befehlsaggregation beim Parsen. |
| `--show-ir` | Zeigt die Baum-IR an und beendet das Programm ohne Ausführung. |
| `--show-bytecode` | Zeigt den flachen Bytecode an und beendet das Programm ohne Ausführung. |
| `--tape-size N` | Legt die Bandgröße auf `N` Zellen fest; `N` muss positiv sein. Standard: 30.000. |
| `-h`, `--help` | Zeigt die Kommandozeilenhilfe an. |

Für einen Vergleich ohne Optimierungspässe und ohne Befehlsaggregation
werden beide Optionen kombiniert:

```sh
python3 main.py test.bf --no-opt --no-coalesce
```
