BASE_URL = "https://api.transferwise.com/v1/"
PROFILE = "profiles"
RATES = "rates?source={}&target={}"
QUOTE = "quotes"
LIST_RECIPIENTS = "accounts?profile={}&currency={}"
TRANSFERS = "transfers"
CANCEL_TRANSFER = "transfers/{}/cancel"

TOKEN = "42cb7f24-97c8-4714-8c6d-2c4b7adb3ab3"

HEADER = {"Authorization": "Bearer" + TOKEN, "Content-Type": "application/json"}

profileId = "2790522"

# bank account to fund.
# rabo personal
TARGET_ACCOUNT = 7533897
