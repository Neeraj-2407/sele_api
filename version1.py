
import re

try:
    # -----------------------------
    # Locate Key Metrics Section
    # -----------------------------
    sub_section = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//div[.//span[normalize-space()='Key Metrics']]"
        ))
    )

    # Get full HTML
    raw_html = sub_section.get_attribute("outerHTML")

    # -----------------------------
    # Remove <script> and <style> tags
    # -----------------------------
    clean_html = re.sub(r"<script.*?>.*?</script>", "", raw_html, flags=re.DOTALL)
    clean_html = re.sub(r"<style.*?>.*?</style>", "", clean_html, flags=re.DOTALL)

    # Store cleaned HTML in variable
    sub_heading_html = clean_html

    print("✅ Successfully scraped the HTML content.")

except Exception as e:
    print("❌ Failed to scrape HTML content.")
    print("Error:", e)

import requests
import json

def summarize_html(html_content):
    """
    Sends HTML content to LLM API and returns summarized text.
    """

    url = "http://192.168.0.200:11434/api/generate"

    payload = {
        "model": "llama3.2:3b",
        "prompt": f"Convert the following HTML content into a clear summarized text:\n\n{html_content}",
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
# Use Scraped HTML Here
# -----------------------------

if sub_heading_html and len(sub_heading_html) > 0:

    summary = summarize_html(sub_heading_html)

    # Store summarized text in variable
    final_summary = summary

    print("\nData Type:", type(final_summary))
    print("\nSummarized Text:\n")
    print(final_summary)

else:
    print("❌ No HTML content available to summarize.")