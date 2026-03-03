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
# Example Usage
# -----------------------------

html_data = """
<html>
  <body>
    <h1>Sales Report</h1>
    <p>This dashboard shows the monthly sales performance of the company.</p>
    <p>Total revenue increased by 15% compared to last month.</p>
  </body>
</html>
"""

summary = summarize_html(html_data)

# Store summarized text in variable
final_summary = summary

print("\nData Type:", type(final_summary))
print("\nSummarized Text:\n")
print(final_summary)