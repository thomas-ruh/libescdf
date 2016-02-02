#!/usr/bin/python3

import re
import textwrap
import yaml

                    ########################################

#
# Fortran wrappers
#

# Default Fortran wrapper structure
f03_wrapper_default = """\
void @name@(
        @params@) {
    @glue_code@
}"""

class EscdfFortranWrapper(object):

    def __init__(self, group, template=None):

        # Init
        self.group = group
        if ( template ):
            self.template = EscdfTemplate(template)
        else:
            self.template = EscdfTemplate(f03_wrapper_default)
        self.wrapper_type = {
            "bool":"bool",
            "char":"char",
            "double":"double",
            "float":"float",
            "int":"int",
            "long_int":"long",
            "short_int":"short",
            "unsigned_long":"unsigned long",
            "unsigned_int":"unsigned int",
            "unsigned_short":"unsigned short"}


    def build_wrapper_glue(self, specs):

        retval = ""
        action = specs["action"]

        # Take care of dimensions first
        if ( len(specs["glue"]) > 1 ):
            for param in specs["glue"][:-1]:
                if ( retval != "" ):
                    retval += "\n"
                if ( action == "get" ):
                    retval += "*%s = escdf_%s_%s_%s();" % \
                        (param, self.group, param, action)
                elif ( action == "put" ):
                    retval += "escdf_%s_%s_%s(*%s);" % \
                        (self.group, param, action, param)
                else:
                    raise ValueError("unsupported action '%s'" % action)

        # Finish with the main target
        if ( retval != "" ):
            retval += "\n"
        param = specs["glue"][-1]
        if ( action == "get" ):
            param_ptr = ""
            param_cast = ""
            if ( len(specs["glue"]) == 1 ):
                param_ptr = "*"
            else:
                param_cast = "(%s *)" % specs["type"]
            retval += "%s%s = %sescdf_%s_%s_%s();" % \
                (param_ptr, param, param_cast, self.group, param, action)
        elif ( action == "put" ):
            retval += "escdf_%s_%s_%s(%s%s);" % \
                (self.group, param, action, param,
                    ", ".join(specs["glue"][:-1]))
        else:
            raise ValueError("unsupported action '%s'" % action)

        return retval


    def build_wrapper_params(self, specs):

        target = specs["f03_name"]
        action = specs["f03_action"]
        retval = {"action":action}

        # Init parameter list
        params_list = []
        target_dims = []

        # Add dimensions when needed
        if ( specs["object"] == "array" ):
            for dim in specs["object_dims"]:
                if ( isinstance(dim, str) ):
                    dim_name = re.sub("(^@|[\\(\\?\\)])", "", dim)
                    if ( not dim_name in params_list ):
                        params_list.append(dim_name)
                    target_dims.append(dim_name)
                else:
                    target_dims.append(dim)

        # Add types and input/output status
        params_mod = ""
        if ( action == "put" ):
            params_mod = "const "
        params_string = "%s%s *%s" % \
            (params_mod, self.wrapper_type[specs["type"]], target)
        for dim in params_list:
            params_string += ", %s%s *%s" % \
            ( params_mod, self.wrapper_type["unsigned_int"], dim)

        # Gather info needed for params and glue code
        retval["type"] = specs["type"]
        retval["desc"] = params_string
        retval["glue"] = []
        if ( len(target_dims) > 0 ):
            retval["glue"] += params_list
            retval["dims"] = target_dims
        retval["glue"] += [target]

        return retval


    def build_wrapper_routine(self, elem, specs, action):
        """Generate a C -> Fortran wrapper for a variable from a dictionary"""

        wrapper_text = self.template
        wrapper_specs = {
            "name":"escdf_f03_%s_%s_%s" % (self.group, elem, action)}
        specs["f03_name"] = elem
        specs["f03_action"] = action
        params_specs = self.build_wrapper_params(specs)
        glue_specs = self.build_wrapper_glue(params_specs)
        wrapper_specs["params"] = params_specs["desc"]
        wrapper_specs["glue_code"] = glue_specs

        wrapper_text = self.template.substitute(wrapper_specs)

        return wrapper_text


                    ########################################

#
# C -> Fortran glue code
#

# Glue code default structure
f03_glue_default = """\
/* C -> Fortran 2003 glue code for @group@ - machine-generated */

@glues@
"""

class EscdfFortranGlue(object):

    def __init__(self, group, yaml_doc, template=None):

        self.group = group
        self.specs = EscdfSpecs(yaml_doc)
        if ( template ):
            self.template = EscdfTemplate(template)
        else:
            self.template = EscdfTemplate(f03_glue_default)
        self.fields = ["object", "object_dims", "type"]

        f03_glues = []
        f03_glue_specs = EscdfFortranWrapper(self.group)
        for elem in self.specs.get_elements():
            for action in ["get", "put"]:
                tmp_spec = self.specs.get_spec(elem)
                spec = {}
                for field in self.fields:
                    try:
                        spec[field] = tmp_spec[field]
                    except KeyError:
                        pass
                f03_glues.append(f03_glue_specs.build_wrapper_routine(elem,
                    spec, action))

        self.patterns = {}
        self.patterns["group"] = self.group
        self.patterns["glues"] = "\n".join(f03_glues)


    def __str__(self):

        return self.template.substitute(self.patterns)

