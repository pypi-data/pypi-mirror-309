from typing import Optional, Dict, Any
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer


class LLM:
    def __init__(
        self,
        model_category: str,
        model_name: str,
        api_key: Optional[str] = None,
        model_parameters: Optional[Dict[str, Any]] = None,
        local_model_path: Optional[str] = None
    ):
        """
        Initialize the LLM client with default token length configurations.

        Parameters
        ----------
        model_category : str
            The name of the language model provider (e.g., 'openai', 'huggingface', 'cohere').
        model_name : str
            The name of the model.
        api_key : str, optional
            The API key for the selected provider.
        model_parameters : dict, optional
            Additional parameters for model configuration.
        local_model_path : str, optional
            Path to a fine-tuned model directory.
        """
        self.model_category = model_category.lower()
        self.model_name = model_name.lower() if model_name else None
        self.api_key = api_key
        self.local_model_path = local_model_path

        # Default parameters
        default_params = {
            "max_length": 600,
            "temperature": 0.7
        }

        # Merge default parameters with provided parameters
        base_parameters = {**default_params, **(model_parameters or {})}

        # Map the parameters based on the model category
        self.model_parameters = self._map_config_parameters(base_parameters)

        # Initialize the language model
        self.model = self._initialize_llm()

    def _map_config_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map configuration parameters to provider-specific format.

        Parameters
        ----------
        params : dict
            Input parameters to map.

        Returns
        -------
        dict
            Mapped parameters for specific provider.
        """
        mapped_params = params.copy()

        if self.model_category == "openai":
            # OpenAI uses max_tokens instead of max_new_tokens
            if "max_new_tokens" in mapped_params:
                mapped_params["max_tokens"] = mapped_params.pop(
                    "max_new_tokens")
            # OpenAI doesn't use max_length
            mapped_params.pop("max_length", None)

        elif self.model_category == "huggingface":
            # Set truncation to True
            mapped_params["truncation"] = True

        elif self.model_category == "cohere":
            # Cohere uses max_tokens instead of max_new_tokens
            if "max_new_tokens" in mapped_params:
                mapped_params["max_tokens"] = mapped_params.pop(
                    "max_new_tokens")
            # Cohere doesn't use max_length
            mapped_params.pop("max_length", None)

        return mapped_params

    def _initialize_llm(self):
        """
        Initialize the language model based on the specified category.

        Returns
        -------
        object
            An instance of the selected language model.

        Raises
        ------
        ValueError
            If the specified model category is unsupported.
        """
        if self.model_category == "openai":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                openai_api_key=self.api_key,
                model_name=self.model_name or "gpt-3.5-turbo",
                **self.model_parameters
            )

        elif self.model_category == "huggingface":
            from langchain_huggingface import HuggingFacePipeline
            # Check if a local model path is provided
            if self.local_model_path:
                # Load the fine-tuned model and tokenizer from local directory
                model = AutoModelForCausalLM.from_pretrained(
                    self.local_model_path)
                tokenizer = AutoTokenizer.from_pretrained(
                    self.local_model_path)
                return pipeline("text-generation", model=model, tokenizer=tokenizer, **self.model_parameters)
            else:
                # Load the model from Hugging Face hub
                return HuggingFacePipeline.from_model_id(
                    model_id=self.model_name,
                    task="text-generation",
                    pipeline_kwargs=self.model_parameters
                )

        elif self.model_category == "cohere":
            from langchain_community.llms import Cohere
            return Cohere(
                cohere_api_key=self.api_key,
                model=self.model_name,
                **self.model_parameters
            )
        else:
            raise ValueError(
                f"Unsupported model category: {self.model_category}")

    def generate(self, prompt: str) -> str:
        """
        Generate a response from the language model.

        Parameters
        ----------
        prompt : str
            The input prompt for the LLM.

        Returns
        -------
        str
            Generated text from the LLM.
        """
        response = self.model.invoke(prompt)
        return response.content if hasattr(response, 'content') else response
