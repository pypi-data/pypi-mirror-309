# -*- coding: utf-8 -*-
# !/usr/bin/env python

"""Module for fetching NAICS code descriptions from the U.S. Census Bureau API.

This module defines a `NaicsDataFetcher` class, which handles querying the U.S. Census Bureau's
API to retrieve descriptions for NAICS (North American Industry Classification System) codes.
The class supports asynchronous requests for improved efficiency, particularly when fetching
data for multiple unique NAICS codes, and manages API key loading securely from an `.env` file.

Classes:
    NaicsDataFetcher: Encapsulates methods to load the Census API key, fetch data for a single
                      NAICS code, fetch data for multiple codes, and process a DataFrame of
                      NAICS codes to retrieve corresponding descriptions.

Functions:
    __init__(cfg: DictConfig): Initializes the `NaicsDataFetcher` with a configuration object
                               and loads the API key from the `.env` file.
    _load_api_key() -> str: Loads the Census API key from the `.env` file, raising an
                            `EnvironmentError` if the file or key is missing.
    _fetch_single_naics_data(naics_code: str, session: aiohttp.ClientSession) -> Dict[str, Optional[str]]:
        Asynchronously fetches a description for a single NAICS code using a shared session.
    _fetch_all_naics_data(naics_codes: List[str]) -> List[Dict[str, Optional[str]]]:
        Asynchronously fetches descriptions for multiple NAICS codes using a single session.
    process_naics_codes(df: pd.DataFrame, code_column: str) -> pd.DataFrame:
        Processes a DataFrame containing NAICS codes, fetching descriptions and returning
        a new DataFrame with `naics_code` and `naics_title` columns.

Example Usage:
    ```
    import hydra
    from omegaconf import DictConfig
    from dotenv import load_dotenv
    import pandas as pd

    # Load configuration using Hydra
    with hydra.initialize(config_path="."):
        cfg = hydra.compose(config_name="main")

    # Example DataFrame with NAICS codes
    df = pd.DataFrame({"naics_code": ["481112", "523910", "621111"]})

    # Create an instance of the NaicsDataFetcher and fetch data
    try:
        fetcher = NaicsDataFetcher(cfg)
        result_df = fetcher.process_naics_codes(df, "naics_code")
        print(result_df)
    except EnvironmentError as e:
        print(e)
    ```

Notes:
    - Requires `aiohttp` for asynchronous HTTP requests, `omegaconf` for configuration handling,
      and `dotenv` to load environment variables.
    - The API key must be stored in an `.env` file with the key `CENSUS_DATA_API_KEY`.
    - Asynchronous requests are used to enhance performance when querying multiple codes.

"""

import asyncio
import os
from datetime import datetime
from functools import lru_cache
from typing import Dict, List, Optional, Union

import aiohttp
import pandas as pd
from dotenv import load_dotenv
from omegaconf import DictConfig


