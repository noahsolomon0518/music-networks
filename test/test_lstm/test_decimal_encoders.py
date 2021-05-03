from unittest import TestCase
from music_networks.lstm.decimal_encoders import DecimalEncoderDimNet, DecimalEncoder




class TestDecimalEncoder(TestCase):
    def test_init(self):
        encoder = DecimalEncoder("test/test_data/midis", True, "both", (30,40), True)
        encoder.encode()



class TestDecimalEncoderDimNet(TestCase):
    def test_init(self):
        print(1)