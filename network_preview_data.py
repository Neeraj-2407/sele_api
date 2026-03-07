from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import gzip
import json
import time

# Start Browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

driver.get("http://localhost:4200/")

wait = WebDriverWait(driver, 20)

# Enter Company Name

company_name_input = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "/html/body/app-root/app-login_04/div/div[2]/div/div[2]/form/div[1]/dx-text-box/div/div[2]/input"
    ))
)
company_name_input.clear()
company_name_input.send_keys("Analytics")

# Enter User Name

user_name_input = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "/html/body/app-root/app-login_04/div/div[2]/div/div[2]/form/div[2]/dx-text-box/div/div[2]/input"
    ))
)
user_name_input.clear()
user_name_input.send_keys("super user")

# Enter Password

password_input = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "/html/body/app-root/app-login_04/div/div[2]/div/div[2]/form/div[3]/dx-text-box/div/div[2]/input"
    ))
)
password_input.clear()
password_input.send_keys("a")

# Click Sign In

sign_in_button = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "/html/body/app-root/app-login_04/div/div[2]/div/div[2]/form/div[5]"
    ))
)
sign_in_button.click()

print("Sign In clicked... waiting for dashboard")

# Handle Alert Popup

from selenium.common.exceptions import NoAlertPresentException
import time

print("Sign In clicked... waiting for dashboard")

# Wait while loading panel exists

while True:
    try:
        # Check for alert popup
        alert = driver.switch_to.alert
        print(" Alert detected:", alert.text)
        alert.accept()
        print(" Alert accepted")

    except NoAlertPresentException:
        pass

    # Check if loading panel still exists
    loading_elements = driver.find_elements(
        By.XPATH,
        "//div[contains(@class,'dx-loadpanel-message') and contains(text(),'Loading')]"
    )

    if len(loading_elements) == 0:
        break

    print(" Loading still in progress...")
    time.sleep(2)

print(" Loading finished")

# Wait Until Login Completes

logout_button = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//img[contains(@src,'log-out.svg')]"
    ))
)

print(" Login successful!")


# Click Logout

driver.execute_script("arguments[0].click();", logout_button)

print("Logout clicked successfully!")


# Click Wings Analytics Button

wings_analytics_button= wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "/html/body/app-root/app-recent-users01/div/div[3]/div[1]"
    ))
)

driver.execute_script("arguments[0].click();", wings_analytics_button)

print("Wings Analytics clicked")

# Wait until next page / analytics card is visible

analytics_card = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "/html/body/app-root/lib-analytics-recent-users/div/div[2]/div/div[2]/dx-scroll-view/div[1]/div/div[1]/div[2]/div/div/mat-card/mat-card-content/div[1]"
    ))
)

# Click Analytics Card

driver.execute_script(
    "arguments[0].scrollIntoView({block:'center'});", analytics_card
)

wait.until(EC.element_to_be_clickable(analytics_card))

driver.execute_script("arguments[0].click();", analytics_card)

print("Analytics card clicked...")

# Wait for Loading to Finish

try:
    WebDriverWait(driver, 60).until(
        EC.invisibility_of_element_located((
            By.XPATH,
            "//div[contains(@class,'dx-loadpanel-message') and contains(text(),'Loading')]"
        ))
    )
    print("Loading finished")
except:
    print("Loading element not detected or already finished")

# Wait for Enquiries Section

enquiries_button = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//span[normalize-space()='Enquiries']"
    ))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", enquiries_button)
driver.execute_script("arguments[0].click();", enquiries_button)

print("Enquiries clicked successfully")

# Wait until Sales becomes visible
wait.until(
    EC.visibility_of_element_located((
        By.XPATH,
        "//div[contains(@class,'accordion-title')]//span[normalize-space()='Sales']"
    ))
)

# Click Sales

sales_button = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//div[contains(@class,'accordion-title')]//span[normalize-space()='Sales']"
    ))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", sales_button)
driver.execute_script("arguments[0].click();", sales_button)

print("Sales button clicked successfully!")

# Click Descriptive (Full XPath)

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



print(" Descriptive page loaded successfully!")

time.sleep(23)

print("\n===== CAPTURING REQUIRED API PREVIEW DATA =====\n")

# CREATE FOLDER

folder = "handler_preview"
os.makedirs(folder, exist_ok=True)

best_data = None
max_components = 0

# CAPTURE REQUIRED API RESPONSE

for request in driver.requests:

    if request.response and "Process/Handler" in request.url:

        try:
            body = request.response.body

            # decompress if gzip
            if request.response.headers.get("Content-Encoding", "") == "gzip":
                body = gzip.decompress(body)

            body = body.decode("utf-8")

            data = json.loads(body)

            component_data = data.get("ComponentData")

            if component_data:

                count = len(component_data)
                print(f"Found ComponentData with {count} components")

                if count > max_components:
                    max_components = count
                    best_data = data

        except Exception as e:
            print(" Error reading response:", e)

# SAVE ONLY REQUIRED JSON FILE

file_path = os.path.join(folder, "required_component_data.json")

if best_data:

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(best_data, f, indent=4)

    print(f"\n Saved required file → {file_path}")

else:
    print(" No ComponentData found")

# PROCESS COMPONENT DATA

print("\n===== PROCESSING COMPONENT DATA =====\n")

cards = {}
charts = {}
pies = {}
tables = {}

component_data = best_data.get("ComponentData", [])

for item in component_data:

    key = item.get("Key")
    value = item.get("Value", {})

    component_type = value.get("componentType")

    component = value.get("component", {})
    comp_data = component.get("Data")

    # KPI CARDS
  
    if component_type == "KPI":

        if isinstance(comp_data, dict):

            label = comp_data.get("kpiLabel")
            kpi_value = comp_data.get("kpiValue")

            if label:
                cards[label] = kpi_value

    # CHARTS

    elif isinstance(comp_data, dict) and "series" in comp_data:

        charts[key] = {
            "months": comp_data.get("xAxis"),
            "series": comp_data.get("series")
        }

    # PIE CHART

    elif component_type == "Pie":

        if isinstance(comp_data, list):
            pies[key] = comp_data

    # TABLE

    elif component_type == "Table":

        table_data = comp_data.get("Data") if isinstance(comp_data, dict) else None

        if table_data:
            tables[key] = table_data

# PRINT SUMMARY

print("\n===== EXTRACTION SUMMARY =====\n")

print(" Cards extracted:", len(cards))
print("Card Names:")
for name in cards:
    print("   •", name)

print("\n Charts extracted:", len(charts))
print("Chart Names:")
for name in charts:
    print("   •", name)

print("\n Pie charts extracted:", len(pies))
print("Pie Chart Names:")
for name in pies:
    print("   •", name)

print("\n Tables extracted:", len(tables))
print("Table Names:")
for name in tables:
    print("   •", name)

input("Press Enter to close browser...")

driver.quit()