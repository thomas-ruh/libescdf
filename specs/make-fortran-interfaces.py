#!/usr/bin/python3

import re
import textwrap
import yaml

                    ########################################

#
# Templates
#

class EscdfTemplate(object):

    def __init__(self, text):

        # Init
        self.text = text
        self.re_newline = re.compile(r"\n", flags=re.MULTILINE+re.DOTALL)

        # Find keywords in template
        re_keywords = re.compile("@([a-z0-9_]+)@", flags=re.MULTILINE)
        self.keywords = re_keywords.findall(self.text)
        if ( self.keywords ):
            self.keywords = list(set(self.keywords))
        else:
            self.keywords = []

        # Find indentation levels of substituted blocks
        # Note: there might be unindented keywords in the template,
        #       hence the use of another keywords variable here
        self.indents = {}
        re_indent = re.compile("^([ ]+)@([a-z0-9_]+)@$", flags=re.MULTILINE)
        indents = list(set(re_indent.findall(self.text)))
        if ( (len(self.keywords) > 0) and (len(indents) > 0) ):
            offsets, keywords = zip(*indents)
            for word in self.keywords: 
                chk_word = [idx for idx, kwd in enumerate(keywords) \
                    if kwd == word]
                if ( len(chk_word) > 1 ):
                    raise NameError(
                        "ambiguous definition of '%s' in template" % name)
                elif ( len(chk_word) == 0 ):
                    self.indents[word] = 0
                else:
                    self.indents[word] = len(offsets[chk_word[0]])


    def check_specs_ok(self, specs):

        errs = [item for item in self.keywords if not item in specs]
        if ( len(errs) > 0 ):
            raise KeyError("missing input keywords: %s" % errs)
        errs = [item for item in specs if not item in self.keywords]
        if ( len(errs) > 0 ):
            raise KeyError("extra input keywords: %s" % errs)

        return True


    def reindent(self, keyword, value):

        if ( self.re_newline.search(value) ):
            sep = "\n" + " " * self.indents[keyword]
            return sep.join(value.split("\n"))
        else:
            return value


    def substitute(self, specs):

        retval = self.text
        for kwd, val in specs.items():
            retval = re.sub("@%s@" % kwd, self.reindent(kwd, val), retval)

        return retval


    def wrap_fortran(self, src_text):

        f03_lines = []
        for line in src_text.splitlines():
          line = textwrap.wrap(line,
              width=77,
              drop_whitespace=False,
              break_long_words=False)
          if ( len(line) > 1 ):
            for idx in range(0,len(line)-1):
                line[idx] += " &"
            for idx in range(1,len(line)):
                line[idx] = "& " + line[idx]
          f03_lines += line

        return "\n".join(f03_lines)


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


                    ########################################

#
# Fortran interfaces
#

# Fortran interface default structure
f03_interface_default = """\
interface
    subroutine @name@(@params_list@)
        implicit none
        @params_desc@
    end subroutine @name@
end interface"""


