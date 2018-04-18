# -*- coding: utf-8 -*-
"""Utils for the docsitalia app."""

from __future__ import absolute_import
from __future__ import unicode_literals

import yaml


def load_yaml(txt):
    """Helper for yaml parsing"""
    try:
        return yaml.safe_load(txt)
    except yaml.YAMLError as exc:
        note = ''
        if hasattr(exc, 'problem_mark'):
            mark = exc.problem_mark
            note = ' (line %d, column %d)' % (mark.line + 1, mark.column + 1)
        raise ValueError(
            "The file could not be loaded, "
            "possibly due to a syntax error%s" % (
                note,))
