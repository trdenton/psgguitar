#!/usr/bin/env python
import pytest
import main

def test_mapNoteToNumber_A4():
    assert( main.Note.mapNoteToNumber("A4") == 69 )

def test_mapNoteToNumber_AS4():
    assert( main.Note.mapNoteToNumber("A#4") == 70 )

def test_mapNoteToNumber_Ab4():
    assert( main.Note.mapNoteToNumber("Ab4") == 68 )

def test_mapNoteToNumber_A5():
    assert( main.Note.mapNoteToNumber("A5") == 69 + 12 )

def test_mapNoteToNumber_G4():
    assert( main.Note.mapNoteToNumber("G4") == 67)

def test_mapNoteToNumber_FS9():
    assert( main.Note.mapNoteToNumber("F#9") == 126 )

def test_mapNoteToNumber_Gb9():
    assert( main.Note.mapNoteToNumber("Gb9") == 126 )


def test_mapNoteToName_A4():
    assert( main.Note.mapNoteToName(69) == "A4")

def test_mapNoteToName_AS4():
    assert( main.Note.mapNoteToName(70) == "A#4")

def test_mapNoteToName_Ab4():
    assert( main.Note.mapNoteToName(68) == "G#4")

def test_mapNoteToName_A5():
    assert( main.Note.mapNoteToName(69 + 12) == "A5")

def test_mapNoteToName_G4():
    assert( main.Note.mapNoteToName(67) == "G4")

def test_mapNoteToName_FS9():
    assert( main.Note.mapNoteToName(126) == "F#9")
