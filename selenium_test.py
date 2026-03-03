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

input("Press Enter to close browser...")
driver.quit()