#!/usr/bin/python3

import re
import textwrap
import yaml

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
                    params_desc[specs["f03_name"]]["dims"].append(dim)
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
# Fortran module
#

# Fortran module default structure
f03_mod_default = """\
module escdf_@group@

    use iso_c_binding

    implicit none

    interface
        subroutine escdf_f03_@group@_new(@group@)
            use iso_c_binding
            implicit none
            C_F_POINTER, intent(out) :: @group@
        end subroutine escdf_f03_@group@_new
    end interface
    interface
        subroutine escdf_f03_@group@_read_metadata(@group@)
            use iso_c_binding
            implicit none
            C_F_POINTER, intent(inout) :: @group@
        end subroutine escdf_f03_@group@_read_metadata
    end interface
    interface
        subroutine escdf_f03_@group@_write_metadata(@group@)
            use iso_c_binding
            implicit none
            C_F_POINTER, intent(in) :: @group@
        end subroutine escdf_f03_@group@_write_metadata
    end interface
    interface
        subroutine escdf_f03_@group@_free(@group@)
            use iso_c_binding
            implicit none
            C_F_POINTER, intent(inout) :: @group@
        end subroutine escdf_f03_@group@_free
    end interface
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

