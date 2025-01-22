# Full model driven, declarative network management without YANG

YANG, as the defacto modelling language used in the networking domain, plays a critical role in the model-driven automation.  
Yet, network automation community suffers from a lack of high quality tools around YANG ecosystem. Starting from the documentation tools to the code generation and SDKs.

When tools fail to deliver, engineers play the favourite screen scraping card to have a go at network automation, effectively discarding the benefits of the model-driven approach.

This repository accompanies a video demonstration that shows how full model-driven, declarative network automation can be achieved without YANG. By using Nokia EDA platform and its OpenAPI-based APIs we generate the pydantic models from the OpenAPI specs and use them to define network resources using native language constructs.

[![video](https://gitlab.com/rdodin/pics/-/wikis/uploads/27b5d6a76c9050de68f083dfa88065a5/netrel013-eda-openapi-yt.png)](https://youtu.be/HgI7Q6EQFVA)

## Get started

1. [Install EDA](https://docs.eda.dev/getting-started/try-eda/)

2. Clone the repo and use `uv` to install the project and dependencies:

    ```bash
    git clone https://github.com/eda-labs/openapi-example-python.git
    cd openapi-example-python
    uv sync
    ```

## Generating pydantic models from OpenAPI

Install `datamodel-codegen`:

```
uv tool install 'datamodel-code-generator[http]'
```

To generate a model:

```bash
# core
datamodel-codegen --url https://raw.githubusercontent.com/eda-labs/openapi/refs/heads/main/core/core.json \
--output-model-type pydantic_v2.BaseModel \
--use-annotated \
--enum-field-as-literal all \
--output models/core.py

# interfaces
datamodel-codegen --url https://raw.githubusercontent.com/eda-labs/openapi/refs/heads/main/apps/interfaces.eda.nokia.com/v1alpha1/interfaces.json \
--output-model-type pydantic_v2.BaseModel \
--use-annotated \
--enum-field-as-literal all \
--output models

# siteinfo
datamodel-codegen --url https://raw.githubusercontent.com/eda-labs/openapi/refs/heads/main/apps/siteinfo.eda.nokia.com/v1alpha1/siteinfo.json \
--output-model-type pydantic_v2.BaseModel \
--use-annotated \
--enum-field-as-literal all \
--output models
```

See [command options](https://koxudaxi.github.io/datamodel-code-generator/#all-command-options) for more details.

## gen_models.py Documentation

This script handles the discovery of all OpenAPI specifications under both core/ and apps/ directories, generates Pydantic models, and caches the discovered specifications to optimize subsequent runs.

### Features

- **Automatic Discovery**: Scans both core/ and apps/ directories for OpenAPI `.json` files.
- **Caching**: Caches discovered specifications in `cached_specs.json` to reduce API calls.
- **Rate Limiting**: Waits 5 seconds between API requests to respect rate limits.
- **Retry Mechanism**: Retries failed API requests up to 3 times with exponential backoff.

### Usage

```bash
# Generate models with default settings
python gen_models.py

# Force fresh discovery by ignoring the cache
python gen_models.py --no-cache

# Display help message
python gen_models.py --help
```

### Troubleshooting

#### Common Errors

##### Missing Dependencies

If you encounter `ModuleNotFoundError: No module named 'requests'`, ensure that you've installed all required dependencies:

##### JSON Decode Errors

If you encounter `json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`, it may indicate an issue with the cached specifications. You can refresh the cache by running:

##### Script Errors

##### Type Errors

If you encounter errors like `TypeError: OpenAPIDiscovery.generate_models() got an unexpected keyword argument 'use_cache'`, ensure that your `gen_models.py` script has the correct method signatures and that you're passing arguments appropriately.

##### Rate Limiting

The script includes a 5-second delay between API requests to prevent hitting GitHub rate limits. If you continue to experience rate limiting issues, consider increasing the `sleep_duration` in the script.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

### References

See [command options](https://koxudaxi.github.io/datamodel-code-generator/#all-command-options) for more details on `datamodel-codegen`.

For more details, refer to the [documentation](docs/gen_models.md).
