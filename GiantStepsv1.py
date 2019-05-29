#================================================================================
# Intervals.py
# Version 1.4
# JL Popyack, May 2016, April 2019, May 2019
# Revisions:
# May 2019
# - revised +/- operators to return deep copies
# April 2019
# - added ".semitones" to Chord class, added "return self" to Chord.invert
# - corrected default inversion
# - amended examples
#================================================================================

from music import *
import copy

#================================================================================
# Define interval constants.
# Each constant refers to the number of semitones that represent it.
# Note that this mapping is not unique, e.g, 7 semitones may be either P5_ or d6_
#================================================================================
P1_ = 0
d2_ = 0
m2_ = 1
M2_ = 2
d3_ = 2
m3_ = 3
A2_ = 3
M3_ = 4
d4_ = 4
P4_ = 5
A3_ = 5
A4_ = 6
d5_ = 6
P5_ = 7
d6_ = 7
m6_ = 8
A5_ = 8
M6_ = 9
d7_ = 9
m7_ = 10
A6_ = 10
M7_ = 11
d8_ = 11
P8_ = 12
A7_ = 12

#================================================================================
# START is the "starting pitch" of an interval.
#================================================================================
START = 0

#================================================================================
# Semitones below the START pitch can be denoted by negating the appropriate
# interval, e.g. -P4.  Semitones an octave higher or lower can use the OCTAVE
# constant, e.g. P4+OCTAVE
# BEAT, BEATS, MEASURE, MEASURES were created so that the JythonMusic programmer
# can use expressions 1*BEAT, 3*BEATS, 1*MEASURE, 2*MEASURES, etc. instead of
# 3.0, 4.0, etc.
#================================================================================
OCTAVE = 12
BEAT = 1.0
BEATS = BEAT
MEASURE = 4*BEATS   #assumes 4/4 time signature
MEASURES = MEASURE

#================================================================================
# makePitches converts a root pitch and a list of semitones to a list of pitches.
# Example:
#   The following are equivalent:
#     pitches = [C2,E2,E2,G2,A2,BF2,A2,G2,E2]
#     pitches = makePitches(C2,[START,4,4,7,9,10,9,7,4])
#     pitches = makePitches(C2,[START,M3_,M3_,P5_,M6_,m7_,M6_,P5_,M3_])
#================================================================================

def makePitches(root,semitones):
    result = []
    for st in semitones:
        if type(st) is list:                        # if this is a chord,
            result.append( makePitches(root,st) )   # apply recursively
        elif st == REST:
            result.append(REST)
        else:
            result.append(root+st)
    return result

### Alternate version of this routine, using map
###def makePitches(root,semitones):
###    return map( lambda st: REST if st==REST else makePitches(root,st) if type(st) is list else root+st , semitones )

#================================================================================
# Chord constants
# These list the intervals that make up a chord.
# Note that these describe I chords only, where the root pitch is the first
# note of the chord.
# ROOT  is the "root pitch" of a chord.
#================================================================================
ROOT  = 0

MAJOR_TRIAD       = [0,4,7]     # [ROOT,M3_,P5_]
MINOR_TRIAD       = [0,3,7]     # [ROOT,m3_,P5_]
DIMINISHED_TRIAD  = [0,3,6]     # [ROOT,m3_,d5]
AUGMENTED_TRIAD   = [0,4,8]     # [ROOT,M3_,A5_]
DOMINANT_SEVENTH  = [0,4,7,10]  # [ROOT,M3_,P5_,m7_]
MAJOR_SEVENTH     = [0,4,7,11]  # [ROOT,M3_,P5_,M7_]
MINOR_SEVENTH     = [0,3,7,10]  # [ROOT,m3_,P5_,m7_]
HALF_DIMINISHED   = [0,3,6,10]  # [ROOT,m3_,d5_,m7]
FULLY_DIMINISHED  = [0,3,6,9]   # [ROOT,m3_,d5_,d7_]
MAJOR_SIXTH       = [0,4,7,9]   # [ROOT,M3_,P5_,m7_]
SUSPENDED_FOURTH  = [0,5,7]     # [ROOT,P4_,P5_]

