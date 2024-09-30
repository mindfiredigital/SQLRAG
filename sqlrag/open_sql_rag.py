"""
sqlrag.open_sql_rag

This module implements the core functionality of SQLRAG,
allowing users to query databases using natural language,
and generate SQL code and visualizations as output.
SQLRAG supports both open-source and OpenAI models and integrates Redis for caching results.
The module also provides GPU support for open-source models and allows for model flexibility
based on user input.

Classes:
    OpenSQLRAG: Main class for handling natural language database querying and
    data visualization using LLMs.

Methods:
    __init__: Initializes the OpenSQLRAG instance with database, LLM, Redis caching,
              and chart generation capabilities.
    _get_prompt_template: Retrieves the appropriate prompt template for SQL generation based
                          on the LLM model type.
    _get_chart_template: Retrieves the appropriate template for chart generation based on
                         the LLM model type.
    _get_model: Selects the LLM model to be used, either OpenAI or open-source.
    get_gpus_list: Returns the list of available GPUs for open-source models.
    get_open_source_models: Retrieves the list of supported open-source models with their
                            specifications.
    generate_code_and_sql: Generates SQL queries and chart code based on user input and caches
                           the results in Redis.
"""

import time
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate
from dotenv import load_dotenv
from .cache import redis_cache
from .constants import (
    PROMPT_TEMPLATE,
    CHART_PROMPT_TEMPLATE,
    ALLOWED_CHART_TYPES,
    PROMPT_TEMPLATE_LLAMA,
    CHART_PROMPT_TEMPLATE_LLAMA,
)
from .utils import extract_sql_query, extract_code_response
from .exceptions import InvalidInputError
from .open_llm import OpenLLM

load_dotenv(".env")


