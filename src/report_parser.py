import re
import os
from typing import Dict, List, Optional, Tuple
from agents.controller_agent import ControllerAgent
from agents.service_agent import ServiceAgent

class ReportsParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.controller_prompt = None

    def read_file(self) -> str:
        try:
            with open(self.file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found.")
            return ""
        except Exception as e:
            print(f"Error reading file: {e}")
            return ""

    def parse_reports(self, content: str):
        """
        Parse the reports from the content.
        """
        # self.controller_prompt = self.controller_parser(content)
        # print(self.controller_prompt)
        self.service_prompt = self.service_parser(content)
        print(self.service_prompt)

    def controller_parser(self, content: str):
        """
        Parse the controller from the content.  
        """
        try:
            controller_start = content.find("Controller\n***") + len("Controller\n***")
            controller_end = content.find("\n***", controller_start)
            
            if controller_start < len("Controller\n***"):
                # "Controller\n***" not found in content
                print("Warning: Controller section not found in the content")
                return ""
                
            if controller_end == -1:
                # End marker not found, use the rest of the content
                print("Warning: End marker for Controller section not found, using rest of content")
                controller_code = content[controller_start:].strip()
            else:
                controller_code = content[controller_start:controller_end].strip()
            controller_agent = ControllerAgent()
            controller_prompt = controller_agent.prompt(controller_code)
            return controller_prompt
        except Exception as e:
            print(f"Error parsing controller section: {e}")
            return ""

    def service_parser(self, content: str):
        """
        Parse the service from the content.
        """
        service_start = content.find("service\n***") + len("service\n***")
        service_end = content.find("\n***", service_start)
        service_code = content[service_start:service_end].strip()
        service_agent = ServiceAgent()
        service_prompt = service_agent.prompt(service_code)
        return service_prompt

    def repo_parser(self, content: str):
        """
        Parse the repo from the content.
        """
        repo_start = content.find("repository\n***") + len("repository\n***")
        repo_end = content.find("\n***", repo_start)
        repo_code = content[repo_start:repo_end].strip()
        return repo_code
    
    def other_parser(self, content: str):
        """
        Parse the other from the content.
        """
        other_start = content.find("other\n***") + len("other\n***")
        other_end = content.find("\n***", other_start)
        other_code = content[other_start:other_end].strip()
        return other_code
    

def main():
    """
    Main function to run the code segregator.
    """
    import argparse

    parser = argparse.ArgumentParser(description='Parse reports.')
    parser.add_argument('report_file', help='Path to the report file')
    args = parser.parse_args()

    reports_parser = ReportsParser(args.report_file)
    content = reports_parser.read_file()
    
    if content:
        reports_parser.parse_reports(content)

if __name__ == "__main__":
    main() 