#================================================================================
# Chord has two constructors:
# With two arguments, it creates a chord with the root as its first note:
#   chord = Chord(C4,MAJOR_TRIAD)       # [C4, E4, G4]
#   chord = Chord(D4,DOMINANT_SEVENTH)  # [D4, FS4, A4, C5]
#
# Its optional third argument specifies which inversion to use (1,2,..n-1),
# where n is the number of notes in the chord. The default inversion is 0
#   chord = Chord(E3,MINOR_TRIAD)       # [E3, G3, B3]
#   chord = Chord(D3,MINOR_SEVENTH,1)   # [D3, F3, A3, C4]  --> [F3, A3, C4, D4]
#   chord = Chord(G3,MAJOR_SEVENTH,2)   # [G3, B3, D4, FS4] --> [D4, FS4, G4, B4]
#================================================================================
class Chord:
   root = C0           # root note of the chord
   quality = [0]       # MAJOR_TRIAD, MINOR_TRIAD, etc.
   pitches = [C0]      # the chord itself is a list of pitches in ascending order
   semitones = [START]

   def __init__(self,root,quality,inversion=0):
       inversion = inversion % len(quality)
       self.root = root
       self.pitches = map( lambda x: root+x,quality )
       self.invert(inversion)
       self.pitches.sort()         # sort pitches in ascending order
       self.semitones = map( lambda p: p-self.root, self.pitches )  # subtract root from each pitch

#================================================================================
# invert can be called directly:
#   ch = Chord(A4,DOMINANT_SEVENTH)   # [A4, CS5, E5, G5]
#   ch.invert(2)                      # [CS5, E5, G5, A5]
#================================================================================
   def invert(self,inversion=0):
       ch = self.pitches
       self.pitches = ch[inversion:] + map( lambda x: OCTAVE+x,ch[:inversion] )
       self.semitones = map( lambda p: p-self.root, self.pitches )  # subtract root from each pitch
       return self

   #========================================================================
   # Overloaded addition and subtraction operators, allow statements such as
   #   Cm = Chord(C4,MINOR_TRIAD)    # [C4, EF4, G4]
   #   Cm_voice1 =  Cm - EF4         # [C4, G4]
   #   Cm_voice1 += [G4, C5, G4]     # now contains three instances of G4
   #   Cm_voice1 += [EF5,G5]         # [C4, EF4, G4, G4, G4, EF5, G5]
   #   Cm_voice1 -= G4               # removes one instance of G4
   #   Cm_voice1 -= [G4]             # removes other two instances of G4
   #   Cm_voice2 =  Chord(C4,MINOR_TRIAD) + Chord(C5,MINOR_TRIAD)
   #   Cm_voice3 =  G3 + Chord(C4,MINOR_TRIAD) + [C5, G5]
   #   Em        =  Chord(E3,MINOR_TRIAD) - [G3] + E4
   #
   # The list of pitches is sorted after adding or subtracting pitches
   #========================================================================
   def __add__(self, object):
      root = self.root
      semitones = copy.deepcopy(self.semitones)
 
      temp = Chord(root,semitones)
      if type(object) is int:     # object is a pitch
         temp.pitches.append(object)
      elif type(object) is list:  # object is a list (hopefully a list of pitches)
         temp.pitches += object
      else:                       # if object is a Chord, join the pitches
         temp.pitches += object.pitches  # otherwise, fail
      temp.pitches.sort()         # sort pitches in ascending order
      temp.semitones = map( lambda p: p-temp.root, temp.pitches )  # subtract root from each pitch
      return temp

   def __radd__(self, object):
      root = self.root
      semitones = copy.deepcopy(self.semitones)
 
      temp = Chord(root,semitones)
      if type(object) is int:     # object is a pitch
         temp.pitches.append(object)
      elif type(object) is list:  # object is a list (hopefully a list of pitches)
         temp.pitches += object
      else:                       # if object is a Chord, join the pitches
         temp.pitches += object.pitches  # otherwise, fail
      temp.pitches.sort()         # sort pitches in ascending order
      temp.semitones = map( lambda p: p-temp.root, temp.pitches )  # subtract root from each pitch
      return temp

   def __sub__(self, pitch):
      root = self.root
      semitones = copy.deepcopy(self.semitones)
 
      temp = Chord(root,semitones)
      if type(pitch) is list:          # remove ALL occurrences of each pitch
         for p in pitch:               # in list, e.g., - [G4]
            while p in temp.pitches:
               temp.pitches.remove(p)
      elif pitch in temp.pitches:
         temp.pitches.remove(pitch)
      temp.pitches.sort()
      temp.semitones = map( lambda p: p-temp.root, temp.pitches )  # subtract root from each pitch
      return temp

   #========================================================================
   # Chord is printed with the names of the pitches, for example:
   #   Cm_voice3 =  G3 + Chord(C4,MINOR_TRIAD) + [C5, G5]
   #   print Cm_voice3          # prints [G3, C4, DS4, G4, C5, G5]
   #   print Cm_voice3.pitches  # prints
   #========================================================================
   def __str__(self):
      return str(map( lambda x: MIDI_PITCHES[x], self.pitches )).translate(None,"'")


