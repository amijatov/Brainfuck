# ============================================================
# Zweites Testprogramm fuer den optimierenden Brainfuck Interpreter
# Schwerpunkt: tiefe Verschachtelung und unbalancierte Schleifen und toter Code
# Alle Ausgabebytes sind druckbares ASCII oder Zeilenumbruch
# Synthetisch erzeugt mit festem Seed 20260915
# Jeder Block wurde einzeln geprueft: terminiert und Zeiger kehrt zurueck
# Band bleibt genullt und keine Bandgrenze verletzt und Ausgabe druckbar
# ============================================================

# Sicherheitsabstand nach rechts fuer Linksbewegungen
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# ========== Abschnitt 1 ==========
# Toter Speicher hinter einer Ausgabe
++++++[->+++++++++++<]>.[-]<>++++++<>[-]<
# Suchschleife nach rechts mit Rueckweg ueber Wachposten
+>>+++>+++>+++<<<<[>]>[-]<[<]>>>[-]<[-]<[-]<<[-]
# Ziffern eins bis neun aus einer Zaehlschleife mit Ausgabe im Rumpf
++++++[->++++++++<]+++++++++[>+.<-]>[-]<
# Speicher weit rechts der nie gelesen wird
>>>>++++++<<<<>>>>[-]<<<<
# Wechselnde Richtungen mit Zwischenschleifen
>>+<<[->>[-]<<]>>[-]<<>>><<<
# Nachbarzelle beschrieben und nie gelesen und spaeter geloescht
>++++++<>[-]<
# Array aus 40 Zellen mit Abbau von rechts nach links
+>++++[->++++++++++<]>[->>[>]+[<]<]>>[>]<[[-]<]<<<[-]
# Zeilenumbruch
++++++++++.[-]

# ========== Abschnitt 2 ==========
# Nachbarzelle beschrieben und nie gelesen und spaeter geloescht
>++++++<>[-]<
# Loeschlauf nach rechts ueber eine bekannte Laenge
>+>+>+>+>+<<<<<>[[-]>]<<<<<<
# Toter Speicher vor einer Suchschleife
>++++++<+>+>+<<[>]<<<[-]>[-]>[-]<<>[-]<
# Suchschleife nach rechts mit Rueckweg ueber Wachposten
+>>+++>+++>+++<<<<[>]>[-]<[<]>>>[-]<[-]<[-]<<[-]
# Speicher weit rechts der nie gelesen wird
>>>>++++++<<<<>>>>[-]<<<<
# Zeilenumbruch
++++++++++.[-]

# ========== Abschnitt 3 ==========
# Zwei Zellen beschrieben und nur eine genutzt
>+++++>++++<[-]<>>[-]<<
# Vier Ebenen mit Ziffern aus dem innersten Rumpf
>>>>+++++++++++++++++++++++++++++++++++++++++++++++<<<<++[->++[->++[->++[->+.<]<]<]<]>>>>[-]<<<<
# Speicher weit rechts der nie gelesen wird
>>>>++++++<<<<>>>>[-]<<<<
# Suchschleife nach rechts mit Rueckweg ueber Wachposten
+>>+++>+++>+++<<<<[>]>[-]<[<]>>>[-]<[-]<[-]<<[-]
# Wert ueberschrieben ohne dazwischen gelesen zu werden
>+++++<>+++++++<>[-]<
# Fuenf Ebenen mit druckbaren Zeichen aus dem innersten Rumpf
>>>>>++++++++++++++++++++++++++++++++<<<<<++[->++[->++[->++[->++[->+.<]<]<]<]<]>>>>>[-]<<<<<
# Zeilenumbruch
++++++++++.[-]

# ========== Abschnitt 4 ==========
# Reihe von Speichern die alle tot sind
>+<>>+<<>>>+<<<>[-]<>>[-]<<>>>[-]<<<
# Array aus 160 Zellen ueber Suchschleifen aufbauen und abbauen
+>++++++++[->++++++++++++++++++++<]>[->>[>]+[<]<]>>[>]<[[-]<]<<<[-]
# Wert ueberschrieben ohne dazwischen gelesen zu werden
>+++++<>+++++++<>[-]<
# Fuenf Ebenen mit druckbaren Zeichen aus dem innersten Rumpf
>>>>>++++++++++++++++++++++++++++++++<<<<<++[->++[->++[->++[->++[->+.<]<]<]<]<]>>>>>[-]<<<<<
# Zeilenumbruch
++++++++++.[-]