class NaicsDataFetcher:
    """Singleton class for fetching NAICS code descriptions from the Census API with caching."""

    _instance = None  # Singleton instance
    _naics_cache = {}

    def __new__(cls, *args, **kwargs):
        """Ensure only a single instance of NaicsDataFetcher is created."""
        if not cls._instance:
            cls._instance = super(NaicsDataFetcher, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        cfg: DictConfig,
        max_concurrent_requests: int = 10,
    ):
        """Initialize the NaicsDataFetcher with configuration and API key.

        Args:
            cfg (DictConfig): The configuration object.
            max_concurrent_requests (int): The maximum number of concurrent requests.

        """
        if not hasattr(self, "_initialized"):  # Avoid re-initialization in singleton
            self.cfg = cfg
            self.census_api_key = self._load_api_key()
            self.base_url = f"{cfg.census_api.base_url}/{cfg.census_api.dataset}"
            self.semaphore = asyncio.Semaphore(max_concurrent_requests)
            self.time = f"{datetime.now().year}-01"
            self._initialized = True

    def _load_api_key(self) -> str:
        """Load the Census API key from the .env file.

        Returns:
            str: The API key for the Census Bureau.

        Raises:
            EnvironmentError: If the .env file or the CENSUS_DATA_API_KEY is not found.

        """
        load_dotenv()
        api_key = os.getenv("CENSUS_DATA_API_KEY")

        if not api_key:
            raise EnvironmentError(
                "CENSUS_DATA_API_KEY not found. Please ensure the .env file is present and contains the API key."
            )
        return api_key

    async def _fetch_from_auxiliar_endpoint(
        self,
        naics_code: str,
        session: aiohttp.ClientSession,
    ) -> Union[str, None]:
        """Get the auxiliar endpoint for the Census API.

        Args:
            naics_code (str): The NAICS code to fetch data for.
            session (aiohttp.ClientSession): The shared aiohttp session.

        Returns:
            str: The auxiliar endpoint for the Census API.

        """
        query_url = self.cfg.usspending_api.base_url.format(naics_code=naics_code)
        async with session.get(query_url) as response:
            if response.status == 200:
                data = await response.json()
                return data["results"][0]["naics_description"].capitalize()
            else:
                print(f"Failed to fetch data for NAICS code {naics_code}: {response.status}")
                return None

    @lru_cache(maxsize=100)
    async def _fetch_single_naics_data(
        self,
        naics_code: str,
        session: aiohttp.ClientSession,
    ) -> Dict[str, Optional[str]]:
        """Fetch data for a single NAICS code asynchronously using a shared session.

        Args:
            naics_code (str): The NAICS code to fetch data for.
            session (aiohttp.ClientSession): The shared aiohttp session.

        Returns:
            Dict[str, Optional[str]]: A dictionary with `naics_code` and `naics_title`.
        """
        if naics_code in self._naics_cache:
            return {"naics_code": naics_code, "naics_title": self._naics_cache[naics_code]}

        full_url = (
            f"{self.base_url}"
            f"?get={"&".join(self.cfg.census_api.parameters['get']).format(time=self.time)}"
            f"&{self.cfg.census_api.parameters['naics_code'].format(naics_code=naics_code)}"
            f"&key={self.census_api_key}"
        )
        async with self.semaphore:
            async with session.get(full_url) as response:
                if response.status == 200:
                    data = await response.json()
                    naics_title = data[1][0].capitalize() if len(data) > 1 else None
                    if naics_title is None:
                        naics_title = await self._fetch_from_auxiliar_endpoint(
                            naics_code,
                            session,
                        )
                    self._naics_cache[naics_code] = naics_title
                    return {"naics_code": naics_code, "naics_title": naics_title}
                else:
                    naics_title = await self._fetch_from_auxiliar_endpoint(
                        naics_code,
                        session,
                    )
                    self._naics_cache[naics_code] = naics_title
                    return {"naics_code": naics_code, "naics_title": naics_title}

    async def _fetch_all_naics_data(
        self,
        naics_codes: List[str],
    ) -> List[Dict[str, Optional[str]]]:
        """Fetch data for multiple NAICS codes asynchronously using a shared session.

        Args:
            naics_codes (List[str]): A list of unique NAICS codes to fetch data for.

        Returns:
            List[Dict[str, Optional[str]]]: A list of dictionaries with `naics_code` and `naics_title`.
        """
        async with aiohttp.ClientSession() as session:  # Shared session for all requests
            tasks = [self._fetch_single_naics_data(code, session) for code in naics_codes]
            return await asyncio.gather(*tasks)

    def process_naics_codes(
        self,
        df: pd.DataFrame,
        code_column: str,
    ) -> pd.DataFrame:
        """Process NAICS codes in a DataFrame and return a DataFrame with fetched data.

        Args:
            df (pd.DataFrame): The DataFrame containing NAICS codes.
            code_column (str): The name of the column containing the NAICS codes.

        Returns:
            pd.DataFrame: A DataFrame containing `naics_code` and `naics_title`.
        """
        unique_naics_codes = df[code_column].unique().tolist()
        data = asyncio.run(self._fetch_all_naics_data(unique_naics_codes))
        result_df = pd.DataFrame(data)
        result_df["naics_title"] = result_df["naics_title"].str.capitalize()
        return result_df


if __name__ == "__main__":
    # This is only used for smoke testing
    import hydra

    with hydra.initialize(
        version_base=None,
        config_path="../../conf",
        job_name="smoke-testing-census",
    ):
        cfg = hydra.compose(config_name="main")
        df = pd.DataFrame({"naics_code": ["322120", "335139", "325991"]})
        try:
            fetcher = NaicsDataFetcher(cfg)
            result_df = fetcher.process_naics_codes(df, "naics_code")
            print(result_df)
        except EnvironmentError as e:
            print(e)
