"""
This module provides utility functions for extracting SQL queries and chart generation code
from model responses. It includes two main functions: `extract_sql_query` and
`extract_code_response`.

Functions:
----------
- extract_sql_query(response: str) -> str:
    Extracts a valid SQL query from the given response string, handling various formats
    such as plain SQL queries, queries within SQL code blocks, and first SELECT statement
    in case of multiple queries.

- extract_code_response(response: str, chart_type: str) -> str:
    Extracts the code for generating charts based on the chart type (either matplotlib
    or chart.js). The code is extracted from the model response in Python or JavaScript code blocks.
"""

import re
from .constants import PYTHON_REGEX, JAVASCRIPT_REGEX


def extract_sql_query(response):
    """
    Extracts a SQL query from the response string.

    This function looks for the following cases:
    - A plain SQL query starting with SELECT.
    - A SQL query inside a code block marked as ```sql```.
    - The first SELECT statement in the response if there are multiple queries or extra text.

    Args:
        response (str): The response from which to extract the SQL query.

    Returns:
        str: The extracted SQL query or the original response if no query is found.
    """

    # Case 1: Only query
    if response.strip().upper().startswith("SELECT"):
        match = re.search(r"SELECT.*?;", response, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(0).strip()

    # Case 2: Query in SQL code block
    sql_block_pattern = r"```sql\s*(.*?)\s*```"
    match = re.search(sql_block_pattern, response, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Case 3: First SELECT statement (for multiple queries or extra text)
    select_pattern = r"\bSELECT\b.*?;"
    match = re.search(select_pattern, response, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(0).strip()

    # If no SQL query is found, return the original response
    return response.strip()


def extract_code_response(response, chart_type):
    """
    Extracts chart generation code based on the chart type from the response.

    This function checks if the provided chart type is 'matplotlib' or 'chart.js',
    and accordingly searches for Python or JavaScript code blocks using regular
    expressions. For chart.js, it also supports code inside <script> tags.

    Args:
        response (str): The model's response containing the code.
        chart_type (str): The type of chart ('matplotlib' or 'chart.js').

    Returns:
        str: The extracted code for generating the chart, or None if no code is found.
    """

    code_match = None
    if chart_type == "matplotlib":
        code_match = re.search(PYTHON_REGEX, response, re.DOTALL)
    elif chart_type == "chart.js":
        code_match = re.search(JAVASCRIPT_REGEX, response, re.DOTALL)
        if code_match:
            # Get the JavaScript code inside either a code block or script tag
            code_match = (
                code_match.group(1) if code_match.group(1) else code_match.group(2)
            )
    return code_match
