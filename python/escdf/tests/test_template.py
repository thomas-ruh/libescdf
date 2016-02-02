import unittest

from escdf.template import EscdfTemplate

class TestEscdfTemplate(unittest.TestCase):

    def test_substitute_default(self):

        tpl_text = "This is a @%template%@ test\n    @%test_block%@"
        tpl = EscdfTemplate(tpl_text)
        pat = {"template":"TEMPLATE", "test_block":"BLOCK"}
        txt = tpl.substitute(pat)

        assert ( txt == "This is a TEMPLATE test\n    BLOCK" )


    def test_substitute_custom(self):

        tpl_text = "This is a ##template@ test\n    ##test_block@"
        tpl = EscdfTemplate(tpl_text, start_tag="##", end_tag="@")
        pat = {"template":"TEMPLATE", "test_block":"BLOCK"}
        txt = tpl.substitute(pat)

        assert ( txt == "This is a TEMPLATE test\n    BLOCK" )
