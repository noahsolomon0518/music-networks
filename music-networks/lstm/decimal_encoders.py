import datetime
class DecimalEncoder:
    def __init__(self, folder, convertToC, scales, noteRange, debug = False):
        self.debug = debug
        self.folder = folder
        self.convertToC = convertToC
        self.scales = scales
        self.noteRange = noteRange
        
    #handles calling functions that all decimal encoders will have
    def _prepare(self):
        self._convertToC(self)
        self._filterByScales(self)
        self._applyNoteRange(self)

    
    def _convertToC(self):
        if(not self.convertToC):
            self.dbg("Not converting pieces to C")
            return
        self.dbg("Converting pieces to C")

    def _filterByScales(self):
        pass


    def _applyNoteRange(self):
        pass

    def _dbg(self,msg):
        if(self.debug):
            print("[DEBUG "+ str(datetime.now().strftime("%H:%M:%S")) +"]:"+msg)


    


    def addFolders(self):
        pass

    def encode(self):
        self._prepare()





class DecimalEncoderDimNet:
    """
    Every distinct combination of notes is a distinct class. Notes can be on or off.
    This network is going to be used to test how well an LSTM
    can deal with a large amount of dimensions. 
    """
    def __init__(self):
        pass










