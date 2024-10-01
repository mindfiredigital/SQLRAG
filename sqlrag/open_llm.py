"""
This module provides an interface for interacting with open-source
large language models (LLMs) using the `gpt4all` package.

It defines the `OpenLLM` class which allows for:
- Loading and interacting with LLM models.
- Listing supported models and GPUs for execution.
- Generating responses based on a given input using the selected model.
"""

import gpt4all


class OpenLLM:
    """
    A class to interact with open-source large language models (LLMs) using gpt4all.

    Methods:
    --------
    list_models() -> list[dict]
        Returns a list of available models supported by gpt4all with descriptions.

    list_gpus() -> list[str]
        Returns a list of available GPUs detected by the system.

    invoke(input: list, max_tokens: int = 3000) -> str
        Generates a response based on the provided prompt and returns it as a string.
    """

    def __init__(
        self, model_name: str = "Meta-Llama-3-8B-Instruct.Q4_0.gguf", device="cpu"
    ):
        """
        Initializes the OpenLLM class with the specified model.

        Args:
        -----
        model_name : str, optional
            Name of the model supported by gpt4all. The default is
            'Meta-Llama-3-8B-Instruct.Q4_0.gguf'.
            Use the `list_models()` method to get the full list of supported models and
            descriptions.

        device : str, optional
            The device to run the model on, such as 'cpu' or 'gpu'. Defaults to 'cpu'.
        """

        self.model = gpt4all.GPT4All(model_name=model_name, device=device)

    @staticmethod
    def list_models() -> list[dict]:
        """
        Returns a list of models supported by gpt4all along with their descriptions.

        Returns:
        --------
        list[dict]:
            A list of dictionaries, where each dictionary contains details about a supported model.
        """

        return gpt4all.GPT4All.list_models()

    @staticmethod
    def list_gpus() -> list[str]:
        """
        Returns a list of available GPUs detected by the system.

        Returns:
        --------
        list[str]:
            A list of strings representing the available GPUs.
        """
        return gpt4all.GPT4All.list_gpus()

    def invoke(self, data: list, max_tokens: int = 3000) -> str:
        """
        Generates a response from the selected LLM based on the given prompt.

        Args:
        -----
        data : list
            A list where the first element contains the user data content for the LLM.

        max_tokens : int, optional
            The maximum number of tokens to generate. Default is 3000.

        Returns:
        --------
        str:
            The generated response from the LLM.
        """

        prompt = data[0].content
        response = self.model.generate(prompt, max_tokens=max_tokens)
        return response
