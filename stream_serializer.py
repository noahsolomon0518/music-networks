import os
import sys
import argparse


parser = argparse.ArgumentParser(description='Serialize midis into streams')

parser.add_argument('Midi Folder',
                       metavar='mf',
                       type=str,
                       help='Folder with midis')

parser.add_argument('Stream Folder',
                       metavar='sf',
                       type=str,
                       help='Folder where midis will be serialized into streams')


args = parser.parse_args()

print(args["Midi Folder"])