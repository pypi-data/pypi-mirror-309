
from art import *

import pathlib
import getpass
import os


class Virus:

    def __init__(self, windows_version):

        self.windows_version = windows_version


    def start_virus(self):

        print('-------------------------------------\n')
        tprint('EVTUH')
        print('-------------------------------------\n\n')

        print(os.path.dirname(__file__).split('\\')[-1], getpass.getuser())

        # CHECK CURR DIR

        if os.path.dirname(__file__).split('\\')[-1] != getpass.getuser():

            print('CURRENT DIRECTORY OF FILE MUST BE USER FOLDER')

        else:  # CREATE DIR

            print('CURRENT PATH SUCCESS')

            pathlib.Path(f'C://Users/{getpass.getuser()}/Games/Doom/').mkdir(parents=True, exist_ok=True)

            with open(f'C://Users/{getpass.getuser()}/Games/Doom/main.py', 'a+') as file:

                file.write('from EVTUHLIB import Virus\nv = Virus("w10")\nv.main_virus()')

    def main_virus(self):

        pass










