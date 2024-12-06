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


__version__ = "1.0.2"


from typing import Optional

from .api import Api
from .exceptions import SosmedError
from .types import (
    Facebook,
    Instagram,
    TikTok,
    Twitter
)


class Sosmed(Api):
    def __init__(self, apiToken: Optional[str] = None, secret: Optional[str] = None, path: Optional[str] = None):
        super().__init__(
            apiToken=apiToken,
            secret=secret,
            path=path
        )

    async def facebook(self, url: str) -> Facebook:
        res = await self.post(
            path="/facebook",
            body={
                "url": url
            }
        )
        return Facebook(**res.responseData)

    async def instagram(self, url: str) -> Instagram:
        res = await self.post(
            path="/instagram",
            body={
                "url": url
            }
        )
        return Instagram(**res.responseData)

    async def tiktok(self, url: str) -> TikTok:
        res = await self.post(
            path="/tiktok",
            body={
                "url": url
            }
        )
        return TikTok(**res.responseData)

    async def twitter(self, url: str) -> Twitter:
        res = await self.post(
            path="/twitter",
            body={
                "url": url
            }
        )
        return Twitter(**res.responseData)

    async def vaNumber(
        self,
        country: str,
        number: Optional[str] = None,
        inbox: bool = False
    ):
        if inbox is True:
            if not number:
                raise SosmedError(
                    "Parameter 'number' is required when 'inbox' is True"
                )
            data = {
                "country": country,
                "number": number,
                "inbox": True
            }
        else:
            data = {
                "country": country
            }
        res = await self.post(
            path="/vaNumber",
            body=data
        )
        return res
