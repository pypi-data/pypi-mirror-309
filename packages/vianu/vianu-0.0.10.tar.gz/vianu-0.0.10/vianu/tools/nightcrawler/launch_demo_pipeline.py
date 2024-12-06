import requests
import logging
import os
import time
from tqdm.auto import tqdm
from dotenv import load_dotenv
import pandas as pd
from requests.auth import HTTPBasicAuth



# Create a named logger
logger = logging.getLogger("nightcrawler_logger")

# Set the log level
logger.setLevel(logging.INFO)

# Define a custom formatter
formatter = logging.Formatter(
    fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)


class SerpApiClient:
    """
    A client to interact with the SERP API for performing search queries.
    """

    def __init__(self, serpapi_token, location):
        """
        Initializes the SerpApiClient with the given API token.

        Args:
            serpapi_token (str): The API token for SERP API.
        """
        self.serpapi_token = serpapi_token
        self.location = location

    def search(self, query, num_results=10):
        """
        Performs a search using SERP API and returns the URLs of the results.

        Args:
            query (str): The search query.
            num_results (int): Number of results to return.

        Returns:
            list: A list of URLs from the search results.
        """
        logger.info(f"Performing SERP API search for query: {query}")

        params = {
            "engine": "google",
            "q": query,
            "api_key": self.serpapi_token,
            "num": num_results,
            "location_requested": self.location,
            "location_used": self.location,
        }

        response = requests.get("https://serpapi.com/search", params=params)

        if response.status_code == 200:
            data = response.json()
            search_results = data.get("organic_results", [])
            urls = [result.get("link") for result in search_results]
            logger.info(f"Found {len(urls)} URLs from SERP API.")
            return urls
        else:
            logger.error(
                f"SERP API request failed with status code {response.status_code}"
            )
            return []

class ZyteApiClient:
    """
    A client to interact with the Zyte API for fetching product details.
    """

    def __init__(self, zyte_api_key, max_retries=1, retry_delay=10):
        """
        Initializes the ZyteApiClient with the given API key and retry configurations.

        Args:
            zyte_api_key (str): The API key for Zyte API.
            max_retries (int): Maximum number of retries for API calls.
            retry_delay (int): Delay between retries in seconds.
        """
        self.endpoint = "https://api.zyte.com/v1/extract"
        self.auth = HTTPBasicAuth(zyte_api_key, "")
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def get_product_details(self, urls):
        """
        Fetches product details from the given URLs using Zyte API.

        Args:
            urls (list): A list of URLs to fetch product details from.

        Returns:
            list: A list of dictionaries containing product details.
        """
        logger.info(f"Fetching product details for {len(urls)} URLs via Zyte API.")
        products = []
        config = {
            "javascript": False,
            "browserHtml": False,
            "screenshot": False,
            "product": True,
            "productOptions": {"extractFrom": "httpResponseBody"},
            "httpResponseBody": True,
            "geolocation": "CH",
            "viewport": {"width": 1280, "height": 1080},
            "actions": [],
        }

        with tqdm(total=len(urls)) as pbar:
            for url in urls:
                attempts = 0
                while attempts < self.max_retries:
                    try:
                        logger.debug(
                            f"Attempting to fetch product details for URL: {url} (Attempt {attempts + 1})"
                        )
                        response = requests.post(
                            self.endpoint,
                            auth=self.auth,
                            json={
                                "url": url,
                                **config,
                            },
                            timeout=10,
                        )

                        if response.status_code == 200:
                            product_data = response.json()
                            product_data["url"] = url  # Ensure the URL is included
                            products.append(product_data)
                            logger.debug(
                                f"Successfully fetched product details for URL: {url}"
                            )
                            break  # Exit the retry loop on success
                        else:
                            logger.error(
                                f"Zyte API request failed for URL {url} with status code {response.status_code} "
                                f"and response: {response.text}"
                            )
                            attempts += 1
                            if attempts < self.max_retries:
                                logger.warning(
                                    f"Retrying in {self.retry_delay} seconds..."
                                )
                                time.sleep(self.retry_delay)
                    except Exception as e:
                        logger.error(
                            f"Exception occurred while fetching product details for URL {url}: {e}"
                        )
                        attempts += 1
                        if attempts < self.max_retries:
                            logger.warning(f"Retrying in {self.retry_delay} seconds...")
                            time.sleep(self.retry_delay)
                else:
                    logger.error(f"All attempts failed for URL: {url}")
                pbar.update(1)

        logger.info(f"Fetched product details for {len(products)} URLs.")
        return products


