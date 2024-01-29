# This file contains utility functions that are used by the kai application

import os
import yaml

from kai.application_hub import Application, ApplicationHub
from kai.report import Report

class Util:
    def fetch_output_and_app_yaml(app_name):
        """
        Fetches the output.yaml file path and loads the contents of app.yaml
        for the given app name.
        """
        # Path to the analysis_reports directory
        analysis_reports_dir = "samples/analysis_reports"
        
        # Check if the specified app folder exists
        app_folder = os.path.join(analysis_reports_dir, app_name)
        if not os.path.exists(app_folder):
            print(f"Error: {app_name} does not exist in the analysis_reports directory.")
            return None
        
        # Path to the output.yaml file
        output_yaml_path = os.path.join(app_folder, "output.yaml")
        
        # Check if output.yaml exists for the specified app
        if not os.path.exists(output_yaml_path):
            print(f"Error: output.yaml does not exist for {app_name}.")
            return None
        
        # Load contents of app.yaml
        app_yaml_path = os.path.join(app_folder, "app.yaml")
        if not os.path.exists(app_yaml_path):
            print(f"Error: app.yaml does not exist for {app_name}.")
            return None
        
        with open(app_yaml_path, "r") as app_yaml_file:
            app_yaml_content = yaml.safe_load(app_yaml_file)
        
        # Create a dictionary with file_path and repo keys
        output = {
            "report_path": output_yaml_path,
            "repo_path": app_yaml_content.get("repo", ""),
            "initial_branch": app_yaml_content.get("initial_branch", ""),
            "solved_branch": app_yaml_content.get("solved_branch", ""),
            "commit_id": app_yaml_content.get("commit_id", ""),
            "timestamp": app_yaml_content.get("timestamp", "")

        }
        
        return output

    def load_app_cached_violation(apps):
        """
        Load the incident store with the given applications
        """
        application_hub = ApplicationHub()
        print(f"Loading incident store with {len(apps)} applications\n")
        for app in apps:
            print(f"Loading application {app}\n")
            app_variables = Util.fetch_output_and_app_yaml(app)
            report = Report(app_variables["report_path"])
            formatted_report = report._read_report()
            a = Application(app, formatted_report, app_variables["repo_path"], app_variables["initial_branch"], app_variables["solved_branch"], app_variables["commit_id"], app_variables["timestamp"])
            application_hub.add_application(a)
        return application_hub.cached_violations


    def write_cached_violations(cached_violations):
        """
        Write the cached_violations to a file for later use
        """

        output_directory = "samples/generated_output/incident_store"
        os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist
        output_file_path = os.path.join(output_directory, "cached_violations.yaml")
        
        print(f"Writing incident store to file: {output_file_path}")

        with open(output_file_path, 'w') as f:
            yaml.dump(cached_violations, f)
        print(f"Written cached_violations to {output_file_path}\n")

    
    # todo: update cached_violations with the new application
        
    
    # determine if new application analysis report is available
    def is_new_analysis_report_available(application):
        # query hub api for the application
        # if the timestamp is newer than the current timestamp
        # return true
        # else return false
        app1 = ApplicationHub.get_app_from_konveyor_hub(application.name)
        if app1 is not None:
            if app1.timestamp > application.timestamp:
                return app1.timestamp
        return None
    
    # update the timestamp in app.yaml if new analysis report is available
    def update_timestamp(application):
        # query hub api for the application
        # if the timestamp is newer than the current timestamp
        # update the timestamp in app.yaml
        # return true
        # else return false
        if Util.is_new_analysis_report_available(application) is not None:
            # update the timestamp in app.yaml
            # Path to the analysis_reports directory
            analysis_reports_dir = "samples/analysis_reports"
            
            # Check if the specified app folder exists
            app_folder = os.path.join(analysis_reports_dir, application.name)
            if not os.path.exists(app_folder):
                print(f"Error: {application.name} does not exist in the analysis_reports directory.")
                return False
                
            # Load contents of app.yaml
            app_yaml_path = os.path.join(app_folder, "app.yaml")
            if not os.path.exists(app_yaml_path):
                print(f"Error: app.yaml does not exist for {application.name}.")
                return False
            # open the file in write mode and update the timestamp field
            with open(app_yaml_path, "r") as app_yaml_file:
                app_yaml_data = yaml.safe_load(app_yaml_file)
            
            # Update the timestamp in the app.yaml data
            app_yaml_data["timestamp"] = application.timestamp
            
            # Write the updated contents back to app.yaml
            with open(app_yaml_path, "w") as app_yaml_file:
                yaml.dump(app_yaml_data, app_yaml_file)
            
            # Return true
            return True
        return False
    
    