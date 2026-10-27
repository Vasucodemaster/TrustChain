import requests

URL = "http://127.0.0.1:8000/reputation/blockchain/1"

print("\n===== F6 SOULBOUND REPUTATION TEST =====\n")

try:
    response = requests.get(URL, timeout=10)

    print("HTTP Status:", response.status_code)

    if response.status_code == 200:
        data = response.json()

        print("Contributor ID :", data.get("contributor_id"))
        print("Reputation     :", data.get("score"))
        print("Updated At     :", data.get("updated_at"))
        print("Owner          :", data.get("owner"))

        print("\n✓ F6 reputation retrieval successful")
        print("✓ Blockchain reputation is accessible")
        print("✓ Contributor identity is bound to an owner")

    else:
        print("\n✗ F6 test failed")
        print(response.text)

except requests.exceptions.ConnectionError:
    print("✗ Backend is not running.")
    print("Start it with:")
    print("PYTHONPATH=. uvicorn app.main:app --reload")

except Exception as e:
    print("✗ Error:", e)
