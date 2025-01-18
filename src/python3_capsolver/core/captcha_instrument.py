import os
import uuid
import base64
import shutil
from typing import Optional
from pathlib import Path

import aiohttp
import requests
from requests.adapters import HTTPAdapter

from .enum import SaveFormatsEnm
from .const import RETRIES, ASYNC_RETRIES
from .serializer import CaptchaResponseSer

__all__ = ("CaptchaInstrumentBase", "FileInstrument")


class FileInstrument:
    """
    This class contains usefull methods for async and async files processing to prepare them for solving

    Examples:
        >>> from python3_capsolver.core.captcha_instrument import FileInstrument
        >>> body = FileInstrument().file_processing(captcha_file="captcha_example.jpeg")
        /9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBUVxxxxx

        >>> from python3_capsolver.core.captcha_instrument import FileInstrument
        >>> body = FileInstrument().file_processing(captcha_link="https://some-url/file.jpeg")
        /9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBUVxxxxx

    Returns:
        String with decoded file data
    """

    @staticmethod
    def _local_file_captcha(captcha_file: str):
        """
        Method get local file, read it and prepare for sending to Captcha solving service
        """
        with open(captcha_file, "rb") as file:
            return file.read()

    @staticmethod
    def _file_const_saver(content: bytes, file_path: str, file_extension: str = "png") -> str:
        """
        Method create and save file in folder
        """
        Path(file_path).mkdir(parents=True, exist_ok=True)

        # generate image name
        file_name = f"file-{uuid.uuid4()}.{file_extension}"

        full_file_path = os.path.join(file_path, file_name)

        # save image to folder
        with open(full_file_path, "wb") as out_image:
            out_image.write(content)
        return full_file_path

    @staticmethod
    def _file_clean(full_file_path: str):
        shutil.rmtree(full_file_path, ignore_errors=True)

    @staticmethod
    def _url_read(url: str, **kwargs):
        """
        Method open links
        """
        # prepare session
        session = requests.Session()
        session.mount("http://", HTTPAdapter(max_retries=RETRIES))
        session.mount("https://", HTTPAdapter(max_retries=RETRIES))
        session.verify = False
        return session.get(url=url, **kwargs)

    @staticmethod
    async def _aio_url_read(url: str, **kwargs) -> bytes:
        """
        Async method read bytes from link
        """
        async with aiohttp.ClientSession() as session:
            async for attempt in ASYNC_RETRIES:
                with attempt:
                    async with session.get(url=url, **kwargs) as resp:
                        return await resp.content.read()

    def file_processing(
        self,
        captcha_link: Optional[str] = None,
        captcha_file: Optional[str] = None,
        captcha_base64: Optional[bytes] = None,
        save_format: SaveFormatsEnm = SaveFormatsEnm.TEMP,
        img_clearing: bool = True,
        file_path: str = "/tmp/",
        file_extension: str = "png",
        **kwargs,
    ) -> str:
        """
        Synchronous method for captcha image processing.
         - Method can read local file and return it's as base64 string.
         - Method can read file URL and return it's as base64 string.
         - Method can decode base64 bytes and return it's as base64 string.

        Args:
            captcha_link: URL link to file. Instrument will send GET request to it and read content
            captcha_file: Local file path. Instrument will read it
            captcha_base64: Readed file base64 data. Instrument will decode it in ``utf-8``
            save_format: This arg works only with ``captcha_link`` arg.
                            If ``SaveFormatsEnm.CONST`` is set - file will be loaded and saved locally.
            img_clearing: This arg works only with ``captcha_link`` arg.
                            If ``False`` - file wil not be removed downloading and saving locally.
            file_path: This arg works only with ``captcha_link`` and ``SaveFormatsEnm.CONST`` args.
                        In this param u can set locally path for downloaded file saving.
            file_extension: This arg works only with ``file_path`` args.
                        In this param u MUST set file format for saving.

        Examples:
            >>> from python3_capsolver.core.captcha_instrument import FileInstrument
            >>> body = FileInstrument().file_processing(captcha_file="captcha_example.jpeg")
            /9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBUVxxxxx

        Returns:
            String with decoded file data
        """
        # if a local file link is passed
        if captcha_file:
            return base64.b64encode(self._local_file_captcha(captcha_file=captcha_file)).decode("utf-8")
        # if the file is transferred in base64 encoding
        elif captcha_base64:
            return base64.b64encode(captcha_base64).decode("utf-8")
        # if a URL is passed
        elif captcha_link:
            content = self._url_read(url=captcha_link, **kwargs).content
            # according to the value of the passed parameter, select the function to save the image
            if save_format == SaveFormatsEnm.CONST.value:
                full_file_path = self._file_const_saver(content, file_path, file_extension=file_extension)
                if img_clearing:
                    self._file_clean(full_file_path=full_file_path)
            return base64.b64encode(content).decode("utf-8")
        else:
            raise ValueError("No valid captcha variant is set.")

    async def aio_file_processing(
        self,
        captcha_link: Optional[str] = None,
        captcha_file: Optional[str] = None,
        captcha_base64: Optional[bytes] = None,
        save_format: SaveFormatsEnm = SaveFormatsEnm.TEMP,
        img_clearing: bool = True,
        file_path: str = "/tmp/",
        file_extension: str = "png",
        **kwargs,
    ) -> str:
        """
        Asynchronous method for captcha image processing.
         - Method can read local file and return it's as base64 string.
         - Method can read file URL and return it's as base64 string.
         - Method can decode base64 bytes and return it's as base64 string.

        Args:
            captcha_link: URL link to file. Instrument will send GET request to it and read content
            captcha_file: Local file path. Instrument will read it
            captcha_base64: Readed file base64 data. Instrument will decode it in ``utf-8``
            save_format: This arg works only with ``captcha_link`` arg.
                            If ``SaveFormatsEnm.CONST`` is set - file will be loaded and saved locally.
            img_clearing: This arg works only with ``captcha_link`` arg.
                            If ``False`` - file wil not be removed downloading and saving locally.
            file_path: This arg works only with ``captcha_link`` and ``SaveFormatsEnm.CONST`` args.
                        In this param u can set locally path for downloaded file saving.
            file_extension: This arg works only with ``file_path`` args.
                        In this param u MUST set file format for saving.

        Examples:
            >>> import asyncio
            >>> from python3_capsolver.core.captcha_instrument import FileInstrument
            >>> body = asyncio.run(FileInstrument()
            ...                     .aio_file_processing(captcha_file="captcha_example.jpeg"))
            /9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBUVxxxxx

        Returns:
            String with decoded file data
        """
        # if a local file link is passed
        if captcha_file:
            return base64.b64encode(self._local_file_captcha(captcha_file=captcha_file)).decode("utf-8")
        # if the file is transferred in base64 encoding
        elif captcha_base64:
            return base64.b64encode(captcha_base64).decode("utf-8")
        # if a URL is passed
        elif captcha_link:
            content = await self._aio_url_read(url=captcha_link, **kwargs)
            # according to the value of the passed parameter, select the function to save the image
            if save_format == SaveFormatsEnm.CONST.value:
                full_file_path = self._file_const_saver(content, file_path, file_extension=file_extension)
                if img_clearing:
                    self._file_clean(full_file_path=full_file_path)
            return base64.b64encode(content).decode("utf-8")

        else:
            raise ValueError("No valid captcha variant is set.")


class CaptchaInstrumentBase:
    CAPTCHA_UNSOLVABLE = "ERROR_CAPTCHA_UNSOLVABLE"
    CAPTCHA_UNSOLVABLE_DESCRIPTION = "Captcha not recognized"
    """
    Basic Captcha solving class

    Args:
        api_key: Capsolver API key
        captcha_type: Captcha type name, like `ReCaptchaV2Task` and etc.
        sleep_time: The waiting time between requests to get the result of the Captcha
        request_url: API address for sending requests
    """

    def __init__(self):
        self.result = CaptchaResponseSer()