# ========== Abschnitt 5 ==========
# Ziffern eins bis neun aus einer Zaehlschleife mit Ausgabe im Rumpf
++++++[->++++++++<]+++++++++[>+.<-]>[-]<
# Grossbuchstabe A ueber Multiplikation
+++++[->+++++++++++++<]>.[-]<
# Drei tote Speicher in Folge
>++<>>+++<<>>>++++<<<>[-]<>>[-]<<>>>[-]<<<
# Ergebnis einer Multiplikation nie gelesen
+++++++[->++++++++<]>[-]<
# Loeschlauf nach rechts ueber eine bekannte Laenge
>+>+>+>+>+<<<<<>[[-]>]<<<<<<
# Suchschleife nach rechts mit Rueckweg ueber Wachposten
+>>+++>+++>+++<<<<[>]>[-]<[<]>>>[-]<[-]<[-]<<[-]
# Zeilenumbruch
++++++++++.[-]

# ========== Abschnitt 6 ==========
# Zwei Zellen beschrieben und nur eine genutzt
>+++++>++++<[-]<>>[-]<<
# Sechs Ebenen ohne Ausgabe
++[->++[->++[->++[->++[->++[->+<]<]<]<]<]<]>>>>>>[-]<<<<<<
# Drei tote Speicher in Folge
>++<>>+++<<>>>++++<<<>[-]<>>[-]<<>>>[-]<<<
# Vier Ebenen mit Ziffern aus dem innersten Rumpf
>>>>+++++++++++++++++++++++++++++++++++++++++++++++<<<<++[->++[->++[->++[->+.<]<]<]<]>>>>[-]<<<<
# Array aus 160 Zellen ueber Suchschleifen aufbauen und abbauen
+>++++++++[->++++++++++++++++++++<]>[->>[>]+[<]<]>>[>]<[[-]<]<<<[-]
# Zeilenumbruch
++++++++++.[-]

# ========== Abschnitt 7 ==========
# Loeschlauf nach rechts ueber eine bekannte Laenge
>+>+>+>+>+<<<<<>[[-]>]<<<<<<
# Fuenf Ebenen mit druckbaren Zeichen aus dem innersten Rumpf
>>>>>++++++++++++++++++++++++++++++++<<<<<++[->++[->++[->++[->++[->+.<]<]<]<]<]>>>>>[-]<<<<<
# Array aus 160 Zellen ueber Suchschleifen aufbauen und abbauen
+>++++++++[->++++++++++++++++++++<]>[->>[>]+[<]<]>>[>]<[[-]<]<<<[-]
# Speicher weit rechts der nie gelesen wird
>>>>++++++<<<<>>>>[-]<<<<
# Verschachtelte Multiplikation mit Zwischenspeicher
+++[->++[->+++[->+<]<]<]>>>[-]<<<
# Toter Speicher zwischen zwei Ausgaben
+++++++[->+++++++++++<]>.>+++++++<>[-]<[-]<
# Zeilenumbruch
++++++++++.[-]

# ========== Abschnitt 8 ==========
# Nachbarzelle beschrieben und nie gelesen und spaeter geloescht
>++++++<>[-]<
# Array aus 40 Zellen mit Abbau von rechts nach links
+>++++[->++++++++++<]>[->>[>]+[<]<]>>[>]<[[-]<]<<<[-]
# Wert ueberschrieben ohne dazwischen gelesen zu werden
>+++++<>+++++++<>[-]<
# Loeschlauf nach rechts ueber eine bekannte Laenge
>+>+>+>+>+<<<<<>[[-]>]<<<<<<
# Vier Ebenen mit Ziffern aus dem innersten Rumpf
>>>>+++++++++++++++++++++++++++++++++++++++++++++++<<<<++[->++[->++[->++[->+.<]<]<]<]>>>>[-]<<<<
# Ergebnis einer Multiplikation nie gelesen
+++++++[->++++++++<]>[-]<
# Multiplikationskette ueber vier Zellen
+++[->++>+++>++++<<<]>[-]>[-]>[-]<<<
# Zeilenumbruch
++++++++++.[-]

# ========== Abschnitt 9 ==========
# Reihe von Speichern die alle tot sind
>+<>>+<<>>>+<<<>[-]<>>[-]<<>>>[-]<<<
# Sechs Ebenen ohne Ausgabe
++[->++[->++[->++[->++[->++[->+<]<]<]<]<]<]>>>>>>[-]<<<<<<
# Drei tote Speicher in Folge
>++<>>+++<<>>>++++<<<>[-]<>>[-]<<>>>[-]<<<
# Wechselnde Richtungen mit Zwischenschleifen
>>+<<[->>[-]<<]>>[-]<<>>><<<
# Toter Speicher vor einer Suchschleife
>++++++<+>+>+<<[>]<<<[-]>[-]>[-]<<>[-]<
# Zeilenumbruch
++++++++++.[-]

