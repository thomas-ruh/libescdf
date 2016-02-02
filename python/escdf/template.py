#!/usr/bin/python3

import re
import textwrap


class EscdfTemplate(object):

    def __init__(self, text, start_tag="@%", end_tag="%@"):

        # Init
        self.text = text
        self.start_tag = start_tag
        self.end_tag = end_tag
        self.re_newline = re.compile(r"\n", flags=re.MULTILINE+re.DOTALL)

        # Find keywords in template
        re_keywords = re.compile("%s([a-z0-9_]+)%s" % \
            (self.start_tag, self.end_tag), flags=re.MULTILINE)
        self.keywords = re_keywords.findall(self.text)
        if ( self.keywords ):
            self.keywords = list(set(self.keywords))
        else:
            self.keywords = []

        # Find indentation levels of substituted blocks
        # Note: there might be unindented keywords in the template,
        #       hence the use of another keywords variable here.
        # TODO: inline keywords can be many, but block keywords
        #       (i.e. when alone in a line) must be unique.
        self.indents = {}
        re_indent = re.compile("^([ ]+)%s([a-z0-9_]+)%s$" % \
            (self.start_tag, self.end_tag), flags=re.MULTILINE)
        indents = list(set(re_indent.findall(self.text)))
        if ( (len(self.keywords) > 0) and (len(indents) > 0) ):
            offsets, patterns = zip(*indents)
            for word in self.keywords: 
                chk_word = [idx for idx, kwd in enumerate(patterns) \
                    if kwd == word]
                if ( len(chk_word) > 1 ):
                    raise NameError(
                        "ambiguous definition of '%s' in template" % name)
                elif ( len(chk_word) == 0 ):
                    self.indents[word] = 0
                else:
                    self.indents[word] = len(offsets[chk_word[0]])


    def check_patterns(self, specs):

        errs = [item for item in self.keywords if not item in specs]
        if ( len(errs) > 0 ):
            raise KeyError("missing input keywords: %s" % errs)
        errs = [item for item in specs if not item in self.keywords]
        if ( len(errs) > 0 ):
            raise KeyError("extra input keywords: %s" % errs)


    def reindent(self, keyword, value):

        if ( self.re_newline.search(value) ):
            try:
                sep = "\n" + " " * self.indents[keyword]
            except KeyError:
                sep = "\n"
            return sep.join(value.split("\n"))
        else:
            return value


    def substitute(self, specs):

        retval = self.text
        for kwd, val in specs.items():
            retval = re.sub("%s%s%s" % \
                (self.start_tag, kwd, self.end_tag),
                self.reindent(kwd, val), retval)

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

