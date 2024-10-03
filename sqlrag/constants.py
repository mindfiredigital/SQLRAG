"""
This module defines templates and constants used for generating SQL
queries and chart code.

It includes:
- Regular expressions for identifying Python and JavaScript code
  blocks within prompts.
- Prompt templates for generating SQL queries based on user input
  for different types of LLM models (OpenAI, LLaMa).
- Prompt templates for generating chart code based on the chart
  type (matplotlib or chart.js).
"""

PYTHON_REGEX = r"```python(.*?)```"
# JAVASCRIPT_REGEX = r"```(?:javascript|js)(.*?)```"
JAVASCRIPT_REGEX = r"```(?:javascript|js)(.*?)```|<script\b[^>]*>(.*?)</script>"


ALLOWED_CHART_TYPES = ["matplotlib", "chart.js"]

PROMPT_TEMPLATE = """
                Always follow the below database schema to construct the correct query
                {schema}

                QUERY:
                {query}

                TASK:
                You are an agent designed to interact with a SQL database.
                Given an input question, create a syntactically correct {dialect} query to run,
                Unless the user specifies a specific number of examples, always limit your query to {top_k} results.
                Do not make any DML statements (INSERT, UPDATE, DELETE, DROP).

                Use the above query to construct a SQL query using the above db schema.
                Please construct only one single query from the user question.
                Do not add extra words just return one single sql query matching with user question.

                AI RESPONSE:
        """

PROMPT_TEMPLATE_LLAMA = """
                [INST] You are an AI assistant designed to interact with a SQL database. Your task is to create a syntactically correct {dialect} query based on the given input question and database schema. Follow these guidelines:

                1. Use the following database schema:
                {schema}

                2. The user's query is:
                {query}

                3. Important rules:
                - Unless specified, limit your query to {top_k} results.
                - Do not use any DML statements (INSERT, UPDATE, DELETE, DROP).
                - Construct only one single query that matches the user's question.
                - Return only the SQL query without any additional explanation.
                - Even do not use ```sql in starting the query and do not end with ``` just plain query in string.
                - Do not returnt the provided prompt back in response.

                Now, please provide the SQL query that answers the user's question. [/INST]
        """


CHART_PROMPT_TEMPLATE = """
                Always follow the below chart data schema to construct the correct {chart_type} code.
                {chart_data}

                QUERY:
                Use the above chart data to plot a chart and the type of chart can be used with {chart_type}.

                TASK:
                After retrieving the data, generate code based on the {chart_type}.

                If the chart_type is 'matplotlib' generate Python code for matplotlib libraries.
                If the chart_type is 'chart.js', generate JavaScript code for chart.js.
                Always stick to generate the code based on provided chart_type.

                The generated code must use the retrieved data and should be structured properly to create the appropriate chart.


                **For Python-based plotting (matplotlib)**:

                Example:

                import pandas as pd
                import matplotlib.pyplot as plt
                import seaborn as sns

                # Data as a pandas DataFrame
                data = pd.DataFrame({{
                        'product_name': ['Product A', 'Product B', 'Product C'],
                        'count': [10, 15, 7]
                }})

                # Bar plot using seaborn
                plt.figure(figsize=(10, 6))
                sns.barplot(x='product_name', y='count', data=data)

                # Save plot
                plt.savefig('output_chart.png')

                **For JavaScript-based plotting (chart.js)**:

                Example:

                const ctx = document.getElementById('myChart').getContext('2d');
                const myChart = new Chart(ctx, {{
                        type: 'bar',
                        data: {{
                        labels: ['Product A', 'Product B', 'Product C'],
                        datasets: [{{
                                label: 'Product Count',
                                data: [10, 15, 7],
                                backgroundColor: [
                                'rgba(255, 99, 132, 0.2)',
                                'rgba(54, 162, 235, 0.2)',
                                'rgba(75, 192, 192, 0.2)'
                                ],
                                borderColor: [
                                'rgba(255, 99, 132, 1)',
                                'rgba(54, 162, 235, 1)',
                                'rgba(75, 192, 192, 1)'
                                ],
                                borderWidth: 1
                        }}]
                        }},
                        options: {{
                        scales: {{
                                y: {{
                                beginAtZero: true
                                }}
                        }}
                        }}
                }});

                Do not return any string data; only return the code required to generate the chart or plot.
                Always reponse the code format based on chart type: {chart_type}

                AI RESPONSE:
        """


CHART_PROMPT_TEMPLATE_LLAMA = """
                [INST] You are an AI assistant tasked with generating code to create a {chart_type} chart based on the provided data. Follow these guidelines:

                1. Use the following chart data:
                {chart_data}

                2. Generate code for a {chart_type} chart using the provided data.

                3. Important rules:
                - If chart_type is 'matplotlib' or 'seaborn', generate Python code using the respective library.
                - If chart_type is 'chart.js', generate JavaScript code for chart.js.
                - Use only the specified chart_type and the provided data.
                - Return only the code required to generate the chart or plot, without any explanations or string data.
                - Do not returnt the provided prompt back in response.

                The generated code must use the retrieved data and should be structured properly to create the appropriate chart.


                **For Python-based plotting (matplotlib/seaborn)**:

                Example:

                import pandas as pd
                import matplotlib.pyplot as plt
                import seaborn as sns

                # Data as a pandas DataFrame
                data = pd.DataFrame({{
                        'product_name': ['Product A', 'Product B', 'Product C'],
                        'count': [10, 15, 7]
                }})

                # Bar plot using seaborn
                plt.figure(figsize=(10, 6))
                sns.barplot(x='product_name', y='count', data=data)

                # Save plot
                plt.savefig('output_chart.png')

                **For JavaScript-based plotting (chart.js)**:

                Example:

                const ctx = document.getElementById('myChart').getContext('2d');
                const myChart = new Chart(ctx, {{
                        type: 'bar',
                        data: {{
                        labels: ['Product A', 'Product B', 'Product C'],
                        datasets: [{{
                                label: 'Product Count',
                                data: [10, 15, 7],
                                backgroundColor: [
                                'rgba(255, 99, 132, 0.2)',
                                'rgba(54, 162, 235, 0.2)',
                                'rgba(75, 192, 192, 0.2)'
                                ],
                                borderColor: [
                                'rgba(255, 99, 132, 1)',
                                'rgba(54, 162, 235, 1)',
                                'rgba(75, 192, 192, 1)'
                                ],
                                borderWidth: 1
                        }}]
                        }},
                        options: {{
                        scales: {{
                                y: {{
                                beginAtZero: true
                                }}
                        }}
                        }}
                }});

                Do not return any string data; only return the code required to generate the chart or plot.

                Now, please provide the code to create the {chart_type} chart using the given data. [/INST]
        """
