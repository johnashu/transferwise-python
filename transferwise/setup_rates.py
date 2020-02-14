data = {
    # Currency exchange types
    "FROM": "GBP",
    "TO": "EUR",
    # Amount to create a quote for.
    # we need a Target amount to send to the API but it is not required.
    "SOURCE_AMOUNT": 2500.00,
    "TARGET_AMOUNT": None,
    # Fee for Transferwise.. Take this off the source amount..  Used to display info only.
    "FEE": 9.47,
    # Highest rateyou currently have / want to wait for more.
    "HIGHEST_RATE":1.20467
,
    # Bank / Transferwise Statement Reference
    "REFERENCE": "Bills-Programmatically",
    # Existing Transfer Id to delete if a higher rate is found..
    "HIGHEST_TRANSFER_ID": False,
    # Delay in seconds between checking the rates.
    "DELAY": 5,
}
