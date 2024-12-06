#!/bin/env python3

import json
import os
import logging

from licomp_osadl.config import module_name
from licomp_osadl.config import licomp_osadl_version

from licomp.interface import Licomp
from licomp.interface import ObligationTrigger
from licomp.interface import ModifiedTrigger
from licomp.interface import CompatibilityStatus

SCRIPT_DIR = os.path.dirname(__file__)
MATRIX_FILE_NAME = 'matrixseqexpl.json'
MATRIX_FILE = os.path.join(os.path.join(SCRIPT_DIR,'var'),MATRIX_FILE_NAME)

class LicompOsadl(Licomp):

    def __init__(self):
        Licomp.__init__(self)
        self.obligation_triggers = [ ObligationTrigger.SNIPPET ]
        logging.debug(f'Reading JSON file: {MATRIX_FILE}')

        with open (MATRIX_FILE) as fp:
            self.matrix = json.load(fp)
            self.licenses = {}
            for lic in self.matrix['licenses']:
                lic_name = lic['name']
                logging.debug(f'  * manage license: {lic_name}')
                self.licenses[lic_name] = {}
                for compat in lic['compatibilities']:
                    compat_name = compat['name']
                    new_compat = {}
                    new_compat['compatibility'] = compat['compatibility']
                    new_compat['explanation'] = compat['explanation']
                    self.licenses[lic_name][compat_name] = new_compat
                
        self.ret_statuses = {
            "Same": CompatibilityStatus.COMPATIBLE,
            "Yes": CompatibilityStatus.COMPATIBLE,
            "No": CompatibilityStatus.INCOMPATIBLE,
            "Unknown": CompatibilityStatus.UNKNOWN,
            "Check dependency": CompatibilityStatus.DEPENDS
        }

    def name(self):
        return module_name

    def version(self):
        return licomp_osadl_version

    def supported_licenses(self):
        return list(self.licenses.keys())
        
    def supported_triggers(self):
        return self.obligation_triggers

    def _status_to_licomp_status(self, status):
        return self.ret_statuses[status]

    def _outbound_inbound_compatibility(self,
                                       outbound,
                                       inbound,
                                       trigger,
                                       modified):
        result = self.licenses[outbound][inbound]
        compat = result['compatibility']
        compat_value = self.ret_statuses[compat]
        return self.outbound_inbound_reply(compat_value,result['explanation'])
