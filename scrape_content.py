import requests

def scrape(url):
    """
    Scrapes full HTML content of the given URL
    and returns it as a string.
    """
    try:
        response = requests.get(url)

        if response.status_code == 200:
            html_content = response.text
            print("✅ Data Found")
            return html_content
        else:
            print("❌ Failed to retrieve page:", response.status_code)
            return None

    except Exception as e:
        print("❌ Error occurred:", e)
        return None


# Example usage
url = "http://192.168.0.152:4200"
html_data = scrape(url)
print("\nData Type:", type(html_data))

# Print full HTML content
print("\nHTML Content:\n")
print(html_data)