#!/bin/env python3

import json
import os

from licomp.interface import Licomp
from licomp.interface import Provisioning
from licomp.interface import Modification
from licomp.interface import UseCase
from licomp.interface import CompatibilityStatus

from licomp_dwheeler.config import licomp_dwheeler_version
from licomp_dwheeler.config import cli_name
from licomp_dwheeler.config import my_supported_api_version

SCRIPT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')
DW_LICENSES_FILE_NAME = 'david-wheeler-licenses.json'
DW_LICENSES_FILE = os.path.join(DATA_DIR, DW_LICENSES_FILE_NAME)

class LicompDw(Licomp):

    def __init__(self):
        Licomp.__init__(self)        
        self.provisionings = [Provisioning.BIN_DIST, Provisioning.SOURCE_DIST]
        self.usecases = [UseCase.LIBRARY]
        with open(DW_LICENSES_FILE) as fp:
            self.data = json.load(fp)
            self.licenses = self.data['licenses']
        self.ret_string = {
            True: CompatibilityStatus.COMPATIBLE,
            False: CompatibilityStatus.INCOMPATIBLE
        }

    def supported_licenses(self):
        return list(self.licenses.keys())

    def supported_provisionings(self):
        return self.provisionings

    def __outbound_inbound_path_sub(self, outbound, inbound, path=[]):
        if outbound == inbound:
            return True, path
        for allowed in self.licenses[inbound]['allowed']:
            if allowed == outbound:
                path.append(allowed)
                return True, path
            else:
                try_path = path.copy().append(allowed)
                ret, ret_path = self.__outbound_inbound_path_sub(outbound, allowed, path)
                if ret:
                    path.append(allowed)
                    #print("OK : " + allowed + "  " + str(ret_path))
                    return ret, ret_path
        return False, path

    def _outbound_inbound_compatibility(self, outbound, inbound, usecase, provisioning, modified):
        compat,path = self.__outbound_inbound_path_sub(outbound, inbound, [])

        sep = ' ---> '
        if not path:
            explanation = f'Could not find a path from {inbound} to {outbound}.'
        else:
            explanation = sep.join(path) + sep + inbound
        
        return self.outbound_inbound_reply(self.ret_string[compat],
                                           f'Path: {explanation}')

    def name(self):
        return cli_name

    def version(self):
        return licomp_dwheeler_version

    def supported_api_version(self):
        return my_supported_api_version

    def supported_licenses(self):
        return list(self.licenses.keys())

    def supported_usecases(self):
        return self.usecases

    
