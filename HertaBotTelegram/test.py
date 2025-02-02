import httpx

try:
    r = httpx.get("https://api.telegram.org")
    print(r.status_code, r.text)
except Exception as e:
    print("Error reaching Telegram:", e)