# SQLRAG

<img src="./OpenRAGLogo.png" alt="Project Logo" width="100" height="auto">

SQLRAG allows users to query databases using natural language and receive results as SQL code and beautiful visualizations. Powered by Large Language Models (LLMs), SQLRAG supports both OpenAI models and open-source alternatives from GPT4All. Additionally, Redis caching is employed for optimized performance, and users can choose between CPU and GPU processing for open-source models.

## Table of Contents

- [SQLRAG](#SQLRAG)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
  - [API Hosting](#api-hosting)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## Description

SQLRAG is a Python package that lets users query their databases using simple natural language prompts. SQLRAG translates these prompts into SQL, executes the queries, and returns results as SQL code, data, and visualizations using either Matplotlib or Chart.js. It supports both open-source LLMs from GPT4All and paid models like OpenAI, giving users flexibility in model choice.

Redis caching is used to speed up responses for repeated queries, and users can opt for GPU processing with open-source models for faster execution.

## Features

- **Natural Language Queries**: Input your queries in plain language, and SQLRAG will convert them into SQL statements.
- **Data Visualization**: Generate charts using Python's Matplotlib or JavaScript's Chart.js.
- **Model Flexibility**: Supports both OpenAI models and open-source alternatives like GPT4All.
- **Redis Caching**: Improves response times for repeated queries by caching previous results.
- **Supports CPU and GPU**: Open-source models can run on both CPU and GPU, providing performance flexibility.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- A compatible database (PostgreSQL, MySQL, SQLite, etc.)
- Redis for caching (optional but recommended)
- An OpenAI API key (if using OpenAI models)

### Installation

SQLRAG is distributed as a Python package and can be installed via `pip`.

1. **Install the package:**
   ```bash
   pip install sqlrag
   ```

2. **Set environment variables (if using OpenAI):**
   ```bash
   export OPENAI_API_KEY=your_openai_key
   ```

That's it! Now you’re ready to use SQLRAG.

## Usage

### For Open-Source Models

You can use open-source models from GPT4All with SQLRAG. Here's how:

```python
from sqlrag.open_sql_rag import OpenSQLRAG

# Initialize SQLRAG with your database and model
sql_rag = OpenSQLRAG("sqlite:///mydb.db", model_name="Meta-Llama-3-8B-Instruct.Q4_0.gguf", is_openai=False)

# Generate SQL code and a chart
data = sql_rag.generate_code_and_sql({"chart_type": "chart.js", "query": "List out all customers"})

# Output the generated SQL code and data
print(data)

# Check available open-source models and supported GPUs
print(sql_rag.get_open_source_models())
print(sql_rag.get_gpus_list())
```

### For OpenAI Models

If you have an OpenAI API key, you can use OpenAI models with SQLRAG as follows:

```python
from sqlrag.open_sql_rag import OpenSQLRAG

# Initialize SQLRAG with your database (OpenAI by default)
sql_rag = OpenSQLRAG("sqlite:///mydb.db")

# Generate SQL code and a chart
data = sql_rag.generate_code_and_sql({"chart_type": "chart.js", "query": "List out all customers"})

# Output the generated SQL code and data
print(data)
```

### Redis Caching

SQLRAG automatically uses Redis to cache results of frequently used queries, speeding up the response time for repeated requests.

## API Hosting

While SQLRAG is primarily a Python package, you can also expose it as an API if desired. However, it’s primarily designed for use as a Python library for direct database querying and data visualization.

## Contributing

We welcome contributions to SQLRAG! Whether it's reporting bugs, submitting features, or writing documentation, feel free to open a pull request or issue. See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## License

SQLRAG is licensed under the MIT License. See [LICENSE.md](LICENSE.md) for further information.

## Acknowledgments

Special thanks to the developers of GPT4All, OpenAI, and Redis for their open-source contributions. Their work has made this project possible.
