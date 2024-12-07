"""Prompt library module."""
from typing import Dict

from pathlib import Path
import os
import json


class PromptLibrary:
    """
    Prompt library is a prompt generation manager class.
    It loads prompts from local directory and also loads placeholder dictionaries.
    It provides a method to generate complete prompts.
    """

    def __init__(self, path_to_library: Path):
        self._load_library(path_to_library)

    def _load_library(self, path_to_library: Path):
        self.library = {}
        prompt_types = [f for f in os.listdir(path_to_library) if os.path.isdir(path_to_library / f)]
        for prompt_type in prompt_types:
            self.library[prompt_type] = {}
            prompt_subtypes = [f for f in os.listdir(path_to_library / prompt_type)
                               if os.path.isdir(path_to_library / prompt_type / f)]
            print(prompt_type, ": ", prompt_subtypes)
            for prompt_subtype in prompt_subtypes:
                self.library[prompt_type][prompt_subtype] = {}
                self._load_prompt(path_to_library, prompt_type, prompt_subtype)
        print(self.library)

    def _load_prompt(self, path_to_library: Path, prompt_type: str, prompt_subtype: str):
        files = os.listdir(path_to_library / prompt_type / prompt_subtype)
        print(files)
        for file in files:
            if file == 'placeholders.json':
                with open(path_to_library / prompt_type / prompt_subtype / file) as f:
                    placeholders = json.load(f)
                    self.library[prompt_type][prompt_subtype]['placeholders'] = placeholders
            elif '.txt' in file:
                with open(path_to_library / prompt_type / prompt_subtype / file) as f:
                    prompt = f.read()
                    self.library[prompt_type][prompt_subtype]['prompt'] = prompt

    def create_prompt(self, prompt: str, placeholders: Dict[str, str]) -> str:
        """
        Main function of PromptLibrary class.
        Creates a prompt by replacing placeholders in the prompt template text.

        Args:
            prompt: prompt template.
            placeholders: dictionary of placeholders keys and values.

        Returns:
            str: complete prompt.

        """
        result = prompt
        for placeholder in placeholders.keys():
            result = result.replace(placeholder, str(placeholders[placeholder]))
        return result


prompt_library = PromptLibrary(Path(__file__).parent / 'library')

if __name__ == '__main__':
    # prompt_library = PromptLibrary(Path(__file__).parent / 'library')
    # print(prompt_library.create_prompt(prompt_library.library['preprocessing']['carrier']['prompt'],
    #                                    prompt_library.library['preprocessing']['carrier']['placeholders']))
    print(prompt_library.create_prompt(prompt_library.library['bookingConfirmation']['hapag-lloyd']['prompt'],
                                       prompt_library.library['bookingConfirmation']['hapag-lloyd']['placeholders']))
