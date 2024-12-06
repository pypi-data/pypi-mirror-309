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

from typing import List, Literal, Union


class Music:
    def __init__(self, **kwargs):
        self.id: int = kwargs.get("id", 0)
        self.title: str = kwargs.get("title", "")
        self.author: str = kwargs.get("author", "")
        self.album: str = kwargs.get("album", "")
        self.playUrl: List[str] = kwargs.get("playUrl", [])
        self.coverLarge: List[str] = kwargs.get("coverLarge", [])
        self.coverMedium: List[str] = kwargs.get("coverMedium", [])
        self.coverThumb: List[str] = kwargs.get("coverThumb", [])
        self.duration: int = kwargs.get("duration", 0)
        self.isCommerceMusic: bool = kwargs.get("isCommerceMusic", False)
        self.isOriginalSound: bool = kwargs.get("isOriginalSound", False)
        self.isAuthorArtist: bool = kwargs.get("isAuthorArtist", False)

    def parse(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "album": self.album,
            "playUrl": self.playUrl,
            "coverLarge": self.coverLarge,
            "coverMedium": self.coverMedium,
            "coverThumb": self.coverThumb,
            "duration": self.duration,
            "isCommerceMusic": self.isCommerceMusic,
            "isOriginalSound": self.isOriginalSound,
            "isAuthorArtist": self.isAuthorArtist
        }

class Statistics:
    def __init__(self, **kwargs):
        self.playCount: int = kwargs.get("playCount", 0)
        self.downloadCount: int = kwargs.get("downloadCount", 0)
        self.shareCount: int = kwargs.get("shareCount", 0)
        self.commentCount: int = kwargs.get("commentCount", 0)
        self.diggCount: int = kwargs.get("diggCount", 0)
        self.collectCount: int = kwargs.get("collectCount", 0)
        self.forwardCount: int = kwargs.get("forwardCount", 0)
        self.whatsappShareCount: int = kwargs.get("whatsappShareCount", 0)
        self.loseCount: int = kwargs.get("loseCount", 0)
        self.loseCommentCount: int = kwargs.get("loseCommentCount", 0)
        self.repostCount: int = kwargs.get("repostCount", 0)

    def parse(self):
        return {
            "playCount": self.playCount,
            "downloadCount": self.downloadCount,
            "shareCount": self.shareCount,
            "commentCount": self.commentCount,
            "diggCount": self.diggCount,
            "collectCount": self.collectCount,
            "forwardCount": self.forwardCount,
            "whatsappShareCount": self.whatsappShareCount,
            "loseCount": self.loseCount,
            "loseCommentCount": self.loseCommentCount,
            "repostCount": self.repostCount
        }


class Author:
    def __init__(self, **kwargs):
        self.id: int = kwargs.get("uid", 0)
        self.username: str = kwargs.get("unique_id", "")
        self.nickname: str = kwargs.get("nickname", "")
        self.signature: str = kwargs.get("signature", "")
        self.region: str = kwargs.get("region", "")
        self.avatarThumb: List[str] = kwargs.get("avatarThumb", [])
        self.avatarMedium: List[str] = kwargs.get("avatarMedium", [])
        self.url: str = kwargs.get("url", "")


    def parse(self):
        return {
            "id": self.id,
            "username": self.username,
            "nickname": self.nickname,
            "signature": self.signature,
            "region": self.region,
            "avatarThumb": self.avatarThumb,
            "avatarMedium": self.avatarMedium,
            "url": self.url
        }


class Video:
    def __init__(self, **kwargs):
        self.ratio: str = kwargs.get("ratio", "")
        self.duration: int = kwargs.get("duration", 0)
        self.playAddr: List[str] = kwargs.get("playAddr", [])
        self.downloadAddr: List[str] = kwargs.get("downloadAddr", [])
        self.cover: List[str] = kwargs.get("cover", [])
        self.dynamicCover: List[str] = kwargs.get("dynamicCover", [])
        self.originCover: List[str] = kwargs.get("originCover", [])


    def parse(self):
        return {
            "ratio": self.ratio,
            "duration": self.duration,
            "playAddr": self.playAddr,
            "downloadAddr": self.downloadAddr,
            "cover": self.cover,
            "dynamicCover": self.dynamicCover,
            "originCover": self.originCover
        }


class TikTok:
    def __init__(self, **kwargs):
        self.type: Literal["video", "image"] = kwargs.get("type", "video")
        self.id: str = kwargs.get("id", "")
        self.createTime: int = kwargs.get("createTime", 0)
        self.description: str = kwargs.get("description", "")
        self.author: Author = Author(**kwargs.get("author", {}))
        self.statistics: Statistics = Statistics(**kwargs.get("statistics", {}))
        self.hashTag: List[str] = kwargs.get("hashtag", [])
        self.isAds: bool = kwargs.get("isADS", False)
        self.cover: Union[List[str], None] = kwargs.get("cover", None)
        self.dynamicCover: Union[List[str], None] = kwargs.get("dynamicCover", None)
        self.originCover: Union[List[str], None] = kwargs.get("originCover", None)
        self.video: Video = Video(**kwargs.get("video", {}))
        self.images: Union[List[str], None] = kwargs.get("images", None)
        self.music: Music = Music(**kwargs.get("music", {}))

    async def download(self, audio: bool = False):
        # Check if file is exists
        if os.path.exists(f"downloads/tiktok-{self.id}.mp4"):
            return f"downloads/tiktok-{self.id}.mp4"

        # Create Folder if not exists
        if not os.path.isdir("downloads"):
            os.mkdir("downloads")
        
        targetUrl: str
        
        if audio is True:
            targetUrl = self.music.playUrl[-1]
        else:
            targetUrl = self.video.playAddr[-1]

        async with aiohttp.ClientSession() as session:
            stream = await session.get(targetUrl)
            async with aiofiles.open(f"downloads/tiktok-{self.id}.mp4", mode="wb") as file:
                await file.write(await stream.read())
                return f"downloads/tiktok-{self.id}.mp4"

    def parse(self):
        return {
            "type": self.type,
            "id": self.id,
            "createTime": self.createTime,
            "description": self.description,
            "author": self.author.parse(),
            "statistics": self.statistics.parse(),
            "hashTag": self.hashTag,
            "isAds": self.isAds,
            "cover": self.cover,
            "dynamicCover": self.dynamicCover,
            "originCover": self.originCover,
            "video": self.video.parse(),
            "images": self.images,
            "music": self.music.parse()
        }
