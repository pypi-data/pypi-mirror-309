import os

from src.client import NightcrawlerClient
from dotenv import load_dotenv

import logging

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
