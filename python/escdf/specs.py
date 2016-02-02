#!/usr/bin/python3

import os
import re
import yaml

                    ########################################

#
# Specifications
#

class EscdfSpecs(object):


    def __init__(self, group, specs_text):

        # Init
        self.group = group

        # Read specifications from file or text string
        if ( (not re.search("\n", specs_text, flags=re.DOTALL)) and \
             os.access(specs_text, os.R_OK) ):
            with open(specs_text, "r") as yaml_doc:
                self.yaml_data = yaml.load(yaml_doc)
        else:
            self.yaml_data = yaml.load(specs_text)

        # Propagate information
        self.bufs = sorted([item for item in self.yaml_data \
            if self.yaml_data[item]["spec_type"] == "buffer"])
        self.data = sorted([item for item in self.yaml_data \
            if self.yaml_data[item]["spec_type"] == "dataset"])
        self.meta = sorted([item for item in self.yaml_data \
            if self.yaml_data[item]["spec_type"] == "metadata"])
        self.elts = self.meta + self.data + self.bufs


    def get_spec(self, elem):

        if ( elem in self.elts ):
            retval = dict(self.yaml_data[elem])
            retval["name"] = elem
            retval["group"] = self.group
            return retval
        else:
            return None


    def get_elements(self):

        return self.elts


    def get_reference(self, elem):

        if ( self.is_ref_fixed(elem) ):
            return self.get_spec(elem[1:])
        elif ( self.is_ref_varying(elem) ):
            return self.get_spec(elem[1:-3])
        else:
            return None


    def is_ref(self, elem):

        return ( (elem[0] == "@") and \
                 ((elem[1:] in self.elts) or (elem[1:-3] in self.elts)) )


    def is_ref_fixed(self, elem):

        return ( self.is_ref(elem) and (elem[-3:] != "(?)") )


    def is_ref_varying(self, elem):

        return ( self.is_ref(elem) and (elem[-3:] == "(?)") )

