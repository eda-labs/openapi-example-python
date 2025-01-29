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

3. Run the example:

    ```bash
    python main.py
    ```