class OpenSQLRAG:
    """
    OpenSQLRAG class allows users to generate SQL queries from natural language
    prompts and visualize the query results using Python Matplotlib or JavaScript
    Chart.js. It supports both OpenAI models and open-source LLMs like GPT4All.

    Attributes:
        db: The SQLDatabase object for connecting to the database.
        model_name: The name of the LLM model (OpenAI or open-source) to use.
        device: The device type ("cpu" or "gpu") for running open-source models.
        is_openai: A boolean flag to determine whether to use OpenAI models or not.
        llm: The selected LLM model for processing prompts.
        schema: The schema of the connected database.
        redis_client: The Redis client for caching query results.
        top_k: The number of top results to retrieve when generating SQL queries.
        prompt_template: The template used for generating SQL query prompts.
        chart_prompt_template: The template used for generating chart code.
    """

    def __init__(
        self,
        db_uri: str,
        model_name: str = "gpt-3.5-turbo-0125",
        device: str = "cpu",
        top_k: int = 5,
        is_openai: bool = True,
        redis_host: str = "localhost",
        redis_port: int = 6379,
    ) -> None:
        """
        Initializes the OpenSQLRAG instance.

        Args:
            db_uri (str): The URI of the database to connect to.
            model_name (str): The name of the LLM model (default: "gpt-3.5-turbo-0125").
            device (str): The device type to run open-source models on ("cpu" or "gpu").
            top_k (int): The number of top results to retrieve for SQL generation (default: 5).
            is_openai (bool): Whether to use OpenAI models (default: True).
            redis_host (str): The Redis server hostname (default: 'localhost').
            redis_port (int): The Redis server port (default: 6379).
        """

        self.db = SQLDatabase.from_uri(db_uri)
        self.model_name = model_name
        self.device = device
        self.is_openai = is_openai
        self.llm = self._get_model(is_openai)
        self.schema = self.db.get_table_info()
        self.redis_client = redis_cache(redis_host, redis_port)
        self.top_k = top_k
        self.prompt_template = PromptTemplate(
            input_variables=["dialect", "top_k", "schema", "query"],
            template=self._get_propmt_template(),
        )

        self.chart_prompt_template = PromptTemplate(
            input_variables=["chart_type", "chart_data"],
            template=self._get_chart_template(),
        )

    def _get_propmt_template(self) -> str:
        """
        Retrieves the prompt template for SQL generation based on the LLM model.

        Returns:
            str: The appropriate SQL prompt template based on whether the model
                 is OpenAI or an open-source LLM.
        """

        if self.is_openai:
            return PROMPT_TEMPLATE

        if self.model_name.startswith("Meta-Llama"):
            return PROMPT_TEMPLATE_LLAMA
        return PROMPT_TEMPLATE

    def _get_chart_template(self) -> str:
        """
        Retrieves the chart generation prompt template based on the LLM model.

        Returns:
            str: The appropriate chart prompt template based on whether the model
                 is OpenAI or an open-source LLM.
        """

        if self.is_openai:
            return CHART_PROMPT_TEMPLATE

        if self.model_name.startswith("Meta-Llama"):
            return CHART_PROMPT_TEMPLATE_LLAMA
        return CHART_PROMPT_TEMPLATE

    def _get_model(self, is_openai):
        """
        Returns the selected LLM model.

        Args:
            is_openai (bool): Whether to use an OpenAI model.

        Returns:
            object: The instantiated LLM model (OpenAI or open-source).
        """

        if is_openai:
            return ChatOpenAI(model=self.model_name)
        return OpenLLM(model_name=self.model_name, device=self.device)

    def get_gpus_list(self) -> list[str]:
        """
        Retrieves the list of available GPUs for running open-source models.

        Returns:
            list: A list of available GPUs.
        """

        return OpenLLM.list_gpus()

    def get_open_source_models(self) -> list[dict]:
        """
        Retrieves the list of available open-source models.

        Returns:
            list: A list of dictionaries containing details of each open-source
                  model (name, filesize, etc.).
        """

        models = OpenLLM.list_models()
        models_list = []

        for model in models:
            models_list.append(
                {
                    "name": model["name"],
                    "model_id": model["filename"],
                    "filesize": model["filesize"],
                    "ram": model["ramrequired"],
                    "parameters": model["parameters"],
                    "type": model["type"],
                }
            )
        return models_list

    def generate_code_and_sql(self, data) -> dict:
        """
        Generates SQL queries and chart code based on the user input. Uses LLM models
        to process the input prompt and generates the SQL query and visualization code.
        Results are cached in Redis.

        Args:
            data (dict): A dictionary containing 'chart_type' and 'query'.

        Returns:
            dict: A dictionary containing the generated SQL query, chart code, and total time taken.
        """
        start_time = time.time()

        try:
            chart_type = data["chart_type"].lower()
            query = data["query"]
        except KeyError as e:
            raise InvalidInputError(
                f"""Missing required key: {str(e)}.
                Dict should have 'chart_type' and 'query' as keys."""
            ) from e

        if chart_type not in ALLOWED_CHART_TYPES:
            raise InvalidInputError(
                f"Invalid chart type. Allowed types: {ALLOWED_CHART_TYPES}"
            )

        # Generate SQL query and check cache
        generated_sql_query = self._generate_sql_query(query)
        cached_result = self._check_cache(generated_sql_query)

        if cached_result:
            return self._format_response(
                "Fetching result from Redis cache...", cached_result, start_time
            )

        try:
            # Run SQL query and generate chart code
            result = self.db.run(generated_sql_query)
            chart_code = self._generate_chart_code(chart_type, result)

            # Cache the result in Redis
            self._cache_result(generated_sql_query, result, chart_code)

            return self._format_response(
                "Query and chart generated successfully.",
                {"sql_query": generated_sql_query, "chart_code": chart_code},
                start_time,
            )
        except Exception as e:
            raise InvalidInputError(f"Something went wrong: {str(e)}.") from e

    def _generate_sql_query(self, query: str) -> str:
        """Helper to generate SQL query from the input query using LLM."""
        system_message = SystemMessagePromptTemplate(
            prompt=self.prompt_template
        ).format(dialect="SQLite", top_k=self.top_k, schema=self.schema, query=query)
        response = self.llm.invoke(input=[system_message])

        return (
            response.content.strip() if self.is_openai else extract_sql_query(response)
        )

    def _check_cache(self, cache_key: str) -> dict:
        """Helper to check for cached results in Redis."""
        return self.redis_client.get(cache_key)

    def _generate_chart_code(self, chart_type: str, result: str) -> str:
        """Helper to generate chart code using the LLM and query result."""
        chart_system_message = SystemMessagePromptTemplate(
            prompt=self.chart_prompt_template
        ).format(chart_type=chart_type, chart_data=f"Query Result: {result}")

        chart_response = self.llm.invoke(input=[chart_system_message])
        response = chart_response.content if self.is_openai else chart_response
        parsed_response = extract_code_response(response, chart_type)

        if parsed_response is None:
            raise InvalidInputError("Something went wrong: Could not generate code")
        return parsed_response

    def _cache_result(self, cache_key: str, result: str, chart_code: str):
        """Helper to cache the SQL query and chart code in Redis."""
        self.redis_client.set(
            cache_key,
            {"sql_query": cache_key, "result": result, "chart_code": chart_code},
        )

    def _format_response(self, message: str, result: dict, start_time: float) -> dict:
        """Helper to format the response dictionary."""
        return {
            "message": message,
            "sql_query": result.get("sql_query"),
            "chart_code": result.get("chart_code"),
            "total_time": time.time() - start_time,
        }
