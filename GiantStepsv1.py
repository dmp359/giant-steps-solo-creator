#================================================================================
# Intervals.py
# Version 1.3
# JL Popyack, May 2016, April 2019
# Revisions:
# - added ".semitones" to Chord class, added "return self" to Chord.invert
# - amended examples
#================================================================================


from music import *

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
      if type(object) is int:     # object is a pitch
         self.pitches.append(object)
      elif type(object) is list:  # object is a list (hopefully a list of pitches)
         self.pitches += object
      else:                       # if object is a Chord, join the pitches
         self.pitches += object.pitches  # otherwise, fail
      self.pitches.sort()         # sort pitches in ascending order
      self.semitones = map( lambda p: p-self.root, self.pitches )  # subtract root from each pitch
      return self

   def __radd__(self, object):
      return self + object

   def __sub__(self, pitch):
      if type(pitch) is list:          # remove ALL occurrences of each pitch
         for p in pitch:               # in list, e.g., - [G4]
            while p in self.pitches:
               self.pitches.remove(p)
      elif pitch in self.pitches:
         self.pitches.remove(pitch)
      self.pitches.sort()
      self.semitones = map( lambda p: p-self.root, self.pitches )  # subtract root from each pitch
      return self

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
# Create the necessary musical data
score = Score("Giant Steps", 260.0) 

piano = Part(BRIGHT_ACOUSTIC, 0)  # Piano to MIDI channel 0
sax = Part(TENOR_SAX, 1)  # Sax to MIDI channel 1

#----CONFIG CONSTANTS---------------------
BEATS_PER_MEASURE = 4.0
NUM_REPEATS_OF_FORM = 4

#---MUSICAL CONSTANTS-----------------------------
# See https://jythonmusic.me/api/midi-constants/scale/
class JazzChord(Chord):
  def __init__(self,root,quality,inversion=0):
    Chord.__init__(self,root,quality,inversion=0)
    if quality is MAJOR_SEVENTH:
        self.scale = MAJOR_SCALE
    elif quality is MINOR_SEVENTH:
        self.scale = AEOLIAN_SCALE
    elif quality is DOMINANT_SEVENTH:
        self.scale = MIXOLYDIAN_SCALE
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
for i in range(NUM_REPEATS_OF_FORM):
    for chord, rhythm in zip(CHORD_LIST, RHYTHM_LIST):
        pianoMelody1.addNoteList([chord.pitches], [rhythm])
#---------------------------------------------------------


#================================================================================
# SOLOIST
#================================================================================
soloMelody = Phrase()
sax.addPhrase(soloMelody)

# I.e. 5th above root of chord, root, root, 2nd above root, etc...
DOWN_BEAT_SCALE_DEGREES = [5, 1, 1, 2, 1, 5, 3, 3, 3, 1, 7, 7, 4, 5, 5, 5,
                           4, 5, 2, 1, 1, 1, 6, 1, 6, 3]
for i in range(NUM_REPEATS_OF_FORM):
    for chord, rhythm, degree in zip(CHORD_LIST, RHYTHM_LIST, DOWN_BEAT_SCALE_DEGREES):
        soloMelody.addNoteList([chord.pitches[0] + chord.scale[degree - 1]], [rhythm])
#=======================================
# PLAY
#=======================================
# add parts to score
score.addPart(piano)
score.addPart(sax)

# play score
Play.midi(score)
