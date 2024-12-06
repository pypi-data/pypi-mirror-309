import re
import xml.etree.ElementTree as ET
from typing import Callable, Any

class ToolParser:
    def __init__(self):
        self.tools: Dict[str, Callable] = {}

    def register_tool(self, name: str, func: Callable):
        """Register a tool function with a name."""
        self.tools[name] = func

    def parse_and_execute(self, input_string: str) -> Any:
        """Extract XML from input string and execute the corresponding tool."""
        try:
            # Use regex to extract the XML content
            match = re.search(r'(<use_tool.*?>.*?</use_tool>)', input_string, re.DOTALL)
            if not match:
                raise ValueError("No valid XML found in input")
            xml_string = match.group(1)

            root = ET.fromstring(xml_string)
            if root.tag != 'use_tool':
                raise ValueError("Root element must be 'use_tool'")

            tool_name_elem = root.find('name')
            if tool_name_elem is None or tool_name_elem.text is None:
                raise ValueError("Missing tool name in XML")

            tool_name = tool_name_elem.text.strip()
            if tool_name not in self.tools:
                raise ValueError(f"Unknown tool: {tool_name}")

            args = {}
            for child in root:
                if child.tag != 'name':
                    args[child.tag] = child.text.strip() if child.text else ''

            return self.tools[tool_name](**args)
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML format: {e}")
        except AttributeError as e:
            raise ValueError(f"Missing required XML elements: {e}")

    def generate_xml(self, tool_name: str, **kwargs) -> str:
        """Generate XML string for a tool call."""
        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")

        root = ET.Element('use_tool')
        name_elem = ET.SubElement(root, 'name')
        name_elem.text = tool_name

        for key, value in kwargs.items():
            elem = ET.SubElement(root, key)
            elem.text = str(value)

        return ET.tostring(root, encoding='unicode')

# Example usage:
if __name__ == "__main__":
    def write_file(path: str, content: str) -> bool:
        print(f"Writing to {path}:")
        print(content)
        return True

    parser = ToolParser()
    parser.register_tool('write_file', write_file)

    # Input string with extra text
    input_string = """
    Certainly! I'll create a copy of the example `requirements.txt` file, but place it inside the `tmp` directory as requested. Here's the file content wrapped in the XML 'use_tool' structure for the write_file tool:

    <use_tool>
        <name>write_file</name>
        <path>tmp/requirements.txt</path>
        <content>
    anthropic>=0.6.0
    openai>=1.0.0
    lxml>=5.3.0

        </content>
    </use_tool>

    This will create a file named `requirements.txt` inside the `tmp` directory with the same content as the example. The file will contain the required Python packages and their minimum versions, which are:

    1. anthropic, version 0.6.0 or higher
    2. openai, version 1.0.0 or higher
    3. lxml, version 5.3.0 or higher

    The file is now ready to be used for testing purposes.
    """

    # Parse and execute
    result = parser.parse_and_execute(input_string)
    print(f"Execution result: {result}")
