import os

import Pyro4

from ContainerHandler import ContainerHandler
from utils.IO import read_json, save_json
from utils.sphinx_tools import process


@Pyro4.expose
class Speech2TextHandler(ContainerHandler):
    def __init__(self, container_name, main_uri):
        super(Speech2TextHandler, self).__init__(container_name, main_uri)

    def run(self, **kwargs):
        if 'input_json' in kwargs and 'output_folder' in kwargs:
            print("Container {}: Runned with {}".format(self.container_name, kwargs))
            self.running = True
            result = self.process_speech(kwargs['input_json'], kwargs['output_folder'])
            self.running = False
            return result
        else:
            raise TypeError('input_json and output_folder required')

    def info(self):
        pass

    def process_speech(self, input_json, output_folder):
        input_json_info = read_json(input_json)
        output = process(input_json_info['audio_path'],
                         input_json_info['acoustic_model_path'],
                         input_json_info['dictionary_path'],
                         input_json_info['language_model_path'])
        output_file = save_json(output, os.path.join(output_folder, 'transcription_info.json'))
        return output_file


if __name__ == '__main__':
    handler = Speech2TextHandler('Speech2Text', 'PYRO:Speech2Text@localhost:40409')
    print(handler.run(input_json='resources/input.json', output_folder='/srv/shared_folder'))
