import datetime
from os import walk
from os import path
import math
import warnings
import music21
from music21 import midi
from sys import getsizeof

HALF_STEPS_ABOVE_C = {
        "C":0,
        "B#":0,
        "D-":1,
        "C#":1,
        "D":2,
        "E-":3,
        "D#":3,
        "F-":4,
        "E":4,
        "E#":5,
        "F":5,
        "F#":6,
        "G-":6,
        "G":7,
        "G#":8,
        "A-":8,
        "A":9,
        "A#":10,
        "B-":10,
        "B":11
    }

# Takes list of paths (or just one), and parses into mido object
def parseMidis(paths, convertToC, mode, removeDrums):
    parsedMidis = []

    if(type(paths) != list):
        paths = [paths]





    for _path in paths:
        mf = midi.MidiFile()
        mf.open(_path)
        mf.read()
        mf.close()
        valid = True
        if(removeDrums):
            for i in range(len(mf.tracks)):
                mf.tracks[i].events = [ev for ev in mf.tracks[i].events if ev.channel != 10]  
        midiStream = midi.translate.midiFileToStream(mf)
        print(midiStream)
        key = midiStream.analyze('key')
        midiStream.insert(0,key)

        if(mode != key.mode and mode != "both"):
            valid = False


        if(valid and not convertToC):
            parsedMidis.append(midiStream)

        if(valid and convertToC):
            key.transpose(int(12-HALF_STEPS_ABOVE_C[key.tonic.name]), inPlace = True)
            for n in midiStream.recurse().notes:
                n.transpose(int(12-HALF_STEPS_ABOVE_C[key.tonic.name]), inPlace = True)
            parsedMidis.append(midiStream)

    return parsedMidis


# Recursively creates list of midi files in directory
def findMidis(folder, r=True):
    paths = []
    if(".mid" in folder):
        paths.append(folder)
        return paths

    for (dirpath, _, filenames) in walk(folder):
        for file in filenames:
            if ".mid" in file:
                paths.append(path.join(dirpath, file))
        if not r:
            return paths
    return paths





class DecimalEncoder:
    def __init__(self, folder, convertToC, mode, noteRange, debug = False):
        """
        Abstract class for all decimal encoders

        Parameters
        ----------
        folder: str
            Path of the folder that has all midis

        convertToC: bool
            Whether to convert all midis to C. If a piece does not have key sig then it is not parsed
        
        mode: str -> ["major", "minor", "both"]
            What type of mode to keep. If choice is major then midis with minor mode will not be parsed

        noteRange: tuple
            The range of notes that will be extracted. Notes outside range will be brought up or brought done octaves
        
        debug: bool
            Whether to recieve verbose
        """
        self.debug = debug
        self.convertToC = convertToC
        self.mode = mode
        self.noteRange = noteRange
        self.midiPaths = findMidis(folder)
        self._dbg("Found "+ str(len(self.midiPaths)) + " midis.")

    def _applyNoteRange(self):
        pass

    def _dbg(self,msg):
        if(self.debug):
            print("[DEBUG "+ str(datetime.datetime.now().strftime("%H:%M:%S")) +"]:"+msg)

    def addFolders(self, folder):
        self.midiPaths.extend(findMidis(folder))

    def encode(self):
        self._dbg("Starting to parse midis.")
        parsedMidis = parseMidis(self.midiPaths, self.convertToC, self.mode, removeDrums = True)
        self._dbg("Finished parsing midis. Below shows one parsed midi: ")
        self._dbg(str(parsedMidis[0]))
        self._dbg(str(getsizeof((parsedMidis[0]))))
        self._dbg("Starting to encode parsed midis.")
        return self._encode(parsedMidis)


    def _encode(self, parsedMidis):
        raise NotImplementedError("Add _encode(midiObjs) function.")





class DecimalEncoderDimNet:
    """
    Every distinct combination of notes is a distinct class. Notes can be on or off.
    This network is going to be used to test how well an LSTM
    can deal with a large amount of dimensions. 
    """
    def __init__(self):
        pass










