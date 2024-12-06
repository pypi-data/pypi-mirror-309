import os
from typing import List
import anthropic
import openai

class AIManager:
    def __init__(self, model: str = "claude-3-5-sonnet-20240620"):
        self.model = model
        self.anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.openai_client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
        self.openai_endpoint = os.getenv("OPENAI_ENDPOINT", "https://api.openai.com/v1/chat/completions")

    def generate_content(self, prompt: str, output_dir: str, examples: List[str], example_contents: List[str]) -> str:
        full_prompt, system = self.construct_prompt(prompt, {
            "output_dir": output_dir,
            "examples": examples,
            "example_contents": example_contents
        })

        if self.model.startswith("claude"):
            return self._generate_with_anthropic(full_prompt, system)
        else:
            return self._generate_with_openai(full_prompt, system)

    def construct_prompt(self, user_prompt: str, context: dict) -> str:
        system_prompt = """You are FileCannon, an AI-powered file generation tool. Your task is to create new files based on examples and natural language descriptions. 
        Generate content that is practical and production-ready, following the structure and conventions shown in the example files."""

        example_contents = "\n\n".join([f"Create a file named `{ex}`.\n{self.wrap_content_in_xml(content, ex)}" for ex, content in zip(context['examples'], context['example_contents'])])

        full_prompt = f"Generate the file content and wrap it in an XML 'use_tool' structure for the write_file tool.\nExamples:\n{example_contents}\n\nUser request: {user_prompt}\nThe file path should be inside {context['output_dir']}."

        return full_prompt, system_prompt

    def _generate_with_anthropic(self, prompt: str, system: str) -> str:
        response = self.anthropic_client.messages.create(
            model=self.model,
            max_tokens=8192,
            system=system,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text

    def _generate_with_openai(self, prompt: str, system: str) -> str:
        response = self.openai_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            max_tokens=8192
        )
        return response.choices[0].message.content

    def wrap_content_in_xml(self, content: str, filename: str) -> str:
        return f"""<use_tool>
    <name>write_file</name>
    <path>{filename}</path>
    <content>
{content}
    </content>
</use_tool>"""
