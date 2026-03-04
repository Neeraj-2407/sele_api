from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
# -----------------------------
# Start Browser
# -----------------------------
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

driver.get("http://192.168.0.152:4200")

wait = WebDriverWait(driver, 20)

# -----------------------------
# Enter Company Name
# -----------------------------
company_name_input = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "/html/body/app-root/app-login_04/div/div[2]/div/div[2]/form/div[1]/dx-text-box/div/div[2]/input"
    ))
)
company_name_input.clear()
company_name_input.send_keys("Analytics")

# -----------------------------
# Enter User Name
# -----------------------------
user_name_input = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "/html/body/app-root/app-login_04/div/div[2]/div/div[2]/form/div[2]/dx-text-box/div/div[2]/input"
    ))
)
user_name_input.clear()
user_name_input.send_keys("super user")

# -----------------------------
# Enter Password
# -----------------------------
password_input = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "/html/body/app-root/app-login_04/div/div[2]/div/div[2]/form/div[3]/dx-text-box/div/div[2]/input"
    ))
)
password_input.clear()
password_input.send_keys("a")

# -----------------------------
# Click Sign In
# -----------------------------
sign_in_button = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "/html/body/app-root/app-login_04/div/div[2]/div/div[2]/form/div[5]"
    ))
)
sign_in_button.click()

print("Sign In clicked... waiting for dashboard")

# -----------------------------
# Wait Until Login Completes
# -----------------------------
logout_button = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//img[contains(@src,'log-out.svg')]"
    ))
)

print("✅ Login successful!")

# -----------------------------
# Click Logout
# -----------------------------
driver.execute_script("arguments[0].click();", logout_button)

print("Logout clicked successfully!")

# -----------------------------
# Click Wings Analytics Button
# -----------------------------
wings_analytics_button = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "/html/body/app-root/app-recent-users01/div/div[3]/div[1]"
    ))
)

wings_analytics_button.click()

print("Wings Analytics button clicked!")

# Optional: Wait few seconds to load next page
wait.until(EC.staleness_of(wings_analytics_button))

print("Wings Analytics page loaded!")
time.sleep(2)

analytics_card = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "/html/body/app-root/lib-analytics-recent-users/div/div[2]/div/div[2]/dx-scroll-view/div[1]/div/div[1]/div[2]/div/div/mat-card/mat-card-content/div[1]"
    ))
)

analytics_card.click()

print("Analytics card clicked... waiting for next page")

# Wait until old element becomes stale (DOM refreshed)
wait.until(EC.staleness_of(analytics_card))

print("Next page loaded successfully!")

# -----------------------------
# Click Enquiries
# -----------------------------
enquiries_button = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//div[contains(@class,'accordion-title')]//span[normalize-space()='Enquiries']"
    ))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", enquiries_button)
driver.execute_script("arguments[0].click();", enquiries_button)

print("Enquiries clicked...")

# Wait until Sales becomes visible
wait.until(
    EC.visibility_of_element_located((
        By.XPATH,
        "//div[contains(@class,'accordion-title')]//span[normalize-space()='Sales']"
    ))
)

# -----------------------------
# Click Sales
# -----------------------------
sales_button = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//div[contains(@class,'accordion-title')]//span[normalize-space()='Sales']"
    ))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", sales_button)
driver.execute_script("arguments[0].click();", sales_button)

print("Sales button clicked successfully!")

# -----------------------------
# Click Descriptive (Full XPath)
# -----------------------------
descriptive_button = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "/html/body/app-root/lib-analytics-welcome/div/div[2]/aside/div/div[2]/dx-accordion/div/div[3]/div[2]/div/button"
    ))
)

# Scroll into view (important for Angular side menus)
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", descriptive_button)

# Small stabilization (optional)
time.sleep(1)

# Click using JS (safer for Angular components)
driver.execute_script("arguments[0].click();", descriptive_button)

print("Descriptive clicked... waiting for page content")

# Wait for new Angular content to load
wait.until(
    EC.visibility_of_element_located((By.CLASS_NAME, "content-area"))
)

print("✅ Descriptive page loaded successfully!")
# -----------------------------
# Scrape KPI Card Titles & Values
# -----------------------------

kpi_data = {}   # Dictionary variable

try:
    # Locate Key Metrics section
    key_metrics_section = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//div[.//span[normalize-space()='Key Metrics']]"
        ))
    )

    # Get all KPI card components
    cards = key_metrics_section.find_elements(By.XPATH, ".//app-kpicharts")

    for card in cards:
        try:
            # Extract title
            title = card.find_element(By.XPATH, ".//div[1]//span").text.strip()

            # Extract value
            value = card.find_element(By.XPATH, ".//div[2]//span").text.strip()

            if title and value:
                kpi_data[title] = value

        except:
            continue

    print("✅ KPI Data Successfully Scraped.\n")

except Exception as e:
    print("❌ Failed to scrape KPI data.")
    print("Error:", e)

# -----------------------------
# Print Dictionary
# -----------------------------
print("KPI Dictionary:\n")
print(kpi_data)

import requests
import json

def summarize_dictionary(data_dict):
    """
    Sends dictionary data to LLM API and returns summarized text.
    """

    url = "http://192.168.0.200:11434/api/generate"

    payload = {
        "model": "llama3.2:3b",
        "prompt": f"Convert the following KPI dictionary into a clear business summary:\n\n{json.dumps(data_dict, indent=2)}",
        "stream": False
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            result = response.json()
            summarized_text = result.get("response", "")
            print("✅ API Call Successful")
            return summarized_text
        else:
            print("❌ API Error:", response.status_code)
            return None

    except Exception as e:
        print("❌ Exception occurred:", e)
        return None


# -----------------------------
# Use Your Scraped Dictionary
# -----------------------------

if kpi_data and isinstance(kpi_data, dict):

    summary = summarize_dictionary(kpi_data)

    final_summary = summary

    print("\nData Type:", type(final_summary))
    print("\nSummarized Text:\n")
    print(final_summary)

else:
    print("❌ No KPI data available to summarize.")
    
input("Press Enter to close browser...")
driver.quit()