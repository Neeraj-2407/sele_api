from seleniumwire import webdriver
import json
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests

# -----------------------------
# Start Browser
# -----------------------------
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

driver.get("http://localhost:4200/")

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
# Handle Alert Popup
# -----------------------------
from selenium.common.exceptions import NoAlertPresentException
import time

print("Sign In clicked... waiting for dashboard")

# -----------------------------
# Wait while loading panel exists
# -----------------------------
while True:
    try:
        # Check for alert popup
        alert = driver.switch_to.alert
        print("⚠ Alert detected:", alert.text)
        alert.accept()
        print("✅ Alert accepted")

    except NoAlertPresentException:
        pass

    # Check if loading panel still exists
    loading_elements = driver.find_elements(
        By.XPATH,
        "//div[contains(@class,'dx-loadpanel-message') and contains(text(),'Loading')]"
    )

    if len(loading_elements) == 0:
        break

    print("⏳ Loading still in progress...")
    time.sleep(2)

print("✅ Loading finished")
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

# -----------------------------
# Click Analytics Card
# -----------------------------
driver.execute_script(
    "arguments[0].scrollIntoView({block:'center'});", analytics_card
)

wait.until(EC.element_to_be_clickable(analytics_card))

driver.execute_script("arguments[0].click();", analytics_card)

print("Analytics card clicked...")
# -----------------------------
# Wait for Loading to Finish
# -----------------------------
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

# -----------------------------
# Wait for Enquiries Section
# -----------------------------
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

time.sleep(23)
# -------------------------------
import gzip
import json
import os
import hashlib

print("\n===== CAPTURING API PREVIEW DATA =====\n")

# =====================================================
# CREATE FOLDER
# =====================================================

folder = "handler_preview"
os.makedirs(folder, exist_ok=True)

file_index = 1

# =====================================================
# SAVE API RESPONSES
# =====================================================

for request in driver.requests:

    if request.response and "Process/Handler" in request.url:

        try:
            body = request.response.body

            # decompress if gzip
            if request.response.headers.get("Content-Encoding", "") == "gzip":
                body = gzip.decompress(body)

            body = body.decode("utf-8")

            data = json.loads(body)

            file_name = os.path.join(folder, f"api_preview_{file_index}.json")

            with open(file_name, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

            print(f"✅ Saved API response → {file_name}")

            file_index += 1

        except Exception as e:
            print("❌ Error reading response:", e)


# =====================================================
# PROCESS SAVED FILES
# =====================================================

print("\n===== PROCESSING COMPONENT DATA =====\n")

cards = {}
charts = {}
pies = {}
tables = {}

seen_hashes = set()
selected_files = []

for file in os.listdir(folder):

    if not file.endswith(".json"):
        continue

    path = os.path.join(folder, file)

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        component_data = data.get("ComponentData")

        # 1️⃣ Check ComponentData exists
        if not component_data:
            print(f"❌ No ComponentData in {file}")
            continue

        # 2️⃣ Remove duplicate ComponentData
        component_hash = hashlib.md5(
            json.dumps(component_data, sort_keys=True).encode()
        ).hexdigest()

        if component_hash in seen_hashes:
            print(f"⚠ Duplicate skipped → {file}")
            continue

        seen_hashes.add(component_hash)
        selected_files.append(file)

        print(f"✅ Processing → {file}")

        # =====================================================
        # EXTRACT COMPONENTS
        # =====================================================

        for item in component_data:

            key = item.get("Key")
            value = item.get("Value", {})

            component_type = value.get("componentType")

            component = value.get("component", {})
            comp_data = component.get("Data")

            # =====================================================
            # KPI CARDS
            # =====================================================

            if component_type == "KPI":

                if isinstance(comp_data, dict):

                    label = comp_data.get("kpiLabel")
                    kpi_value = comp_data.get("kpiValue")

                    if label and label not in cards:
                        cards[label] = kpi_value

            # =====================================================
            # CHARTS (Line / MixTimeline / Bar etc)
            # =====================================================

            elif isinstance(comp_data, dict) and "series" in comp_data:

                if key not in charts:
                    charts[key] = {
                        "months": comp_data.get("xAxis"),
                        "series": comp_data.get("series")
                    }

            # =====================================================
            # PIE CHART
            # =====================================================

            elif component_type == "Pie":

                if isinstance(comp_data, list):

                    if key not in pies:
                        pies[key] = comp_data

            # =====================================================
            # TABLE
            # =====================================================

            elif component_type == "Table":

                table_data = comp_data.get("Data") if isinstance(comp_data, dict) else None

                if table_data and key not in tables:
                    tables[key] = table_data

    except Exception as e:
        print(f"❌ Error reading {file}: {e}")


# =====================================================
# SAVE EXTRACTED DATA
# =====================================================

print("\n===== SAVING EXTRACTED DATA =====\n")

with open(os.path.join(folder, "cards.json"), "w") as f:
    json.dump(cards, f, indent=4)

with open(os.path.join(folder, "charts.json"), "w") as f:
    json.dump(charts, f, indent=4)

with open(os.path.join(folder, "pies.json"), "w") as f:
    json.dump(pies, f, indent=4)

with open(os.path.join(folder, "tables.json"), "w") as f:
    json.dump(tables, f, indent=4)

print("\n===== EXTRACTION SUMMARY =====\n")

print("✅ Cards extracted:", len(cards))
print("Card Names:")
for name in cards.keys():
    print("   •", name)

print("\n✅ Charts extracted:", len(charts))
print("Chart Names:")
for name in charts.keys():
    print("   •", name)

print("\n✅ Pie charts extracted:", len(pies))
print("Pie Chart Names:")
for name in pies.keys():
    print("   •", name)

print("\n✅ Tables extracted:", len(tables))
print("Table Names:")
for name in tables.keys():
    print("   •", name)

print("\nSelected Files Used:")
for f in selected_files:
    print("   •", f)

"""
# Load JSON
with open("api_preview_24.json", "r") as f:
    data = json.load(f)

# Extract ComponentData
component_data = data.get("ComponentData")

# LLM API
url = "http://192.168.0.200:11434/api/generate"

payload = {
    "model": "llama3.2:3b",
    "prompt": f"Summarize following ComponentData into a clear business summary:\n\n{json.dumps(component_data, indent=2)}",
    "stream": False
}

try:
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        result = response.json()
        final_summary = result.get("response", "").strip()

        if not final_summary:
            print("❌ Summary is empty.")
            exit()

        print("✅ Summary Generated Successfully")
        print(final_summary)

    else:
        print("❌ API Error:", response.status_code)
        print(response.text)
        exit()

except Exception as e:
    print("❌ Exception during summary:", e)
    exit()


# =====================================================
# SEND EMAIL WITH SUMMARY
# =====================================================

try:
    email_payload = {
        "email": "neerajwings1@gmail.com",
        "cc": "neerajsainandigama@gmail.com",
        "subject": "Automated Business Summary Report",
        "message": final_summary   # 🔑 summarized text goes here
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
"""
input("Press Enter to close browser...")

driver.quit()