#================================================================================
# Chord constants for use with MAJOR scale
#================================================================================
I_    = 1
ii_   = 2
iii_  = 3
IV_   = 4
V_    = 5
vi_   = 6
vii_  = 7
viio_ = 8


# ------------------------------------------------------------------------------------------------------------------------------------------------------
# GiantSteps.py
# ------------------------------------------------------------------------------------------------------------------------------------------------------
import random

# Create the necessary musical data
score = Score("Giant Steps", 286.0)

piano = Part(BRIGHT_ACOUSTIC, 0)  # Piano to MIDI channel 0
sax = Part(TENOR_SAX, 1)  # Sax to MIDI channel 1

#----CONFIG CONSTANTS---------------------
BEATS_PER_MEASURE = 4.0
NUM_REPEATS_OF_FORM = 4

#---MUSICAL CONSTANTS-----------------------------
# See https://jythonmusic.me/api/midi-constants/scale/

# Inherit the Chord class and add a scale associated with each chord
class JazzChord(Chord):
    def __init__(self,root,quality,inversion=0):
        Chord.__init__(self,root,quality,inversion=0)
        if quality is MAJOR_SEVENTH:
            self.scale = MAJOR_SCALE
        elif quality is MINOR_SEVENTH:
            self.scale = AEOLIAN_SCALE
        elif quality is DOMINANT_SEVENTH:
            self.scale = MIXOLYDIAN_SCALE
            
    def dropOctave(self):
        self.pitches = map(lambda x: x - 12, self.pitches)
#================================================================================
# PIANO
#================================================================================
pianoMelody1 = Phrase()
piano.addPhrase(pianoMelody1)

#---------CHORDS-------------------
BMaj7 = JazzChord(B4, MAJOR_SEVENTH, 0)
D7 = JazzChord(D4, DOMINANT_SEVENTH, 0)
GMaj7 = JazzChord(G4, MAJOR_SEVENTH, 0)
Bb7 = JazzChord(BF4, DOMINANT_SEVENTH, 0)
Ebmaj7 = JazzChord(EF4, MAJOR_SEVENTH, 0)
Amin7 = JazzChord(A4, MINOR_SEVENTH, 0)
FS7 = JazzChord(FS4, DOMINANT_SEVENTH, 0)
CSmin7 = JazzChord(CS4, MINOR_SEVENTH, 0)
Fmin7 = JazzChord(F4, MINOR_SEVENTH, 0)
#--------FORM----------------------
CHORD_LIST = [BMaj7, D7, GMaj7, Bb7, Ebmaj7, Amin7, D7, GMaj7, Bb7, Ebmaj7, FS7,
                  BMaj7, Fmin7, Bb7, Ebmaj7, Amin7, D7, GMaj7, CSmin7, FS7, BMaj7,
                  Fmin7, Bb7, Ebmaj7, CSmin7, FS7]
RHYTHM_LIST = [HN, HN, HN, HN, WN, HN, HN, HN, HN, HN, HN, WN, HN, HN, WN, 
                   HN, HN, WN, HN, HN, WN, HN, HN, WN, HN, HN]
# TODO: Randomize these inversions instead of 0's
#---------Comp the form-----------------------------------
for chord, rhythm in zip(CHORD_LIST, RHYTHM_LIST):
    pianoMelody1.addNoteList([chord.pitches], [rhythm])
#---------------------------------------------------------

