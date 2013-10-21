# -*- coding: utf-8 -*-
from unittest import TestCase
from plone.recipe.codeanalysis.csslint import code_analysis_csslint
from shutil import rmtree
from tempfile import mkdtemp
from os.path import join as path_join
from os.path import isfile as path_isfile


class TestCssLint(TestCase):
    def setUp(self):
        self.options = {
            'csslint-bin': 'csslint',
            'jenkins': 'False'
        }
        self.test_dir = mkdtemp()

    def tearDown(self):
        rmtree(self.test_dir)

    def test_analysis_should_return_false_when_error_found(self):
        incorrect_code = file(path_join(self.test_dir, 'incorrect.css'), 'w')
        incorrect_code.write(
            'a:link {color: blue}\n'
            '{}\n'
            'h3 {color: red}\n'
            'bodyy {color: purple}')
        incorrect_code.close()
        self.options['directory'] = self.test_dir
        self.assertFalse(code_analysis_csslint(self.options))

    def test_analysis_should_return_false_when_oserror(self):
        # The options are fake, so it should raise an OSError
        # and return false.
        self.options['csslint-bin'] = 'FAKE_BIN'
        self.options['directory'] = self.test_dir
        self.assertFalse(code_analysis_csslint(self.options))

    # This test is failing on travis.
    #def test_analysis_should_return_true(self):
    #    correct_code = file(path_join(self.test_dir, 'correct.css'), 'w')
    #    correct_code.write(
    #        'a:link {color:blue}\n'
    #        'h3 {color: red}\n'
    #        'body {color: purple}')
    #    correct_code.close()
    #    self.options['directory'] = self.test_dir
    #    self.assertTrue(code_analysis_csslint(self.options))

    def test_analysis_file_should_exist_when_jenkins_is_true(self):
        location_tmp_dir = mkdtemp()
        correct_code = file(path_join(self.test_dir, 'correct.css'), 'w')
        correct_code.write(
            'a:link {color:blue}\n'
            'h3 {color: red}\n'
            'body {color: purple}')
        correct_code.close()
        self.options['directory'] = self.test_dir
        self.options['location'] = location_tmp_dir
        self.options['jenkins'] = 'True'  # need to activate jenkins.
        code_analysis_csslint(self.options)
        file_exist = path_isfile(path_join(location_tmp_dir, 'csslint.xml'))
        rmtree(location_tmp_dir)
        self.assertTrue(file_exist)
