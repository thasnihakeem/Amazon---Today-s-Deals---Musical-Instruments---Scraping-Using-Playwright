# Importing libraries
import csv
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        await page.goto('https://www.amazon.in/gp/goldbox?deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%252215C82F45284EDD496F94A2C368D1B4BD%2522%252C%2522sorting%2522%253A%2522BY_SCORE%2522%257D')

# Fetching all resulted product links

        all_items = await page.query_selector_all('.a-link-normal.DealCardDynamic-module__linkOutlineOffset_2XU8RDGmNg2HG1E-ESseNq')     
        product_links = []
        for item in all_items:
            link = await item.get_attribute('href')
            product_links.append(link)

        with open('product_details.csv', 'w', newline='', encoding='utf-8') as csvfile:

            writer = csv.writer(csvfile)
            writer.writerow(['Product Link', 'Product Name', 'Brand', 'Star Rating', 'Number of Ratings', 'Original Price', 'Offer Price', 'Color', 'Size', 'Material', 'Connectivity_technology', 'Connector_type', 'Compatible_devices'])
            
            for link in product_links:
                await page.goto(link)
                
# Scraping data like 'Product Link', 'Product Name', 'Brand', 'Star Rating', 'Number of Ratings', 'Original Price', 'Offer Price', 'Color', 'Size', 'Material', 'Connectivity_technology', 'Connector_type', 'Compatible_devices'               

                # product_name
                try:                                                                                  #try to get the data
                    product_name = await (await page.query_selector("#productTitle")).text_content()
                except:                                                                               #if the data is not found, print the error message
                    product_name = "Not Available"
                
                # star_rating
                try:                                                                                  #try to get the data
                    star_rating = await (await page.query_selector(".a-icon-alt")).text_content()
                    star_rating = star_rating.split(" ")[0]                                           #Removing unwanted characters
                except:                                                                               #if the data is not found,
                    star_rating = "Not Available"
                
                # num_ratings
                try:                                                                                            #try to get the data
                    ratings_text = await (await page.query_selector("#acrCustomerReviewText")).text_content()
                    num_ratings = ratings_text.split(" ")[0]                                                    #Removing unwanted characters
                except:                                                                                         #if the data is not found,   
                    num_ratings = "Not Available"
                
                # original_price
                try:                                                                                               #try to get the data
                    original_price = await (await page.query_selector(".a-price.a-text-price")).text_content()
                    original_price = original_price.split("₹")[1]                                                  #Removing unwanted characters
                except:                                                                                            #if the data is not found,
                    original_price = "Not Available"
                
                # offer_price
                try:                                                                                    #try to get the data
                    offer_price = await (await page.query_selector(".a-price-whole")).text_content()
                except:                                                                                 #if the data is not found,
                    offer_price = "Not Available"
                
                # brand
                try:                                                                                                #try to get the data
                    brand = await (await page.query_selector("tr.po-brand td span.po-break-word")).text_content()
                except:                                                                                             #if the data is not found,
                    brand = "Not Available"v
                
                # color
                try:                                                                                                #try to get the data
                    color = await (await page.query_selector("tr.po-color td span.po-break-word")).text_content()
                except:                                                                                             #if the data is not found,
                    color = "Not Available"
                    
                # size
                try:                                                                                                #try to get the data
                    size = await (await page.query_selector("tr.po-size td span.po-break-word")).text_content()
                except:                                                                                             #if the data is not found,
                    size = "Not Available"
                    
                # material
                try:                                                                                                           #try to get the data
                    material = await (await page.query_selector("tr.po-back.material td span.po-break-word")).text_content()
                except:                                                                                                        #if the data is not found,
                    material = "Not Available"
                    
                # connectivity_technology
                try:                                                                                                                                   #try to get the data
                    connectivity_technology = await (await page.query_selector("tr.po-connectivity_technology td span.po-break-word")).text_content()
                except:                                                                                                                                #if the data is not found,
                    connectivity_technology = "Not Available"
                    
                # connector_type
                try:                                                                                                                 #try to get the data
                    connector_type = await (await page.query_selector("tr.po-connector_type td span.po-break-word")).text_content()
                except:                                                                                                              #if the data is not found,
                    connector_type = "Not Available"
                    
                #  compatible_devices
                try:                                                                                                                         #try to get the data
                    compatible_devices = await (await page.query_selector("tr.po-compatible_devices td span.po-break-word")).text_content()
                except:                                                                                                                      #if the data is not found,
                    compatible_devices = "Not Available"

                writer.writerow([link, product_name, brand, star_rating, num_ratings, original_price, offer_price,  color, size, material, connectivity_technology, connector_type, compatible_devices])

        print('CSV file has been written successfully.')
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())

