# -*- utf-8 -*-
import pdb

import unittest
from plone.recipe.codeanalysis.csslint import code_analysis_csslint
from mock import MagicMock
from mock import patch


class TestCssLint(unittest.TestCase):
    @patch('subprocess.Popen')
    def test_analysis_should_return_false(self, mock_class):
        mock_class().communicate = MagicMock(
            return_value=(' x Error - x ', 'IGNORED ERR',)
        )
        from subprocess import Popen
        options = {'csslint-bin': 'FAKE_EXECUTABLE',
                   'directory': 'FAKE_DIRECTORY',
                   'jenkins': 'False'}
        self.assertFalse(code_analysis_csslint(options))

    @patch('subprocess.Popen')
    def test_analysis_should_return_true(self, mock_class):
        mock_class().communicate = MagicMock(
            return_value=(' x (W000) x ', 'IGNORED ERR',)
        )
        # import pdb; pdb.set_trace()
        from subprocess import Popen
        options = {'csslint-bin': 'FAKE_EXECUTABLE',
                   'directory': 'FAKE_DIRECTORY',
                   'jenkins': 'False'}
        self.assertTrue(code_analysis_csslint(options))
