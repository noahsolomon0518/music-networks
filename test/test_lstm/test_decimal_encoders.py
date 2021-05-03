from unittest import TestCase
from music_networks.lstm.decimal_encoders import DecimalEncoderDimNet, DecimalEncoder, MidiParser





class TestMidiParser(TestCase):
    def test_init(self):
        mp = MidiParser("test/test_data/midis", True, "both", True)
    
    def test_parse(self):
        mp = MidiParser("test/test_data/midis", True, "both", True)
        mp.parse(saveTo="C:/Users/noahs/Data Science/music-networks/test/test_data/streams", nWorkers = 8)
    




class TestDecimalEncoder(TestCase):
    def test_init(self):
        encoder = DecimalEncoder(0)



class TestDecimalEncoderDimNet(TestCase):
    def test_init(self):
        print(1)