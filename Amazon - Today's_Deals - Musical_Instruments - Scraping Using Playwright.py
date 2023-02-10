# Importing libraries
import random
import asyncio
import pandas as pd
from playwright.async_api import async_playwright


# Function to perform a request and retry the request if it fails, with a maximum of 5 retries
async def perform_request_with_retry(page, link):
    MAX_RETRIES = 5
    retry_count = 0
    while retry_count < MAX_RETRIES:
        try:
            # Make a request to the link
            await page.goto(link)
            # If the request is successful, break the loop
            break
        except:
            retry_count += 1
            if retry_count == MAX_RETRIES:
                # Raise an exception if the maximum number of retries is reached
                raise Exception("Request timed out")
            # Sleep for a random duration between 1 and 5 seconds
            await asyncio.sleep(random.uniform(1, 5))

            
# Function to extract the product links
async def get_product_links(page):
    # Select all elements
    all_items = await page.query_selector_all('.a-link-normal.DealCardDynamic-module__linkOutlineOffset_2XU8RDGmNg2HG1E-ESseNq')
    product_links = []
    # Loop through each item and extract the href attribute
    for item in all_items:
        link = await item.get_attribute('href')
        product_links.append(link)
    # Return the list of product links
    return product_links


# Function to extract the product name
async def get_product_name(page):
    # Try to extract the product name from the page
    try:
        product_name = await (await page.query_selector("#productTitle")).text_content()
    # If extraction fails, leave product name as "Not Available"
    except:
        product_name = "Not Available"
    return product_name


# Function to extract the brand of the product
async def get_brand(page):
    # Try to extract the brand from the page
    try:
        brand = await (await page.query_selector("tr.po-brand td span.po-break-word")).text_content()
    # If extraction fails, leave brand as "Not Available"
    except:
        brand = "Not Available"
    return brand


# Function to extract the star rating of the product
async def get_star_rating(page):
    # Try to extract the star rating from the page
    try:
        star_rating = await (await page.query_selector(".a-icon-alt")).text_content()
        star_rating = star_rating.split(" ")[0]
    # If extraction fails, leave star rating as "Not Available"
    except:
        star_rating = "Not Available"
    return star_rating


# Function to extract the number of ratings of the product
async def get_num_ratings(page):
    # Try to extract the number of ratings from the page
    try:
        ratings_text = await (await page.query_selector("#acrCustomerReviewText")).text_content()
        num_ratings = ratings_text.split(" ")[0]
    # If extraction fails, leave number of ratings as "Not Available"
    except:
        num_ratings = "Not Available"
    return num_ratings


# Function to extract the original price of the product
async def get_original_price(page):
    # Try to extract the original price from the page
    try:
        original_price = await (await page.query_selector(".a-price.a-text-price")).text_content()
        original_price = original_price.split("₹")[1]
    # If extraction fails, leave original price as "Not Available"
    except:
        original_price = "Not Available"
    return original_price


# Function to extract the offer price of the product
async def get_offer_price(page):
    # Try to extract the offer price from the page
    try:
        offer_price = await (await page.query_selector(".a-price-whole")).text_content()
    # If extraction fails, leave offer price as "Not Available"
    except:
        offer_price = "Not Available"
    return offer_price


# Function to extract the color of the product
async def get_color(page):
    # Try to extract the color from the page
    try:
        color = await (await page.query_selector("tr.po-color td span.po-break-word")).text_content()
    # If extraction fails, leave color as "Not Available"
    except:
        color = "Not Available"
    return color


# Function to extract the size of the product
async def get_size(page):
    # Try to extract the size from the page
    try:
        size = await (await page.query_selector("tr.po-size td span.po-break-word")).text_content()
    # If extraction fails, leave size as "Not Available"
    except:
        size = "Not Available"
    return size


# Function to extract the material of the product
async def get_material(page):
    # Try to extract the material from the page
    try:
        material = await (await page.query_selector("tr.po-back.material td span.po-break-word")).text_content()
    # If extraction fails, leave material as "Not Available"
    except:
        material = "Not Available"
    return material


# Function to extract the connectivity technology of the product
async def get_connectivity_technology(page):
    # Try to extract the connectivity technology from the page
    try:
        connectivity_technology = await (await page.query_selector("tr.po-connectivity_technology td span.po-break-word")).text_content()
    # If extraction fails, leave connectivity technology as "Not Available"
    except:
        connectivity_technology = "Not Available"
    return connectivity_technology


# Function to extract the connector type of the product
async def get_connector_type(page):
    # Try to extract the connector type from the page
    try:
        connector_type = await (await page.query_selector("tr.po-connector_type td span.po-break-word")).text_content()
    # If extraction fails, leave connector_type as "Not Available"
    except:
        connector_type = "Not Available"
    return connector_type


#Function to extract the compatible devices of the product
async def get_compatible_devices(page):
    # Try to extract the compatible devices from the page
    try:
        compatible_devices = await (await page.query_selector("tr.po-compatible_devices td span.po-break-word")).text_content()
    # If extraction fails, leave compatible devices as "Not Available"
    except:
        compatible_devices = "Not Available"
    return compatible_devices


# Main function to extract and save product data
async def main():
    # Start an async session with Playwright
    async with async_playwright() as pw:
        # Launch a new browser instance
        browser = await pw.chromium.launch()
        # Open a new page in the browser
        page = await browser.new_page()
        # Navigate to the Amazon deal page
        await perform_request_with_retry(page, 'https://www.amazon.in/gp/goldbox?deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%252215C82F45284EDD496F94A2C368D1B4BD%2522%252C%2522sorting%2522%253A%2522BY_SCORE%2522%257D')
        # Get the links to each product
        product_links = await get_product_links(page)

        # Create an empty list to store the extracted data
        data = []
        # Iterate over the product links
        for link in product_links:
            # Load the product page
            await perform_request_with_retry(page, link)
            # Extract the product information
            
            # Product Name
            product_name = await get_product_name(page)
            
            # Brand
            brand = await get_brand(page)
            
            # Star Rating
            star_rating = await get_star_rating(page)
            
            # Number of Ratings
            num_ratings = await get_num_ratings(page)
            
            # Original Price
            original_price = await get_original_price(page)
            
            # Offer Price
            offer_price = await get_offer_price(page)
            
            # Color
            color = await get_color(page)
            
            # Size
            size = await get_size(page)
            
            # Material
            material = await get_material(page)
            
            # Connectivity Technology
            connectivity_technology = await get_connectivity_technology(page)
            
            # Connector Type
            connector_type = await get_connector_type(page)
            
            # Compatible Devices
            compatible_devices = await get_compatible_devices(page)
            
            
            # Add the extracted data to the list
            data.append((link, product_name, brand, star_rating, num_ratings, original_price, offer_price, color,
                         size, material, connectivity_technology, connector_type, compatible_devices))

        # Create a pandas dataframe from the extracted data
        df = pd.DataFrame(data, columns=['Product Link', 'Product Name', 'Brand', 'Star Rating', 'Number of Ratings', 'Original Price', 'Offer Price', 
                                         'Color', 'Size', 'Material', 'Connectivity_technology', 'Connector_type', 'Compatible_devices'])
        # Save the data to a CSV file
        df.to_csv('product_details5.csv', index=False)

        # Notify the user that the file has been saved
        print('CSV file has been written successfully.')
        # Close the browser instance
        await browser.close()

# Entry point to the script
if __name__ == '__main__':
    asyncio.run(main())
