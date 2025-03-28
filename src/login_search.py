import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
import pandas as pd
import time

# Webdriver path
service = Service(executable_path='C:/Users/User/Downloads/edgedriver_win32/msedgedriver.exe')
driver = webdriver.Edge(service=service)

# Login function (copied from login.py)
def login():
    login_url = "https://secure.birds.cornell.edu/cassso/login?service=https%3A%2F%2Fbirdsoftheworld.org%2Flogin%2Fcas"
    driver.get(login_url)
    time.sleep(2)
    
    username_input = driver.find_element(By.ID, "input-user-name")
    password_input = driver.find_element(By.ID, "input-password")
    
    username_input.send_keys("your_user")  # username
    password_input.send_keys("your_password")  # password
    
    submit_button = driver.find_element(By.ID, "form-submit")
    submit_button.click()
    time.sleep(5)
    
    # Verify login
    if "bow/home" in driver.current_url:
        print("✅ Login successful")
    else:
        print("❌ Login failed:", driver.current_url)
        driver.quit()
        exit()

# Search food habits
def search_food(species_code):
    try:
        url = f"https://birdsoftheworld.org/bow/species/{species_code}/cur/introduction#food"
        driver.get(url)
        time.sleep(3)  # 3 second pause for page loading
        
        # Check if correct page loaded
        if species_code not in driver.current_url:
            print(f"❌ Failed to access page for {species_code}")
            return False
        
        # Full page text
        page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        
        # Search for keywords using REGEX - was finding all instances before
        keywords = [r'\bant\b', r'\bhymenoptera\b', r'\bants\b']
        
        # Check if any regex matches the text
        if any(re.search(keyword, page_text) for keyword in keywords):
            print(f"✅ {species_code}: positive for ants!")
            return True
        else:
            print(f"❌ {species_code}: does not eat ants")
            return False
    
    # Return if any error occurs
    except Exception as e:
        print(f"⚠️ Error with {species_code}: {e}")
        return False

# Main function
def main():
    try:
        login()
        
        # Read species codes list
        species_df = pd.read_csv('speciescodes.csv')
        
        # Empty list for results
        results = []
        
        for index, row in species_df.iterrows():
            species_code = row['speciescode']
            species_name = row['speciename']
            
            found = search_food(species_code)
            results.append({
                'species_code': species_code,
                'species_name': species_name,
                'ant_related': found
            })
        
        # Create CSV with 'True' or 'False' results
        results_df = pd.DataFrame(results)
        results_df.to_csv('diet_results.csv', index=False)
        print("✅ Results saved to 'diet_results.csv'")
    
    finally:
        driver.quit()

# Run the code 
if __name__ == "__main__":
    main()