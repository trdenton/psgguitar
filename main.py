#!/usr/bin/env python
import readline
import rlcompleter
import math
import sys
import re

class Note:

    def mapNoteToNumber(note: str):
        # we only support a0 to a9
        # which is already way too big
        # a4 is 69
        # a0 is 21

        note = note[0].upper() + note[1:]

        base_nums = {}
        base_nums["A"] = 21
        base_nums["B"] = 23
        base_nums["C"] = 12 # c0
        base_nums["D"] = 14
        base_nums["E"] = 16
        base_nums["F"] = 17
        base_nums["G"] = 19

        sharps=note.count("#")
        flats=note.count("b")
        note_mod = sharps - flats

        note = note.replace("#","")
        note = note.replace("b","")

        base = note[0]
        octave = 4
        if len(note) > 1:
            octave = int(note[-1])

        result = base_nums[base] + octave*12 + note_mod
        return result

    def mapNoteToName(num: int):
        # find which octave
        octave = math.floor(num / 12) - 1
        # octave 0 is a,b
        # octave 1 starts at c1
        step = num % 12
        names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        base = names[step]
        return f"{base}{octave}"

    def equalIgnoreOctave(self, other):
        num1 = self.num
        num2 = other.num
        if (num1 - num2)%12 == 0:
            return True
        return False

    def __repr__(self):
        return f"Note({self.name})"

    def addHalfSteps(self, num: int):
        return Note(self.num + num)

    def __eq__(self, other):
        return self.num == other.num

    def __init__(self, name_or_num):
        if type(name_or_num) == str:
            self.name = name_or_num
            self.num = Note.mapNoteToNumber(name_or_num)
        elif type(name_or_num) == int:
            self.num = name_or_num
            self.name = Note.mapNoteToName(name_or_num)

class GuitarString:
    def __init__(self, name: str):
        self.name = name
        self.openNote = Note(name)

    def __repr__(self):
        return f"{self.openNote}"

    # returns a GuitarString
    def fret(self, fret_num):
        note = self.openNote.addHalfSteps(fret_num).name
        result = GuitarString(note)
        return result

    # returns a Note
    def fret_note(self, fret_num):
        return self.openNote.addHalfSteps(fret_num)


class Chord:
    def __init__(self, root, chord_type):
        self.name = f"{root}{chord_type}"
        self.note1 = Note(root)
        if chord_type == "M":
            self.note2 = self.note1.addHalfSteps(4)
            self.note3 = self.note2.addHalfSteps(3)
        if chord_type == "m":
            self.note2 = self.note1.addHalfSteps(3)
            self.note3 = self.note2.addHalfSteps(4)
        if chord_type == "aug":
            self.note2 = self.note1.addHalfSteps(4)
            self.note3 = self.note2.addHalfSteps(4)
        if chord_type == "dim":
            self.note2 = self.note1.addHalfSteps(3)
            self.note3 = self.note2.addHalfSteps(3)

    def contains(self, note):
        if self.note1.equalIgnoreOctave(note):
            return 1
        if self.note2.equalIgnoreOctave(note):
            return 2
        if self.note3.equalIgnoreOctave(note):
            return 3
        return 0

class Guitar:
    def __init__(self, stringNames):
        self.strings = []
        for sn in stringNames:
            self.strings.append(GuitarString(sn))

    def __repr__(self):
        strs = []
        for s in self.strings:
            strs.append(f"{s}")
        return "\n".join(strs)

