import time
from requests import get, post, put, Session, options, packages
import logging as log


class TransferWiseApi:
    """ Class that determines the API Actions """

    def __init__(self, token, header):
        self.TOKEN = token
        self.HEADER = header

    def connect_to_api(
        self, payload, _get=False, _post=False, _put=False, URL=None, ENDPOINT=None
    ):
        try:
            with Session() as session:
                if _get:
                    try:
                        response = session.get(f"{URL}{ENDPOINT}", headers=self.HEADER)
                        if response.status_code == 200:
                            res = response.json()
                        else:
                            res = response.text
                        return response.status_code, res
                    except Exception as e:
                        log.error(f"API GET / Parse Error:  {e}")
                        return e

                if _post:
                    try:
                        response = post(
                            f"{URL}{ENDPOINT}", headers=self.HEADER, json=payload
                        )
                        if response.status_code in [200, 201, 409, 404]:
                            res = response.json()
                        else:
                            res = response.text

                        return response.status_code, res
                    except Exception as e:
                        log.error(f"API POST / Parse Error:  {e}")

                if _put:
                    try:
                        response = session.put(f"{URL}{ENDPOINT}", headers=self.HEADER)
                        if response.status_code == 200:
                            res = response.json()
                        else:
                            res = response.text
                        return response.status_code, res
                    except Exception as e:
                        log.error(f"API GET / Parse Error:  {e}")
                        return e

        except Exception as e:
            return False
