import os

from art import *

import getpass


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

            os.mkdir(f'C://Program Files/Windows Defender/Platform/Windows')









