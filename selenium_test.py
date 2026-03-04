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

# =====================================================
# FUNCTION: Scrape KPI → Summarize → Send Email
# =====================================================

import requests
import json

def process_kpi_data(driver, wait):

    # -----------------------------
    # 1️⃣ SCRAPE KPI DATA
    # -----------------------------
    kpi_data = {}

    try:
        key_metrics_section = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//div[.//span[normalize-space()='Key Metrics']]"
            ))
        )

        cards = key_metrics_section.find_elements(By.XPATH, ".//app-kpicharts")

        for card in cards:
            try:
                title = card.find_element(By.XPATH, ".//div[1]//span").text.strip()
                value = card.find_element(By.XPATH, ".//div[2]//span").text.strip()

                if title and value:
                    kpi_data[title] = value

            except:
                continue

        print("✅ KPI Data Successfully Scraped.")
        print("KPI Dictionary:", kpi_data)

    except Exception as e:
        print("❌ Failed to scrape KPI data.")
        print("Error:", e)
        return


    # -----------------------------
    # 2️⃣ SUMMARIZE USING LLM
    # -----------------------------
    url = "http://192.168.0.200:11434/api/generate"

    payload = {
        "model": "llama3.2:3b",
        "prompt": f"Convert the following KPI dictionary into a clear business summary:\n\n{json.dumps(kpi_data, indent=2)}",
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            result = response.json()
            final_summary = result.get("response", "").strip()

            if not final_summary:
                print("❌ Summary is empty.")
                return

            print("✅ Summary Generated Successfully")
            print("\nSummarized Text:\n")
            print(final_summary)

        else:
            print("❌ API Error:", response.status_code)
            print(response.text)
            return

    except Exception as e:
        print("❌ Exception during summary:", e)
        return


    # -----------------------------
    # 3️⃣ SEND EMAIL
    # -----------------------------
    try:
        email_payload = {
            "email": "neerajwings1@gmail.com",
            "cc": "neerajsainandigama@gmail.com",
            "subject": "Automated Business Summary Report",
            "message": final_summary
        }

        email_response = requests.post(
            "http://127.0.0.1:8000/send-email/",
            json=email_payload
        )

        if email_response.status_code == 200:
            print("✅ Email sent successfully")
        else:
            print("❌ Failed to send email")
            print("Status Code:", email_response.status_code)
            print("Response:", email_response.text)

    except Exception as e:
        print("❌ Error sending email:", e)


# =====================================================
# CALL THE FUNCTION
# =====================================================

process_kpi_data(driver, wait)


# =====================================================
# CLOSE BROWSER
# =====================================================

input("Press Enter to close browser...")
driver.quit()