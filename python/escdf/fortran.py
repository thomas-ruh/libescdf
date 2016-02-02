#!/usr/bin/python3

from escdf.template import EscdfTemplate
from escdf.specs import EscdfSpecs

#
# Fortran interface
#

# Fortran interface default structure
f03_interface_default = """\
interface
    subroutine escdf_@%group%@_@%action%@_@%name%@(@%params_list%@)
        use iso_c_binding
        implicit none
        @%params_desc%@
    end subroutine escdf_@%group%@_@%action%@_@%name%@
end interface"""


class EscdfFortranInterface(object):

    def __init__(self, specs, template=None):
        """Generate a Fortran interface for a variable from a dictionary"""

        # Init
        self.specs = specs
        if ( template ):
            self.template = EscdfTemplate(template)
        else:
            self.template = EscdfTemplate(f03_interface_default)

        # Hard-coded C -> Fortran type conversion (for now) 
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

        # Hard-coded argument intents (for now)
        self.f03_intent = {"get":"inout", "put":"in"}

        # Check the consistency of the specs
        required_fields = ["action", "group", "name", "object", "type"]
        errs = [item for item in required_fields if item not in specs]
        if ( len(errs) > 0 ):
            raise KeyError("missing required fields: %s" % errs)

        # Generate Fortran source code
        f03_specs = {
            "name":specs["name"],
            "group":specs["group"],
            "action":specs["action"]}
        params_list = [self.specs["group"], self.specs["name"]]
        f03_specs["params_list"] = ", ".join(params_list)
        f03_specs["params_desc"] = "type(c_ptr), intent(%s) :: %s\n" % \
            (self.f03_intent[specs["action"]], specs["group"])
        if ( specs["object"] == "scalar" ):
            param_intent = "intent(%s)" % self.f03_intent[specs["action"]]
        else:
            param_intent = "pointer"
        f03_specs["params_desc"] += "%s, %s :: %s" % \
            (self.f03_type[specs["type"]], param_intent, specs["name"])
        f03_text = self.template.substitute(f03_specs)
        self.f03_text = self.template.wrap_fortran(f03_text)


    def __str__(self):

        return self.f03_text


                    ########################################

#
# Fortran module
#

# Fortran module default structure
f03_mod_default = """\
module escdf_@%group%@

    use iso_c_binding

    implicit none

    interface
        subroutine escdf_f03_@%group%@_new(@%group%@)
            use iso_c_binding
            implicit none
            type(c_ptr), intent(out) :: @%group%@
        end subroutine escdf_f03_@%group%@_new
    end interface
    interface
        subroutine escdf_f03_@%group%@_read_metadata(@%group%@)
            use iso_c_binding
            implicit none
            type(c_ptr), intent(inout) :: @%group%@
        end subroutine escdf_f03_@%group%@_read_metadata
    end interface
    interface
        subroutine escdf_f03_@%group%@_write_metadata(@%group%@)
            use iso_c_binding
            implicit none
            type(c_ptr), intent(in) :: @%group%@
        end subroutine escdf_f03_@%group%@_write_metadata
    end interface
    interface
        subroutine escdf_f03_@%group%@_free(@%group%@)
            use iso_c_binding
            implicit none
            type(c_ptr), intent(inout) :: @%group%@
        end subroutine escdf_f03_@%group%@_free
    end interface
    @%interfaces%@

end module escdf_@%group%@
"""

class EscdfFortranModule(object):

    def __init__(self, group, yaml_doc, template=None):

        # Init
        self.group = group
        self.specs = EscdfSpecs(self.group, yaml_doc)
        if ( template ):
            self.template = EscdfTemplate(template)
        else:
            self.template = EscdfTemplate(f03_mod_default)

        # Build Fortran interfaces
        f03_interfaces = []
        for elem in self.specs.get_elements():
            spec = self.specs.get_spec(elem)
            for action in ["get", "put"]:
                spec["action"] = action
                f03_interfaces.append("%s" % EscdfFortranInterface(spec))

        # Substitute patterns
        self.patterns = {}
        self.patterns["group"] = self.group
        self.patterns["interfaces"] = "\n".join(f03_interfaces)
        self.f03_module = self.template.substitute(self.patterns)


    def __str__(self):

        return self.f03_module