class EscdfFortranInterface(object):

    def __init__(self, group, template=None):

        # Init
        self.group = group
        if ( template ):
            self.template = EscdfTemplate(template)
        else:
            self.template = EscdfTemplate(f03_interface_default)
        self.f03_type = {
            "bool":"logical",
            "char":"character(len=*)",
            "double":"double precision",
            "float":"real",
            "int":"integer",
            "long_int":"integer",
            "short_int":"integer",
            "unsigned_long":"integer",
            "unsigned_int":"integer",
            "unsigned_short":"integer"}


    def build_f03_interface(self, elem, specs, action):
        """Generate a Fortran interface for a variable from a dictionary"""

        f03_text = self.template
        specs["f03_name"] = elem
        specs["f03_action"] = action
        f03_specs = self.build_f03_params(specs)
        green_light = self.template.check_specs_ok(f03_specs)

        f03_text = self.template.substitute(f03_specs)
        f03_text = self.template.wrap_fortran(f03_text)

        return f03_text


    def build_f03_params(self, specs):

        ret = {"name":"escdf_f03_%s_%s_%s" % \
            (self.group, specs["f03_name"], specs["f03_action"])}
        f03_intent = {"get":"inout", "put":"in"}
        params_list = []
        params_desc = {}

        params_desc[specs["f03_name"]] = {}
        if ( specs["object"] == "array" ):
            params_desc[specs["f03_name"]]["dims"] = []
            for dim in specs["object_dims"]:
                if ( isinstance(dim, str) ):
                    dim_name = re.sub("(^@|[\\(\\?\\)])", "", dim)
                    if ( not dim_name in params_list ):
                        params_list.append(dim_name)
                        params_desc[dim_name] = {
                            "type":self.f03_type["unsigned_int"],
                            "intent":"in"}
                    params_desc[specs["f03_name"]]["dims"].append(dim_name)
                else:
                    params_desc[target]["dims"].append(dim)
        params_list.append(specs["f03_name"])
        params_intent = f03_intent[specs["f03_action"]]
        params_desc[specs["f03_name"]] = {
            "type":self.f03_type[specs["type"]],
            "intent":f03_intent[specs["f03_action"]]}

        ret["params_list"] = ", ".join(params_list)
        ret["params_desc"] = ""
        for name in params_list:
            desc = params_desc[name]
            if ( len(ret["params_desc"]) > 0 ):
                ret["params_desc"] += "\n"
            ret["params_desc"] += "%s, intent(%s) :: %s" % \
                (desc["type"], desc["intent"], name)
            if ( "dims" in params_desc[specs["f03_name"]] ):
                ret["params_desc"] += "(%s)" % \
                    ", ".join(params_desc[specs["f03_name"]]["dims"])

        return ret


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
        action = specs["action"];

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
        param = specs["glue"][-1]
        if ( action == "get" ):
            param_ptr = ""
            if ( len(specs["glue"]) == 1 ):
                param_ptr = "*"
            retval += "%s%s = escdf_%s_%s_%s();" % \
                (param_ptr, param, self.group, param, action)
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
        params_string = "%s%s %s" % \
            (params_mod, self.wrapper_type[specs["type"]], target)
        for dim in params_list:
            params_string += ", %s%s %s" % \
            ( params_mod, self.wrapper_type["unsigned_int"], dim)

        # Gather info needed for params and glue code
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

        print(self.template)
        print(self.patterns.keys())


    def __str__(self):

        print("GLUE:", "glues" in self.patterns)
        return self.template.substitute(self.patterns)


                    ########################################

#
# Fortran module
#

# Fortran module default structure
f03_mod_default = """\
module escdf_@group@

    implicit none

    @interfaces@

end module escdf_@group@
"""

class EscdfFortranModule(object):

    def __init__(self, group, yaml_doc, template=None):

        self.group = group
        self.specs = EscdfSpecs(yaml_doc)
        if ( template ):
            self.template = EscdfTemplate(template)
        else:
            self.template = EscdfTemplate(f03_mod_default)
        self.fields = ["object", "object_dims", "type"]

        f03_interfaces = []
        f03_int_specs = EscdfFortranInterface(self.group)
        for elem in self.specs.get_elements():
            for action in ["get", "put"]:
                tmp_spec = self.specs.get_spec(elem)
                spec = {}
                for field in self.fields:
                    try:
                        spec[field] = tmp_spec[field]
                    except KeyError:
                        pass
                f03_interfaces.append(f03_int_specs.build_f03_interface(elem,
                    spec, action))

        self.patterns = {}
        self.patterns["group"] = self.group
        self.patterns["interfaces"] = "\n".join(f03_interfaces)


    def __str__(self):

        return self.template.substitute(self.patterns)


                    ########################################
                    ########################################

if ( __name__ == "__main__" ):
    #geo_mod = EscdfFortranModule("geometry", "escdf-specs-geometry-0.1.yml")
    #print(geo_mod)
    geo_glue = EscdfFortranGlue("geometry", "escdf-specs-geometry-0.1.yml")
    print(geo_glue)
