from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
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

# =====================================================
# CLICK NEXT BUTTON
# =====================================================

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import io

wait = WebDriverWait(driver, 30)

# =====================================================
# CLICK DESCRIPTIVE
# =====================================================

descriptive_button = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "/html/body/app-root/lib-analytics-welcome/div/div[2]/aside/div/div[2]/dx-accordion/div/div[3]/div[2]/div/button"
    ))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", descriptive_button)
time.sleep(1)
driver.execute_script("arguments[0].click();", descriptive_button)

print("Descriptive clicked...")

wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "content-area")))

print("Descriptive page loaded!")

# =====================================================
# CLICK NEXT
# =====================================================

next_button = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "/html/body/app-root/lib-analytics-welcome/div/header/div[1]/button"
    ))
)

driver.execute_script("arguments[0].scrollIntoView({block:'center'});", next_button)
time.sleep(1)
driver.execute_script("arguments[0].click();", next_button)

print("Next button clicked...")

# Wait for page content
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "content-area")))
time.sleep(4)

print("Next page loaded!")

# -------------------------------
# Start Screenshot Process
# -------------------------------

# Scroll to top first
driver.execute_script("window.scrollTo(0,0)")
time.sleep(2)

import os
import time
from selenium.webdriver.common.by import By

print("Starting smart scrolling screenshots...")

# folder for screenshots
os.makedirs("dashboard_screenshots", exist_ok=True)

# find scrollable container
scroll_container = driver.find_element(By.CLASS_NAME, "content-area")

# viewport height of container
viewport_height = driver.execute_script(
    "return arguments[0].clientHeight", scroll_container
)

# total scrollable height
total_height = driver.execute_script(
    "return arguments[0].scrollHeight", scroll_container
)

scroll_position = 0
screenshot_index = 1

while scroll_position < total_height:

    # scroll to position
    driver.execute_script(
        "arguments[0].scrollTop = arguments[1]",
        scroll_container,
        scroll_position
    )

    time.sleep(2)

    # screenshot
    file_name = f"dashboard_screenshots/screenshot_{screenshot_index}.png"
    driver.save_screenshot(file_name)

    print(f"Saved {file_name}")

    # move exactly one viewport down (no overlap)
    scroll_position += viewport_height

    screenshot_index += 1

    # update height (important for lazy loading dashboards)
    total_height = driver.execute_script(
        "return arguments[0].scrollHeight", scroll_container
    )

print("✅ Screenshots captured until page end")
input("Press Enter to close browser...")

driver.quit()