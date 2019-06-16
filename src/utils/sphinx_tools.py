#!/usr/bin/env python

import re

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

from utils.IO import check_file, check_folder


def process(audio_path, acoustic_model_path, dictionary_path, language_model_path):
    """
    TODO DOCUMENTATION
    :param audio_path:
    :param acoustic_model_path:
    :param dictionary_path:
    :param language_model_path:
    :return:
    """
    check_folder(acoustic_model_path)
    check_file(dictionary_path)
    check_file(audio_path)
    check_file(language_model_path)

    config = Decoder.default_config()
    config.set_string('-hmm', acoustic_model_path)
    config.set_string('-lm', language_model_path)
    config.set_string('-dict', dictionary_path)

    decoder = Decoder(config)
    decoder.start_utt()
    stream = open(audio_path, 'rb')

    while True:
        buf = stream.read(2048)
        if buf:
            decoder.process_raw(buf, False, False)
        else:
            break

    decoder.end_utt()
    # print('Best hypothesis segments:',
    #       [(seg.word, seg.start_frame / 100, seg.end_frame / 100) for seg in decoder.seg()])

    hypothesis = decoder.hyp()
    logmath = decoder.get_logmath()

    pattern = re.compile("<.*s.*>")
    output = {}
    output['model_score'] = logmath.exp(hypothesis.best_score)
    output['confidence'] = logmath.exp(hypothesis.prob)
    output['text'] = [{'text': seg.word, 'start_time': seg.start_frame / 100, 'end_time': seg.end_frame / 100}
                      for seg in decoder.seg() if not pattern.match(seg.word)]
    return output
