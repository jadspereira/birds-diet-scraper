# This script lists "speciescode" from Birds of the World website, up to the defined limit number.
# The Selenium library mimics user scrolling and page inspection behavior to capture species codes
# These codes are stored in a list and then converted to a CSV spreadsheet for verification
# The Edge browser was used, hence the selenium.webdriver.edge.service and selenium.webdriver.edge.options webdriver

# Modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
import time
import csv

# Function to find species codes
def list_speciescodes(limit):
    service = Service(executable_path='C:/Users/User/Downloads/edgedriver_win32/msedgedriver.exe') # webdriver path
    driver = webdriver.Edge(service=service)
    
    driver.get('https://birdsoftheworld.org/bow/species') # Birds of the World URL

    # Set to store unique values
    speciescodes = set()

    # Scroll down 300 pixels to load new records
    for i in range(100000):  # Adjust number of iterations as needed
        driver.execute_script("window.scrollBy(0, 50);")  # Scrolls 300 pixels down
        time.sleep(0.05)  # 1 second pause to allow loading more records

    # Search for species code in website HTML (many ifs, but it works)
    while len(speciescodes) < limit:
        # Locate elements containing speciescodes
        elements = driver.find_elements(By.XPATH, "//div[@data-speciescode]")  # div where speciescode is
        
        for element in elements:
            # Get attribute value
            speciescode = element.get_attribute("data-speciescode")
            scientific_name_element = element.find_element(By.XPATH, ".//a/span[@class='Heading-sub Heading-sub--inline Heading-sub--sci']")
            scientific_name = scientific_name_element.text.strip() # remove space

            speciescodes.add((speciescode, scientific_name))  # Add to set
            
            if len(speciescodes) >= limit:  # If desired number is reached, break
                break

        if len(speciescodes) < limit: # Maybe I can remove this if (?)
            # Continue scrolling
            driver.execute_script("window.scrollBy(0, 100);")  # Another 300px
            time.sleep(0.08)  # Pause

    # Close when finished
    driver.quit()

    # Save to CSV file
    with open('speciescodes.csv', mode='w', newline='') as file:
        writer = csv.writer(file, delimiter= ',', quotechar= '"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['speciescode', 'speciename'])  # Add header
        for code, name in speciescodes:
            writer.writerow([code,name])

    print(f"Collected {len(speciescodes)} speciescodes and saved to 'speciescodes.csv' file.") # Completion message

# Define total number of species in Birds of the World
list_speciescodes(100) 

# End of script