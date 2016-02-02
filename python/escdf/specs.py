#!/usr/bin/python3

import re
import textwrap
import yaml

                    ########################################

#
# Specifications
#

class EscdfSpecs(object):


    def __init__(self, specs_file):

        with open(specs_file, "r") as yaml_doc:
            self.yaml_data = yaml.load(yaml_doc)
            self.bufs = sorted([item for item in self.yaml_data \
                if self.yaml_data[item]["spec_type"] == "buffer"])
            self.sets = sorted([item for item in self.yaml_data \
                if self.yaml_data[item]["spec_type"] == "dataset"])
            self.meta = sorted([item for item in self.yaml_data \
                if self.yaml_data[item]["spec_type"] == "metadata"])
            self.elts = self.meta + self.sets + self.bufs


    def get_spec(self, elem):

        if ( elem in self.elts ):
            return self.yaml_data[elem]
        else:
            return None


    def get_elements(self):

        return self.elts


    def get_reference(self, elem):

        if ( self.is_ref_fixed(elem) ):
            return self.yaml_data[elem[1:]]
        elif ( self.is_ref_varying(elem) ):
            return self.yaml_data[elem[1:-3]]
        else:
            return None


    def is_ref(self, elem):

        return ( (elem[0] == "@") and \
                 ((elem[1:] in self.elts) or (elem[1:-3] in self.elts)) )


    def is_ref_fixed(self, elem):

        return ( self.is_ref(elem) and (elem[-3:] != "(?)") )


    def is_ref_varying(self, elem):

        return ( self.is_ref(elem) and (elem[-3:] == "(?)") )

