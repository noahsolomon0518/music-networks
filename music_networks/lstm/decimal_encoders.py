import datetime
from os import walk
from os import path
import math
import warnings
import music21
from music21 import midi, converter
from sys import getsizeof
from timeit import timeit
import time
import pickle
from multiprocessing import Process, Queue, Array
import multiprocessing as mp


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



class MidiParser:
    """
    This object is used to parse midis to music21 streams and performs functions such as 
    converting all pieces to C, only extracting a certain mode ect. This process takes a long time
    so there is a function called serialize which pickles the streams so the decimal encoder
    can quickly extract the parsed midis whenever it needs to. 
    """

    def __init__(self, folder, convertToC, mode, removeDrums, debug = False):

        self.convertToC = convertToC
        self.mode = mode
        self.removeDrums = removeDrums
        self.debug = debug
        self.midiPaths = []
        self.queueMidis(folder)
        self._dbg(str(len(self.midiPaths))+ "midis queued up to be parsed.")


        

    

    def parse(self, saveTo, nWorkers = 8):
        nMidis = len(self.midiPaths)
        parsingSplit = self.partitionSplit(nMidis, nWorkers)
        processes = []
        for split in parsingSplit:
            p = mp.Process(target=self.parsePartition, args=(self.midiPaths, split, saveTo))
            p.start()
            processes.append(p)
        for process in processes:
            process.join()
        


    def partitionSplit(self, nMidis, nWorkers):
        split = [[] for i in range(nWorkers)]
        for ind in range(nMidis):
            split[ind%nWorkers].append(ind)
        return split



    def parsePartition(self, _paths, inds, folder):
        for ind in inds:
            _path = _paths[ind]
            valid = True
            midiStream = converter.parse(_path)
            key = midiStream.analyze('key')
            midiStream.insert(0,key)
            if(self.mode != key.mode and self.mode != "both"):
                continue
        
            if(self.convertToC):
                self._convertToC(midiStream)

            
            self.serialize(midiStream, folder)


    def _convertToC(self, stream):
        key = stream.keySignature
        key.transpose(int(12-HALF_STEPS_ABOVE_C[key.tonic.name]), inPlace = True)
        for n in stream.recurse().notes:
            n.transpose(int(12-HALF_STEPS_ABOVE_C[key.tonic.name]), inPlace = True)




    def serialize(self, parsedMidis, folder):
        if type(parsedMidis) != list:
            parsedMidis = [parsedMidis] 

        for parsedMidi in parsedMidis:
            converter.freeze(parsedMidi, fp = folder+"/"+str(parsedMidi.id)+".stream")



    def _dbg(self, msg):
        if(self.debug):
            print("[DEBUG "+ str(time.time()) +"]:"+msg)


    def queueMidis(self, folder, r=True):
        """
        Queues up midis to be parsed

        Parameters
        ----------
        folder: str
            The folder at which the midis are located
        r: bool
            Whether the midis should be recursively extracted from the folders
        
        Returns list of paths
        """
        paths = []
        if(".mid" in folder):
            paths.append(folder)
            self.midiPaths.extend(paths)
            return 

        for (dirpath, _, filenames) in walk(folder):
            for file in filenames:
                if ".mid" in file:
                    paths.append(path.join(dirpath, file))
            if not r:
                self.midiPaths.extend(paths)
                return
        self.midiPaths.extend(paths)
        












class DecimalEncoder:
    def __init__(self, parsedMidis, debug = False):
        """
        Abstract class for all decimal encoders

        Parameters
        ----------
        parsedMidis: path of folder of streams
            The parsed midis that will used for training
        debug: bool
            Whether to recieve verbose
        """
        self.debug = debug



    def _dbg(self,msg):
        if(self.debug):
            print("[DEBUG "+ str(datetime.datetime.now().strftime("%H:%M:%S")) +"]:"+msg)

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