# ========== Abschnitt 10 ==========
# Speicher weit rechts der nie gelesen wird
>>>>++++++<<<<>>>>[-]<<<<
# Toter Speicher zwischen zwei Ausgaben
+++++++[->+++++++++++<]>.>+++++++<>[-]<[-]<
# Multiplikationskette ueber vier Zellen
+++[->++>+++>++++<<<]>[-]>[-]>[-]<<<
# Ziffern eins bis neun aus einer Zaehlschleife mit Ausgabe im Rumpf
++++++[->++++++++<]+++++++++[>+.<-]>[-]<
# Zeilenumbruch
++++++++++.[-]

# ========== Abschnitt 11 ==========
# Wechselnde Richtungen mit Zwischenschleifen
>>+<<[->>[-]<<]>>[-]<<>>><<<
# Reihe von Speichern die alle tot sind
>+<>>+<<>>>+<<<>[-]<>>[-]<<>>>[-]<<<
# Multiplikationskette ueber vier Zellen
+++[->++>+++>++++<<<]>[-]>[-]>[-]<<<
# Nachbarzelle beschrieben und nie gelesen und spaeter geloescht
>++++++<>[-]<
# Drei tote Speicher in Folge
>++<>>+++<<>>>++++<<<>[-]<>>[-]<<>>>[-]<<<
# Zeilenumbruch
++++++++++.[-]

# ========== Abschnitt 12 ==========
# Grossbuchstabe A ueber Multiplikation
+++++[->+++++++++++++<]>.[-]<
# Array aus 160 Zellen ueber Suchschleifen aufbauen und abbauen
+>++++++++[->++++++++++++++++++++<]>[->>[>]+[<]<]>>[>]<[[-]<]<<<[-]
# Ergebnis einer Multiplikation nie gelesen
+++++++[->++++++++<]>[-]<
# Drei tote Speicher in Folge
>++<>>+++<<>>>++++<<<>[-]<>>[-]<<>>>[-]<<<
# Fuenf Ebenen mit druckbaren Zeichen aus dem innersten Rumpf
>>>>>++++++++++++++++++++++++++++++++<<<<<++[->++[->++[->++[->++[->+.<]<]<]<]<]>>>>>[-]<<<<<
# Ziffern eins bis neun aus einer Zaehlschleife mit Ausgabe im Rumpf
++++++[->++++++++<]+++++++++[>+.<-]>[-]<
# Zeilenumbruch
++++++++++.[-]

# ========== Abschnitt 13 toter Code am Programmende ==========
# Hier kann die Rueckwaertsanalyse ohne Hindernis arbeiten
# Nachbarzelle beschrieben und nie gelesen und spaeter geloescht
>++++++<>[-]<
# Zwei Zellen beschrieben und nur eine genutzt
>+++++>++++<[-]<>>[-]<<
# Wert ueberschrieben ohne dazwischen gelesen zu werden
>+++++<>+++++++<>[-]<
# Ergebnis einer Multiplikation nie gelesen
+++++++[->++++++++<]>[-]<
# Speicher weit rechts der nie gelesen wird
>>>>++++++<<<<>>>>[-]<<<<
# Reihe von Speichern die alle tot sind
>+<>>+<<>>>+<<<>[-]<>>[-]<<>>>[-]<<<
# Toter Speicher hinter einer Ausgabe
++++++[->+++++++++++<]>.[-]<>++++++<>[-]<
# Toter Speicher vor einer Suchschleife
>++++++<+>+>+<<[>]<<<[-]>[-]>[-]<<>[-]<
# Drei tote Speicher in Folge
>++<>>+++<<>>>++++<<<>[-]<>>[-]<<>>>[-]<<<
# Toter Speicher zwischen zwei Ausgaben
+++++++[->+++++++++++<]>.>+++++++<>[-]<[-]<
# Zeilenumbruch
++++++++++.[-]

# Abschluss
# Ausrufezeichen als Endmarkierung
+++++[->++++++<]>+++.[-]<
# Zeilenumbruch
++++++++++.[-]

# Sicherheitsabstand wieder verlassen
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Ende
