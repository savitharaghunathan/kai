import unittest
import kai.util as util
import kai.application_hub as ApplicationHub
import kai.application_hub as Application

import unittest
import os
import yaml
import shutil

class TestUtil(unittest.TestCase):
    
    def setUp(self):
        
        # Create a temporary directory structure for testing
        self.temp_dir = "tests/temp_test_dir"
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(os.path.join(self.temp_dir, "samples", "analysis_reports", "valid_app"), exist_ok=True)
        # Create app.yaml file with test data
        app_yaml_data = {
            "repo": "https://github.com/mathianasj/eap-coolstore-monolith.git",
            "initial_branch": "main",
            "solved_branch": "quarkus-migration",
            "commit_id": None,
            "timestamp": None
        }
        with open(os.path.join(self.temp_dir, "samples", "analysis_reports", "valid_app", "app.yaml"), "w") as f:
            yaml.dump(app_yaml_data, f)
        # Create an empty output.yaml file
        open(os.path.join(self.temp_dir, "samples", "analysis_reports", "valid_app", "output.yaml"), "a").close()

    def tearDown(self):
        # Remove the temporary directory after testing
        
        shutil.rmtree(self.temp_dir)

    def test_fetch_output_and_app_yaml_folder_not_exist(self):
        u = util()
        result = u.fetch_output_and_app_yaml("non_existent_app")
        self.assertIsNone(result)
        
    def test_fetch_output_and_app_yaml_output_file_not_exist(self):
        result = util.fetch_output_and_app_yaml("existing_app_without_output")
        self.assertIsNone(result)
        
    def test_fetch_output_and_app_yaml_app_yaml_not_exist(self):
        result = util.fetch_output_and_app_yaml("existing_app_without_app_yaml")
        self.assertIsNone(result)
        
    def test_fetch_output_and_app_yaml_valid_input(self):
        result = util.fetch_output_and_app_yaml("valid_app")
        expected_output = {
            "report_path": os.path.join(self.temp_dir, "samples", "analysis_reports", "valid_app", "output.yaml"),
            "repo_path": "test_repo",
            "initial_branch": "main",
            "solved_branch": "solved",
            "commit_id": "123456",
            "timestamp": "2024-01-30"
        }
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()