'''
Algorithm

Given a starting pitch and an ending pitch, return a list of 4 pitches connecting
the two in some sort of musical way within the chord. Does not include the ending pitch

Direction of 0 means descend

E.g F#5 Start. D5 end. 4 notes. Bmaj7 
'''
def create_line(start, end, jazz_chord, direction=1):
    line = jazz_chord.pitches
    NUM_PITCHES = 4

    # If line starts on the root, arpeggiate a pentatonic scale. PENTATONIC_SCALE = [0, 2, 4, 7, 9]
    if (start is jazz_chord.pitches[0]):
        line = []
        pentatonic = JazzChord(start, PENTATONIC_SCALE[:NUM_PITCHES], 0)
        if direction is 0:
            pentatonic.invert(1)
            pentatonic.dropOctave()
            line = pentatonic.pitches
            line.reverse()
        else:
            line = pentatonic.pitches
        
    # If line starts on the 3rd, arpeggiate the appropriate inversion
    elif start is jazz_chord.pitches[1]:
        if direction is 0:
            jazz_chord.invert(2)
            jazz_chord.dropOctave()
            line = jazz_chord.pitches
            line.reverse()
        else:
            jazz_chord.invert(1)
            line = jazz_chord.pitches
        
    # If line starts on the 5th, arpeggiate the appropriate inversion
    elif start is jazz_chord.pitches[2]:
        if direction is 0:
            jazz_chord.invert(3)
            jazz_chord.dropOctave()
            line = jazz_chord.pitches
            line.reverse()
        else:
            jazz_chord.invert(2)
            line = jazz_chord.pitches
        
    # If line starts on the 7th, arpeggiate the appropriate inversion
    elif start is jazz_chord.pitches[3]:
        if direction is 0:
            line = jazz_chord.pitches
        else:
            jazz_chord.invert(3)
            line = jazz_chord.pitches
   
    # TODO: Remaining possibilities, i.e. 6th, 4th, etc.
    # Else, just return an arpeggiated chord for now
    return line
#================================================================================
# SOLOIST
#================================================================================
soloMelody = Phrase()
sax.addPhrase(soloMelody)
soloLinePitches = []
soloLineRhythms = []

# I.e. 5th above root of chord, root, root, 2nd above root, etc...
# Taken from Coltrane's first chorus
DOWN_BEAT_SCALE_DEGREES = [5, 1, 1, 2, 1, 5, 3, 3, 3, 1, 7, 7, 4, 5, 5, 5,
                           4, 5, 2, 1, 1, 1, 6, 1, 6, 3]

DIRECTIONS = [0, 1, 0, 0, 1, 0, 1,
    1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0]


# Basic first pass. Arpeggiate
for i, chord in enumerate(CHORD_LIST):
    current_down_beat = chord.pitches[0] + chord.scale[DOWN_BEAT_SCALE_DEGREES[i] - 1]
    if i >= len(CHORD_LIST) - 1:
        break
    next_chord = CHORD_LIST[i + 1]
    next_down_beat = next_chord.pitches[0] + next_chord.scale[DOWN_BEAT_SCALE_DEGREES[i + 1] - 1]
    num_filler_eight_notes = int((RHYTHM_LIST[i] / EN) - 1)
    
    # Create a line to connect to next_down_beat
    line = create_line(current_down_beat, next_down_beat, chord, DIRECTIONS[i])
 
    for note in line:
        soloLinePitches.append(note)
        soloLineRhythms.append(EN)
        
    # Just repeat line if chord is entire bar. TODO: Improve
    if num_filler_eight_notes > 3:
        for note in line:
            soloLinePitches.append(note)
            soloLineRhythms.append(EN)

# Second pass. Smooth out octaves
for i, pitch in enumerate(soloLinePitches):
    if i >= len(soloLinePitches) - 1:
        break
    distance = pitch - soloLinePitches[i + 1]
    
    # Next pitch is below an octave away, so raise it up
    if distance >= 12:
        soloLinePitches[i + 1] += 12
        soloLinePitches[i + 2] += 12
        soloLinePitches[i + 3] += 12
        soloLinePitches[i + 4] += 12

    # Next pitch is above an octave up
    if distance <= -12:
        soloLinePitches[i + 1] -= 12
        soloLinePitches[i + 2] -= 12
        soloLinePitches[i + 3] -= 12
        soloLinePitches[i + 4] -= 12

# Add notes and rhythms to phrase
soloMelody.addNoteList(soloLinePitches, soloLineRhythms)

# Tie (common tone) pitches that are the same note
Mod.tiePitches(soloMelody)
#=======================================
# PLAY
#=======================================
# Add parts to score
score.addPart(piano)
score.addPart(sax)

# View melody line
View.notation(sax)

# Play score
Play.midi(score)
