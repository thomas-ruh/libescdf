import unittest
import yaml

from escdf.specs import EscdfSpecs

# Fake specifications for the tests
escdf_basic_specs = """\
%YAML 1.2
---

metadata1:
    object: scalar
    type: unsigned_int
    spec_type: metadata
metadata2:
    object: scalar
    type: unsigned_int
    spec_type: metadata
metadata3:
    object: scalar
    type: unsigned_int
    spec_type: metadata
dataset1:
    object: array
    object_dims: ["@metadata1", 2, 3]
    type: double
    spec_type: metadata
dataset2:
    object: array
    object_dims: [5]
    type: int
    spec_type: metadata
dataset3:
    object: varying_array
    object_dims: [3, "@metadata2", "@dataset2(?)"]
    type: float
    spec_type: metadata

"""

class TestEscdfSpecs(unittest.TestCase):

    def test_init_loads_text(self):

        specs = EscdfSpecs(escdf_basic_specs)
        yaml_data = yaml.load(escdf_basic_specs)
        assert ( len(yaml_data.keys()) == len(specs.yaml_data) )


    def test_elts_matches_yaml(self):

        specs = EscdfSpecs(escdf_basic_specs)
        chk_elts = list(set(specs.elts + specs.yaml_data.keys()))
        assert ( (len(chk_elts) == len(specs.elts)) and \
                 (len(chk_elts) == len(specs.yaml_data.keys())) )


    def test_get_spec_sets_name(self):

        specs = EscdfSpecs(escdf_basic_specs)
        assert ( "name" in specs.get_spec("metadata1") )


    def test_is_ref_detects_refs(self):

        specs = EscdfSpecs(escdf_basic_specs)
        assert ( (not specs.is_ref("metadata1")) and \
                 (specs.is_ref("@metadata1")) and \
                 (specs.is_ref("@dataset2(?)")) and \
                 (not specs.is_ref("@wrong_ref")) )


    def test_is_ref_fixed_works(self):

        specs = EscdfSpecs(escdf_basic_specs)
        assert ( (specs.is_ref_fixed("@metadata1")) and \
                 (not specs.is_ref_fixed("@dataset2(?)")) and \
                 (not specs.is_ref_fixed("@wrong_ref")) )


    def test_is_ref_varying_works(self):

        specs = EscdfSpecs(escdf_basic_specs)
        assert ( (specs.is_ref_varying("@dataset2(?)")) and \
                 (not specs.is_ref_varying("@metadata1")) and \
                 (not specs.is_ref_varying("@wrong_ref")) )

