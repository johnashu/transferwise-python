import time
from requests import get, post, put, Session, options, packages
import logging as log

# suppress warnings..
from requests.packages.urllib3.exceptions import InsecureRequestWarning

packages.urllib3.disable_warnings(InsecureRequestWarning)

from config import *


class TransferWiseApi:
    """ Class that determines the API Actions """

    def __init__(self, token):
        self.TOKEN = token

    def connect_to_api(
        self, payload, _get=False, _post=False, _put=False, URL=None, ENDPOINT=None
    ):
        try:
            with Session() as session:
                if _get:
                    try:
                        response = session.get(f"{URL}{ENDPOINT}", headers=HEADER)
                        log.debug(
                            f"\n\n\tSTATUS CODE:  {response.status_code}\n\nRESPONSE  ::  {response.text}"
                        )
                        if response.status_code == 200:
                            res = response.json()
                        else:
                            res = response.text
                        return response.status_code, res
                    except Exception as e:
                        log.debug("API GET / Parse Error:  {}".format(e))
                        return e

                if _post:
                    try:
                        response = post(
                            f"{URL}{ENDPOINT}", headers=HEADER, json=payload
                        )
                        if response.status_code in [200, 201, 409, 404]:
                            res = response.json()
                        else:
                            res = response.text

                        return response.status_code, res
                    except Exception as e:
                        print("API POST / Parse Error:  {}".format(e))
                        pass

                if _put:
                    try:
                        response = session.put(f"{URL}{ENDPOINT}", headers=HEADER)
                        log.debug(
                            f"\n\n\tSTATUS CODE:  {response.status_code}\n\nRESPONSE  ::  {response.text}"
                        )
                        if response.status_code == 200:
                            res = response.json()
                        else:
                            res = response.text
                        return response.status_code, res
                    except Exception as e:
                        log.debug("API GET / Parse Error:  {}".format(e))
                        return e

        except Exception as e:
            return False
