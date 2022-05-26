# Project Info: This program is used to scrap the required data from ww.amazon.com and all the scraped data is dumped as CSV file in the users local system .
# Python version: 3.10
# Requirenments:
 * ## beautifulsoup4==4.11.1
 * ## requests==2.27.1
 * ## tqdm==4.64.0
# Input:
 * ## Headers: Google chrome headers are extracted, using curl and are passed as a argument from main.py .
# How to run:
 * ## Get into the current working directory (analystt_amazon_scrap).
 * ## Run the main.py file.
# Note: All those records whose values are not mentioned on website are returned as None/NULL.