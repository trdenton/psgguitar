#!/usr/bin/env python
import math
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

    def fret(self, fret_num):
        return self.openNote.addHalfSteps(fret_num)

class Chord:
    def __init__(self):
        pass

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

    def print_fretboard(self):
        first = True
        for s in self.guitar.strings:
            line = ""
            for f in range(self.num_frets):
                note = s.fret(f)
                result = re.sub(r"\d+", "", note.name)
                fret = f" {result}"
                if len(fret)==2:
                    fret+=" "
                line += f"{fret} |";
            div = re.sub(r".", "-", line)
            if first:
                print(div)
                first = False
            print(line)
            print(div)

    def __repr__(self):
        return f"{self.guitar}"

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

    def fret(self, num):
        notes = [s.fret(num) for s in self.guitar.strings]
        return notes

if __name__ == "__main__":
    psg = PedalSteelGuitar()
    psg.print_fretboard()
