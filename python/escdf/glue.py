#!/usr/bin/python3

from escdf.template import EscdfTemplate
from escdf.specs import EscdfSpecs


#
# Fortran wrapper
#

# Default Fortran wrapper structure
f03_wrapper_default = """\
void escdf_f03_@%group%@_@%action%@_@%name%@(
        @%params%@) {
    @%glue_code%@
}"""


class EscdfFortranWrapper(object):

    def __init__(self, specs, template=None):

        # Init
        self.specs = specs
        if ( template ):
            self.template = EscdfTemplate(template)
        else:
            self.template = EscdfTemplate(f03_wrapper_default)

        # Hard-coded specs -> C type conversion (for now)
        self.wrap_type = {
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

        # Check consistency of specs
        required_fields = ["action", "group", "name", "object", "type"]
        errs = [item for item in required_fields if item not in specs]
        if ( len(errs) > 0 ):
            raise KeyError("missing required fields: %s" % errs)

        # Generate wrapper code
        wrap_specs = {
            "name":specs["name"],
            "group":specs["group"],
            "action":specs["action"]}
        params = "escdf_%s_t *%s, %s *%s" % \
            (specs["group"], specs["group"], self.wrap_type[specs["type"]],
            specs["name"])
        wrap_specs["params"] = params
        glue_ptr = ""
        if ( specs["object"] == "scalar" ):
            glue_ptr = "*"
        if ( specs["action"] == "read" ):
            if ( specs["spec_type"] == "metadata" ):
                glue_code = "*%s = %s.%s;" % \
                    (specs["name"], specs["group"], specs["name"])
            else:
                glue_code = "%s%s = escdf_%s_%s_%s();" % \
                    (glue_ptr, specs["name"], specs["group"],
                    specs["action"], specs["name"])
        elif ( specs["action"] == "write" ):
            glue_code = "escdf_%s_%s_%s(%s%s);" % \
                (specs["group"], specs["action"], specs["name"], glue_ptr,
                specs["name"])
        else:
            raise NotImplementedError("unknown action '%s'" % specs["action"])
        wrap_specs["glue_code"] = glue_code
        self.wrapper_text = self.template.substitute(wrap_specs)


    def __str__(self):

        return self.wrapper_text


                    ########################################

#
# C -> Fortran glue code
#

# Glue code default structure
f03_glue_default = """\
/* C -> Fortran 2003 glue code for @group@ - machine-generated */

void escdf_f03_@%group%@_new(escdf_@%group%@_t *@%group%@) {
    @%group%@ = escdf_@%group%@_new(choke_me, choke_me);
}
void escdf_f03_@%group%@_read_metadata(escdf_@%group%@_t *@%group%@) {
    escdf_@%group%@_read_metadata(@%group%@);
}
void escdf_f03_@%group%@_write_metadata(escdf_@%group%@_t *@%group%@) {
    escdf_@%group%@_write_metadata(@%group%@);
}
void escdf_f03_@%group%@_free(escdf_@%group%@_t *@%group%@) {
    escdf_@%group%@_free(@%group%@);
}
@%wrappers%@
"""


class EscdfFortranGlue(object):

    def __init__(self, group, yaml_doc, template=None):

        # Init
        self.group = group
        self.specs = EscdfSpecs(self.group, yaml_doc)
        if ( template ):
            self.template = EscdfTemplate(template)
        else:
            self.template = EscdfTemplate(f03_glue_default)

        # Build Fortran wrappers
        f03_wrappers = []
        for elem in self.specs.get_elements():
            spec = self.specs.get_spec(elem)
            for action in ["read", "write"]:
                spec["action"] = action
                f03_wrappers.append("%s" % EscdfFortranWrapper(spec))

        # Substitute patterns
        self.patterns = {}
        self.patterns["group"] = self.group
        self.patterns["wrappers"] = "\n".join(f03_wrappers)
        self.f03_glue = self.template.substitute(self.patterns)


    def __str__(self):

        return self.f03_glue

