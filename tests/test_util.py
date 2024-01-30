import os
import unittest

import yaml

from kai.util import Util as util


class TestUtil(unittest.TestCase):

    def test_fetch_output_and_app_yaml_folder_not_exist(self):
        result = util.fetch_output_and_app_yaml("non_existent_app")
        self.assertIsNone(result)

    def test_fetch_output_and_app_yaml_folder_exist(self):
        result = util.fetch_output_and_app_yaml("kitchensink")
        self.assertIsNotNone(result)

    def test_fetch_output_and_app_yaml_valid_input(self):
        result = util.fetch_output_and_app_yaml("kitchensink")
        self.assertIsNotNone(result)

    def test_fetch_output_and_app_yaml_invalid_input(self):
        result = util.fetch_output_and_app_yaml("sample")
        self.assertIsNone(result)

    def test_load_app_cached_violation(self):
        # Create a sample list of apps
        apps = ["eap-coolstore-monolith"]
        result = util.load_app_cached_violation(apps)
        self.assertIsInstance(result, dict)
        self.assertTrue(
            result
        )  # Check if result is not empty (non-None and non-empty dictionary)

    def test_write_cached_violations(self):
        test_cached_violations = {
            "violation_1": {
                "javaee-to-jakarta-namespaces-00001": {
                    "eap-coolstore-monolith": {
                        "webapp/WEB-INF/beans.xml": [
                            {
                                "variables": {
                                    "matchingText": "http://xmlns.jcp.org/xml/ns/javaee"
                                },
                                "line_number": 18,
                                "message": "Replace `http://xmlns.jcp.org/xml/ns/javaee` with `https://jakarta.ee/xml/ns/jakartaee` and change the schema version number ",
                            },
                            {
                                "variables": {
                                    "matchingText": "http://xmlns.jcp.org/xml/ns/javaee"
                                },
                                "line_number": 20,
                                "message": "Replace `http://xmlns.jcp.org/xml/ns/javaee` with `https://jakarta.ee/xml/ns/jakartaee` and change the schema version number ",
                            },
                            {
                                "variables": {
                                    "matchingText": "http://xmlns.jcp.org/xml/ns/javaee"
                                },
                                "line_number": 21,
                                "message": "Replace `http://xmlns.jcp.org/xml/ns/javaee` with `https://jakarta.ee/xml/ns/jakartaee` and change the schema version number ",
                            },
                        ]
                    }
                }
            },
            "violation_2": {
                "javaee-to-jakarta-namespaces-00006": {
                    "eap-coolstore-monolith": {
                        "webapp/WEB-INF/beans.xml": [
                            {
                                "variables": {"matchingText": "beans_1_1.xsd"},
                                "line_number": 21,
                                "message": 'Replace `beans_1_1.xsd` with `beans_3_0.xsd` and update the version attribute to `"3.0"`',
                            }
                        ]
                    }
                }
            },
        }
        output_directory = "samples/generated_output/incident_store"
        output_file_path = os.path.join(output_directory, "cached_violations.yaml")

        try:
            # Call the function under test
            util.write_cached_violations(test_cached_violations)

            # Check if the file was created
            print(output_file_path)
            self.assertTrue(os.path.exists(output_file_path))

            # Check if the written data matches the expected data
            with open(output_file_path, "r") as f:
                loaded_data = yaml.safe_load(f)
            self.assertEqual(loaded_data, test_cached_violations)

        finally:
            # Clean up
            if os.path.exists(output_file_path):
                os.remove(output_file_path)


if __name__ == "__main__":
    unittest.main()
