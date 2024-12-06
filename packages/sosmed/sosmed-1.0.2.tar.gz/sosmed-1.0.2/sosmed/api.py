# MIT License

# Copyright (c) 2024 AyiinXd

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import aiohttp
import hmac
import hashlib
import os
from json import dumps
from typing import Dict, Optional

from .exceptions import SosmedError, RequiredError
from .types import Response, ResponseAuth


class Api:
    apiToken: Optional[str]
    secret: Optional[str]
    baseUrl: str = "https://api.ayiin.fun/api"
    def __init__(self, apiToken: Optional[str] = None, secret: Optional[str] = None, path: Optional[str] = None):
        self.apiToken = apiToken
        self.secret = secret
        self.path = path if path else "downloads"
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
        }

    def setApiToken(self, apiToken: str):
        self.apiToken = apiToken

    def setSecret(self, secret: str):
        self.secret = secret

    async def auth(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        prompt: bool = False
    ):
        if prompt is True:
            name = input("Input Your Name: ")
            email = input("Input Your Email: ")
        else:
            if not name or not email:
                raise RequiredError("name and email is required if prompt is False")
            name = name
            email = email

        body = {
            "name": name,
            "email": email
        }

        async with aiohttp.ClientSession(headers=self.headers) as session:
            response = await session.post(
                url=f"{self.baseUrl}/auth",
                json=body,
                headers=self.headers
            )
            json = await response.json()
            res: ResponseAuth = ResponseAuth(**json)
            if res.success:
                self.setApiToken(res.data.token)
                self.setSecret(res.data.secret)
                print("[Auth Sosmed] - Sosmed Auth Success now you must set apiToken and secret in Sosmed class.")
                return res.data
            else:
                raise SosmedError(res.message)

    async def post(self, path: str, body: Optional[Dict[str, str]] = None) -> Response:
        if not self.apiToken or not self.secret:
            raise RequiredError("apiToken and secret is required but not found. Please set apiToken and secret in Sosmed class or call 'Sosmed.auth()' method first.")
        signature = await self.createSignature(
            body=body if body else {},
            path=path,
            method="POST"
        )
        self.headers['Xd-Signature'] = signature
        self.headers['Xd-Api-Token'] = self.apiToken
        async with aiohttp.ClientSession(headers=self.headers) as session:
            res = await session.post(
                url=f"{self.baseUrl}{path}",
                json=body,
                headers=self.headers
            )
            json = await res.json()
            res: Response = Response(**json)
            if res.responseSuccess:
                return res
            else:
                raise SosmedError(res.responseMessage)

    def validatePath(self, autoClean: bool = False):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        
        if autoClean:
            for file in os.listdir(self.path):
                try:
                    os.remove(os.path.join(self.path, file))
                except FileNotFoundError:
                    pass

    async def createSignature(
        self,
        body: dict,
        path: str,
        method: str,
    ):
        stringify = dumps(body).replace(" ", "").replace(", ", ",")
        msg = f"METHOD={method}; PATH={path}; TOKEN={self.apiToken}; URL={stringify};"
        print(msg)
        signature = hmac.new(
            bytes(self.secret, 'latin-1'),
            bytes(msg, 'latin-1'),
            hashlib.sha256
        ).hexdigest()
        return signature