class Processor:
    """
    Processes the product data and applies specific filtering rules.
    """

    def __init__(self, country_code):
        """
        Initializes the Processor with the given country code.

        Args:
            country_code (str): The country code to filter results by.
        """
        self.country_code = country_code.lower()

    def process(self, products):
        """
        Processes the product data and filters based on country code.

        Args:
            products (list): A list of product data dictionaries.

        Returns:
            list: A filtered list of product data dictionaries.
        """
        logger.info(
            f"Processing {len(products)} products and filtering by country code: {self.country_code.upper()}"
        )

        filtered_products = []
        for product in products:
            url = product.get("url", "")
            if (
                f".{self.country_code}/" in url.lower()
                or url.lower().endswith(f".{self.country_code}")
                or ".com" in url.lower()
            ):
                filtered_products.append(product)

        logger.info(
            f"Filtered down to {len(filtered_products)} products after applying country code filter."
        )
        return filtered_products


class NightcrawlerClient:
    """
    The main client that orchestrates the search, data fetching, and processing.
    """

    def __init__(self, serpapi_token=None, zyte_api_key=None):
        """
        Initializes the NightcrawlerClient with optional API tokens.

        Args:
            serpapi_token (str, optional): The API token for SERP API.
            zyte_api_key (str, optional): The API key for Zyte API.
        """
        self.serpapi_token = serpapi_token
        self.zyte_api_key = zyte_api_key

    def search(self, query, location, num_results=10, country_code="ch"):
        """
        Performs the search, gets product details, processes them, and returns a DataFrame.

        Args:
            query (str): The search query.
            num_results (int): Number of search results to process.
            country_code (str): The country code to filter results.

        Returns:
            DataFrame: A pandas DataFrame containing the final product data.
        """
        # Ensure API tokens are set
        if not self.serpapi_token:
            raise ValueError("SERP API token is not set.")
        if not self.zyte_api_key:
            raise ValueError("Zyte API key is not set.")

        # Instantiate clients
        serp_client = SerpApiClient(self.serpapi_token, location)
        zyte_client = ZyteApiClient(self.zyte_api_key)
        processor = Processor(country_code)

        # Perform search
        urls = serp_client.search(query, num_results)
        if not urls:
            logger.error("No URLs found from SERP API.")
            return pd.DataFrame()

        # Get product details
        products = zyte_client.get_product_details(urls)
        if not products:
            logger.error("No product details fetched from Zyte API.")
            return pd.DataFrame()

        # Process products
        filtered_products = processor.process(products)
        if not filtered_products:
            logger.warning("No products left after filtering.")
            return pd.DataFrame()

        # Flatten the product data
        df = pd.json_normalize(filtered_products)

        # Log and return the DataFrame
        logger.info("Search completed. Returning flattened DataFrame.")
        return df


if __name__ == "__main__":
    load_dotenv()

    # Instantiate the client
    nc_client = NightcrawlerClient()

    # Set API tokens
    nc_client.serpapi_token = os.getenv("SERP_API_TOKEN", "YOUR_SERPAPI_TOKEN")
    nc_client.zyte_api_key = os.getenv("ZYTE_API_TOKEN", "YOUR_ZYTE_API_KEY")

    # Perform search
    df = nc_client.search("sildenafil", num_results=5, location="Switzerland")

    # Display results
    print(df)
