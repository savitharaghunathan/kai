import unittest
from kai.util import Util as util
import kai.application_hub as ApplicationHub
import kai.application_hub as Application

import unittest
import os
import yaml
import shutil

class TestUtil(unittest.TestCase):
    
    

    def test_fetch_output_and_app_yaml_folder_not_exist(self):
        result = util.fetch_output_and_app_yaml("non_existent_app")
        self.assertIsNone(result)
        
        
    def test_fetch_output_and_app_yaml_valid_input(self):
        result = util.fetch_output_and_app_yaml("kitchensink")
        expected_output = {
            "report_path": "samples/analysis_reports/kitchensink/output.yaml",
            "repo_path": "https://github.com/tqvarnst/jboss-eap-quickstarts.git",
            "initial_branch": "7.1",
            "solved_branch": "quarkus-3.2",
            "commit_id": None,
            "timestamp": None
        }
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()





