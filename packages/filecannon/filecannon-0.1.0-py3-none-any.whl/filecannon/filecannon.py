#!/usr/bin/env python3

import argparse
import os
from typing import List
from filecannon.ai_manager import AIManager
from filecannon.file_manager import FileManager
from filecannon.tool_parser import ToolParser

class FileCannon:
    def __init__(self):
        self.ai_manager = AIManager()
        self.tool_parser = ToolParser()
        self.tool_parser.register_tool('write_file', FileManager.write_file)

    def run(self, prompt: str, examples: List[str], model: str, output_dir: str):
        # Validate output directory
        if not FileManager.validate_path(output_dir):
            print(f"Error: Invalid output directory '{output_dir}'")
            return

        # Read example files
        example_contents = [FileManager.read_file(example) for example in examples]

        # Generate content using AI
        content = self.ai_manager.generate_content(prompt, output_dir, examples, example_contents)
        print("Received", content)

        # Parse the content for tool usage
        parsed_content = self.tool_parser.parse_and_execute(content)

def main():
    parser = argparse.ArgumentParser(description="filecannon: AI-powered file generation CLI tool")
    parser.add_argument("prompt", help="Description of the file to generate")
    parser.add_argument("-e", "--example", action="append", help="Path to example file(s)")
    parser.add_argument("-m", "--model", default="claude-3-5-sonnet-20240620", help="Model to use")
    parser.add_argument("-o", "--output", default=".", help="Output directory")

    args = parser.parse_args()

    filecannon = FileCannon()
    filecannon.run(args.prompt, args.example or [], args.model, args.output)

if __name__ == "__main__":
    main()
