#!/usr/bin/env python
from os import environ, path

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

import os

# os.chdir('/opt/project')

# Create a decoder with certain model
config = Decoder.default_config()
# config.set_string('-hmm', 'resources/es-es_acoustic_model')
config.set_string('-hmm', 'resources/original')
config.set_string('-lm', 'resources/model.lm.bin')
config.set_string('-dict', 'resources/es.dic')
decoder = Decoder(config)

# Decode streaming data.
decoder = Decoder(config)
decoder.start_utt()
stream = open('resources/4.wav', 'rb')
while True:
    buf = stream.read(1024)
    if buf:
        decoder.process_raw(buf, False, False)
    else:
        break
decoder.end_utt()
print('Best hypothesis segments: ', [seg.word for seg in decoder.seg()])
