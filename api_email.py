import requests
import json

def send_email(summary_text):
    api_endpoint = "http://127.0.0.1:8001/send-email/"

    payload = {
        "email": "neerajwings1@gmail.com",   # ✅ Correct field name
        "subject": "Automated Summary Report",
        "message": summary_text
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            api_endpoint,
            headers=headers,
            data=json.dumps(payload)
        )

        if response.status_code == 200:
            print("✅ Email sent successfully!")
        else:
            print("❌ Failed to send email")
            print("Status Code:", response.status_code)
            print("Response:", response.text)

    except Exception as e:
        print("❌ Error occurred while sending email:", e)


# Example usage
summarized_text = """
Sales Report Summary:
- Revenue increased by 15%.
- Customer engagement improved.
- Overall business performance is strong.
"""

send_email(summarized_text)