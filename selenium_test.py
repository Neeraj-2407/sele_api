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
time.sleep(30)

# -----------------------------
# Wait for Login Success
# (Wait for logout icon to appear)
# -----------------------------
logout_button = wait.until(
    EC.presence_of_element_located((
        By.XPATH,
        "//img[contains(@src,'log-out.svg')]"
    ))
)

# -----------------------------
# Click Logout
# -----------------------------
driver.execute_script("arguments[0].click();", logout_button)

print("Login and Logout successful!")

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
time.sleep(20)

print("Analytics card clicked!")

# -----------------------------
# Click "Sales" Accordion
# -----------------------------
sales_button = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//span[text()='Sales']/parent::div"
    ))
)

# Scroll into view (important)
driver.execute_script("arguments[0].scrollIntoView(true);", sales_button)

# Click
driver.execute_script("arguments[0].click();", sales_button)

print("Sales button clicked successfully!")

# -----------------------------
# Click "Descriptive"
# -----------------------------
descriptive_button = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//span[normalize-space()='Descriptive']"
    ))
)

# Scroll into view (important for Angular)
driver.execute_script("arguments[0].scrollIntoView(true);", descriptive_button)

# Click using JS (safer)
driver.execute_script("arguments[0].click();", descriptive_button)

print("Descriptive clicked... waiting for page to load")

# -----------------------------
# Wait Until Page Fully Loads
# -----------------------------

# Option 1: Wait until old element disappears
wait.until(EC.staleness_of(descriptive_button))

print("✅ Descriptive page loaded successfully!")

input("Press Enter to close browser...")
driver.quit()