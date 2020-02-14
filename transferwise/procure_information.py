from transferwise_api import TransferWiseApi
from config import *


def pprint_res(lst):
    for x in lst:
        for k, v in x.items():
            if not isinstance(v, dict):
                print(f"{k}  ::  {v}")
            else:
                for k1, v1 in v.items():
                    print(f"{k1}  ::  {v1}")
        print()


tw = TransferWiseApi()

code, profile = tw.connect_to_api(None, _get=True, URL=BASE_URL, ENDPOINT=PROFILE)

LIST_RECIPIENTS = LIST_RECIPIENTS.format(profileId, "EUR")

code, recipients_list = tw.connect_to_api(
    None, _get=True, URL=BASE_URL, ENDPOINT=LIST_RECIPIENTS
)

pprint_res(profile)
pprint_res(recipients_list)