class PedalSteelGuitar:
    def __init__(self):
        self.num_frets = 24
        notes = ["F#4","D#4","G#4","E4","B4","G#3","F#3","E3","D3","B3"]
        self.guitar = Guitar(notes)
        self.pedals = {}
        self.actuated = {}
        # pedals
        self.pedals["A"] = [0, 0, 0, 0, 2, 0, 0, 0, 0, 2]
        self.pedals["B"] = [0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
        self.pedals["C"] = [0, 0, 0, 2, 2, 0, 0, 0, 0, 0]
        # levers
        self.pedals["D"] = [0,-1, 0, 0, 0, 0, 0, 0,-1, 0]
        self.pedals["E"] = [0, 0, 0,-1, 0, 0, 0,-1, 0, 0]
        self.pedals["F"] = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        self.pedals["G"] = [1, 0, 0, 0, 0, 0, 1, 0, 0, 0]

    def print_fretboard(self, chord=None):
        WHITE_TEXT = "\033[97"  # ANSI code for black foreground
        BLACK_TEXT = "\033[30m"  # ANSI code for black foreground
        BLACK_BACKGROUND = "\033[40m" # ANSI code for green background
        RED_BACKGROUND = "\033[41m" # ANSI code for green background
        GREEN_BACKGROUND = "\033[42m" # ANSI code for green background
        YELLOW_BACKGROUND = "\033[43m" # ANSI code for green background
        BRIGHT_RED_BACKGROUND = "\033[101m" # ANSI code for green background
        BRIGHT_GREEN_BACKGROUND = "\033[102m" # ANSI code for green background
        BRIGHT_YELLOW_BACKGROUND = "\033[103m" # ANSI code for green background
        RESET = "\033[0m" # ANSI code to reset formatting

        first_line = ""
        for f in range(self.num_frets):
            first_line += f"{f:>3} |"

        # add the pedal info
        first_line += "  A |  B |  C |  D |  E |  F |  G |"
        div = re.sub(r".", "-", first_line)
        print(f"{WHITE_TEXT}{GREEN_BACKGROUND} ROOT {YELLOW_BACKGROUND} THIRD {RED_BACKGROUND} FIFTH {RESET}")
        if chord is not None:
            print(f"Chord: {chord.name}")
        print(first_line)
        print(div)
        for i,s in enumerate(self.guitar.strings):
            line = ""
            a = " "
            b = " "
            c = " "
            d = " "
            e = " "
            f = " "
            g = " "
            modified = False
            if self.pedals["A"][i] != 0:
                if "A" in self.actuated:
                    a = "X"
                    modified = True
                else:
                    a = "-"
            if self.pedals["B"][i] != 0:
                if "B" in self.actuated:
                    b = "X"
                    modified = True
                else:
                    b = "-"
            if self.pedals["C"][i] != 0:
                if "C" in self.actuated:
                    c = "X"
                    modified = True
                else:
                    c = "-"
            if self.pedals["D"][i] != 0:
                if "D" in self.actuated:
                    d = "X"
                    modified = True
                else:
                    d = "-"
            if self.pedals["E"][i] != 0:
                if "E" in self.actuated:
                    e = "X"
                    modified = True
                else:
                    e = "-"
            if self.pedals["F"][i] != 0:
                if "F" in self.actuated:
                    f = "X"
                    modified = True
                else:
                    f = "-"
            if self.pedals["G"][i] != 0:
                if "G" in self.actuated:
                    g = "X"
                    modified = True
                else:
                    g = "-"
            end_line = f"  {a} |  {b} |  {c} |  {d} |  {e} |  {f} |  {g} |"

            for f in range(self.num_frets):
                note = s.fret_note(f)
                in_chord = 0
                if chord is not None:
                    in_chord = chord.contains(note)
                result = re.sub(r"\d+", "", note.name)
                fret = f" {result}"
                if len(fret)==2:
                    fret+=" "

                bg_color = BLACK_BACKGROUND

                if not modified:
                    if in_chord == 1:
                        bg_color = GREEN_BACKGROUND
                    if in_chord == 2:
                        bg_color = YELLOW_BACKGROUND
                    if in_chord == 3:
                        bg_color = RED_BACKGROUND
                else:
                    if in_chord == 1:
                        bg_color = BRIGHT_GREEN_BACKGROUND
                    if in_chord == 2:
                        bg_color = BRIGHT_YELLOW_BACKGROUND
                    if in_chord == 3:
                        bg_color = BRIGHT_RED_BACKGROUND

                fret = f"{WHITE_TEXT}{bg_color}{fret}{RESET}"
                line += f"{fret} |";

            print(line + end_line)
            print(div)

    def __repr__(self):
        return f"{self.guitar}"

    def pedalToggle(self, index):
        if index in self.actuated:
            self.pedalRelease(index)
        else:
            self.pedalPush(index)

    def pedalPush(self, index):
        if index in self.actuated:
            return
        self.actuated[index] = True
        offsets = self.pedals[index]
        for (i,offset) in enumerate(offsets):
            s = self.guitar.strings[i]
            s = s.fret(offset)
            self.guitar.strings[i] = s

    def pedalRelease(self, index):
        if not index in self.actuated:
            return
        del self.actuated[index]
        offsets = self.pedals[index]
        for (i,offset) in enumerate(offsets):
            s = self.guitar.strings[i]
            s = s.fret(-offset)
            self.guitar.strings[i] = s

    def print_pedals(self):
        a = " "
        b = " "
        c = " "
        d = " "
        e = " "
        f = " "
        g = " "
        if 'A' in self.actuated:
            a = "X"
        if 'B' in self.actuated:
            b = "X"
        if 'C' in self.actuated:
            c = "X"

        if 'D' in self.actuated:
            d = "X"
        if 'E' in self.actuated:
            e = "X"
        if 'F' in self.actuated:
            f = "X"
        if 'G' in self.actuated:
            g = "X"

        print("Pedals:")
        print("A B C   D E F G")
        print(f"{a} {b} {c}   {d} {e} {f} {g}")

    def fret(self, num):
        notes = [s.fret(num) for s in self.guitar.strings]
        return notes


class SimpleCompleter(object):

    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            # This is the first time for this text, so build a match list.
            if text:
                self.matches = [s
                                for s in self.options
                                if s and s.startswith(text)]
            else:
                self.matches = self.options[:]

        # Return the state'th item from the match list,
        # if we have that many.
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response

psg = PedalSteelGuitar()
all_chords = {}

def make_completer(vocabulary):
    """
    Creates a custom completer function for readline.
    """
    def custom_complete(text, state):
        results = [x for x in vocabulary if x.startswith(text)] + [None]
        # Add a space after completion if it's a full word, mimicking default readline behavior.
        completion = results[state]
        if completion is not None and completion in vocabulary:
            return completion + " "
        return completion
    return custom_complete

def input_loop():
    line = ''
    chord = None
    while line != 'quit':
        try:
            line = input('Prompt ("quit" to quit): ').strip()
        except EOFError as e:
            sys.exit()
        if line in ['pA', 'pB', 'pC', 'pD', 'pE', 'pF', 'pG']:
            line = line[1:]
            psg.pedalToggle(line)
            psg.print_pedals()
        if line == 'pedals':
            psg.print_pedals()
            continue
        if line in [c for c in all_chords.keys()]:
            chord = all_chords[line]

        psg.print_fretboard(chord)
        psg.print_pedals()

if __name__ == "__main__":
    psg.print_fretboard()
    psg.print_pedals()
    vocabulary = ['pA','pB','pC','pD','pE','pF','pG', 'pedals']

    root_notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    chord_types = ["M", "m", "dim", "aug"]

    for root in root_notes:
        for chord_type in chord_types:
            c = Chord(root, chord_type)
            all_chords[c.name] = c
            vocabulary.append(c.name)

    # Bind the Tab key to the complete function
    readline.parse_and_bind('bind ^I rl_complete')

    # Set the custom completer function
    readline.set_completer(make_completer(vocabulary))

    # Prompt the user for text
    input_loop()
