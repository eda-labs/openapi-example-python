#!/usr/bin/env python3

import requests
import json
import logging
import time
from pathlib import Path
import subprocess
import sys
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAPIDiscovery:
    def __init__(self):
        self.base_url = "https://api.github.com/repos/eda-labs/openapi"
        self.raw_base = "https://raw.githubusercontent.com/eda-labs/openapi/main"
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        self.cache_file = Path("cached_specs.json")
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        self.session = requests.Session()
        self.session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
        
    def get_contents(self, path=""):
        url = f"{self.base_url}/contents/{path}"
        logger.info(f"Fetching contents from: {url}")
        
        response = self.session.get(url, headers=self.headers)
        response.raise_for_status()
        
        # Rate limiting info
        remaining = response.headers.get('X-RateLimit-Remaining')
        if remaining:
            logger.info(f"API calls remaining: {remaining}")
            
        # Sleep for 5 seconds to respect rate limits
        sleep_duration = 5
        logger.debug(f"Sleeping for {sleep_duration} seconds...")
        time.sleep(sleep_duration)
        
        content = response.json()
        if isinstance(content, str):
            raise ValueError(f"Unexpected response format: {content}")
        return content

    def load_cached_specs(self):
        try:
            if self.cache_file.exists() and self.cache_file.stat().st_size > 0:
                with open(self.cache_file) as f:
                    cached = json.load(f)
                    if isinstance(cached, list):
                        return cached
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"Cache read error: {e}")
        return []

    def save_specs_cache(self, specs):
        try:
            with open(self.cache_file, "w") as f:
                json.dump(specs, f, indent=2)
        except OSError as e:
            logger.error(f"Failed to save cache: {e}")

    def discover_specs(self, use_cache=True):
        if use_cache:
            cached = self.load_cached_specs()
            if cached:
                logger.info("Using cached specs")
                return cached

        specs = []
        
        # Check core path
        core_specs = self.get_contents("core")
        for spec in core_specs:
            if spec.get("type") == "file" and spec.get("name", "").endswith(".json"):
                specs.append({
                    "name": Path(spec["name"]).stem,
                    "url": f"{self.raw_base}/core/{spec['name']}"
                })

        # Check apps path
        apps = self.get_contents("apps")
        for app in apps:
            if app.get("type") == "dir":
                versions = self.get_contents(app["path"])
                for version in versions:
                    if version.get("type") == "dir":
                        files = self.get_contents(version["path"])
                        for file in files:
                            if file.get("name", "").endswith(".json"):
                                specs.append({
                                    "name": app["name"].split(".")[0],
                                    "url": f"{self.raw_base}/{file['path']}"
                                })

        if specs:
            self.save_specs_cache(specs)
            
        return specs

    def generate_models(self, use_cache=True):
        output_dir = Path("models")
        output_dir.mkdir(exist_ok=True)
        specs = self.discover_specs(use_cache=use_cache)
        
        if not specs:
            logger.warning("No specs found!")
            return
            
        for spec in specs:
            url_parts = spec["url"].split("/")
            module_name = url_parts[-1].replace(".json", "")
            
            cmd = [
                "datamodel-codegen",
                "--url", spec["url"],
                "--output-model-type", "pydantic_v2.BaseModel",
                "--use-annotated",
                "--enum-field-as-literal", "all",
                "--output", str(output_dir)  # Change to output directory only
            ]
            
            try:
                logger.info(f"Generating models for {module_name}...")
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError as e:
                logger.error(f"Error generating models for {module_name}: {e}")

if __name__ == "__main__":
    discovery = OpenAPIDiscovery()
    # Use --no-cache flag to force fresh discovery
    use_cache = "--no-cache" not in sys.argv
    discovery.generate_models(use_cache=use_cache)