import requests

def get_sec_filings(ticker):
    try:
        url = f"https://data.sec.gov/submissions/CIK{ticker}.json"

        headers = {
            "User-Agent": "your-email@example.com"
        }

        r = requests.get(url, headers=headers)
        data = r.json()

        filings = data.get("filings", {}).get("recent", {})

        forms = filings.get("form", [])
        dates = filings.get("filingDate", [])

        results = []

        for i in range(len(forms)):
            if forms[i] == "8-K":
                results.append({
                    "form": forms[i],
                    "date": dates[i]
                })

        return results[:3]

    except:
        return []
