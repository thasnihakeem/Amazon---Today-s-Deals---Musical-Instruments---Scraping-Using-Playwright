import random
import asyncio
import pandas as pd
from playwright.async_api import async_playwright

# Perform a request and retries the request if it fails
async def perform_request_with_retry(page, link):
    MAX_RETRIES = 5
    retry_count = 0
    while retry_count < MAX_RETRIES:
        try:
            await page.goto(link)
            break
        except:
            retry_count += 1
            if retry_count == MAX_RETRIES:
                raise Exception("Request timed out")
            await asyncio.sleep(random.uniform(1, 5))

# Extract the Product links
async def get_product_links(page):
    all_items = await page.query_selector_all('.a-link-normal.DealCardDynamic-module__linkOutlineOffset_2XU8RDGmNg2HG1E-ESseNq')
    product_links = []
    for item in all_items:
        link = await item.get_attribute('href')
        product_links.append(link)
    return product_links

# Extract the Product name
async def get_product_name(page):
    try:
        product_name = await (await page.query_selector("#productTitle")).text_content()
    except:
        product_name = "Not Available"
    return product_name

# Extract the star rating of the products
async def get_star_rating(page):
    try:
        star_rating = await (await page.query_selector(".a-icon-alt")).text_content()
        star_rating = star_rating.split(" ")[0]
    except:
        star_rating = "Not Available"
    return star_rating


# Extract the number of ratings of products
async def get_num_ratings(page):
    try:
        ratings_text = await (await page.query_selector("#acrCustomerReviewText")).text_content()
        num_ratings = ratings_text.split(" ")[0]
    except:
        num_ratings = "Not Available"
    return num_ratings


# Extract the original price of the products
async def get_original_price(page):
    try:
        original_price = await (await page.query_selector(".a-price.a-text-price")).text_content()
        original_price = original_price.split("₹")[1]
    except:
        original_price = "Not Available"
    return original_price

# Extract the offer price of the products
async def get_offer_price(page):
    try:
        offer_price = await (await page.query_selector(".a-price-whole")).text_content()
    except:
        offer_price = "Not Available"
    return offer_price

# Extract the brand of the products
async def get_brand(page):
    try:
        brand = await (await page.query_selector("tr.po-brand td span.po-break-word")).text_content()
    except:
        brand = "Not Available"
    return brand

# Extract the original colour of the products
async def get_color(page):
    try:
        color = await (await page.query_selector("tr.po-color td span.po-break-word")).text_content()
    except:
        color = "Not Available"
    return color

# Extract the size of the products
async def get_size(page):
    try:
        size = await (await page.query_selector("tr.po-size td span.po-break-word")).text_content()
    except:
        size = "Not Available"
    return size

# Extract the material of the products
async def get_material(page):
    try:
        material = await (await page.query_selector("tr.po-back.material td span.po-break-word")).text_content()
    except:
        material = "Not Available"
    return material

# Extract the connectivity technology of the products
async def get_connectivity_technology(page):
    try:
        connectivity_technology = await (await page.query_selector("tr.po-connectivity_technology td span.po-break-word")).text_content()
    except:
        connectivity_technology = "Not Available"
    return connectivity_technology

# Extract the connecter type of the products
async def get_connector_type(page):
    try:
        connector_type = await (await page.query_selector("tr.po-connector_type td span.po-break-word")).text_content()
    except:
        connector_type = "Not Available"
    return connector_type

# Extract the supportive compatible devices of the products
async def get_compatible_devices(page):
    try:
        compatible_devices = await (await page.query_selector("tr.po-compatible_devices td span.po-break-word")).text_content()
    except:
        compatible_devices = "Not Available"
    return compatible_devices


# Extract all data
async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        await page.goto('https://www.amazon.in/gp/goldbox?deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%252215C82F45284EDD496F94A2C368D1B4BD%2522%252C%2522sorting%2522%253A%2522BY_SCORE%2522%257D')
        product_links = await get_product_links(page)

        data = []
        # Get the product data
        for link in product_links:
            await perform_request_with_retry(page, link)
            product_name = await get_product_name(page)
            brand = await get_brand(page)
            star_rating = await get_star_rating(page)
            num_ratings = await get_num_ratings(page)
            original_price = await get_original_price(page)
            offer_price = await get_offer_price(page)
            color = await get_color(page)
            size = await get_size(page)
            material = await get_material(page)
            connectivity_technology = await get_connectivity_technology(page)
            connector_type = await get_connector_type(page)
            compatible_devices = await get_compatible_devices(page)
            data.append((link, product_name, brand, star_rating, num_ratings, original_price, offer_price,  color, size, material, connectivity_technology, connector_type, compatible_devices))
        
        # Save the extracted data to a dataframe
        df = pd.DataFrame(data, columns=['Product Link', 'Product Name', 'Brand', 'Star Rating', 'Number of Ratings', 'Original Price', 'Offer Price', 'Color', 'Size', 'Material', 'Connectivity_technology', 'Connector_type', 'Compatible_devices'])
        # Save the extracted data to a csv file
        df.to_csv('product_details5.csv', index=False)

        print('CSV file has been written successfully.')
        await browser.close()

# Execute the scraping and saving of Amazon today's deals - musical instruments  
if __name__ == '__main__':
    asyncio.run(main())