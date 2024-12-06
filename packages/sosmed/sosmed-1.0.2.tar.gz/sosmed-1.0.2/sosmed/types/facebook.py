# MIT License

# Copyright (c) 2024 AyiinXd

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following "conditions":

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import aiofiles
import aiohttp
import os

from typing import Dict, List, Literal, Optional, Union


class Facebook:
    def __init__(self, **kwargs):
        self.id: str = kwargs.get("id", "")
        self.normalVideo = kwargs.get("normalVideo", "")
        self.hdVideo = kwargs.get("hdVideo", "")
        self.audio = kwargs.get("audio", "")

    def randomId(self) -> str:
        return os.urandom(8).hex()

    async def download(self, audio: bool = False):
        # Check if file is exists
        if os.path.exists(f"downloads/facebook-{self.id}.mp4"):
            return f"downloads/facebook-{self.id}.mp4"

        # Create Folder if not exists
        if not os.path.isdir("downloads"):
            os.mkdir("downloads")
        
        targetUrl: str
        
        if audio is True:
            targetUrl = self.audio
        else:
            targetUrl = self.hdVideo

        async with aiohttp.ClientSession() as session:
            stream = await session.get(targetUrl)
            async with aiofiles.open(f"downloads/facebook-{self.id}.mp4", mode="wb") as file:
                await file.write(await stream.read())
                return f"downloads/facebook-{self.id}.mp4"
