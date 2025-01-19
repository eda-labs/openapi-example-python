# openapi-example-python

Install `datamodel-codegen`:

```
uv tool install 'datamodel-code-generator[http]'
```

To generate a mode:

```
datamodel-codegen --url https://raw.githubusercontent.com/eda-labs/openapi/refs/heads/main/apps/interfaces.eda.nokia.com/v1alpha1/interfaces.json \
--output-model-type pydantic_v2.BaseModel \
--use-annotated \
--enum-field-as-literal all \
--output models
```

See [command options](https://koxudaxi.github.io/datamodel-code-generator/#all-command-options) for more details.
