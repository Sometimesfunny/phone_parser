from typing import Optional
from aiohttp import ClientSession
import re

import aiohttp
from errors import HTTPError


class PhoneParser:
    def __init__(
        self, headers: Optional[dict] = None, regexp: Optional[str] = None
    ) -> None:
        if not headers:
            # Using Mobile user agent to get covered phone numbers
            self.headers = {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
            }
        else:
            self.headers = headers
        if not regexp:
            # Regexp to filter russian phone numbers in text
            self.regexp = r"[\">]\+?[78]?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{1,4}[\s\-]?[0-9]{1,4}[\s\-]?[0-9]{1,4}[<\"]"
        else:
            self.regexp = regexp
        self.pattern: re.Pattern[str] = re.compile(self.regexp)

    async def _download_page(self, url: str) -> str:
        """Requests website and returns plain text

        Args:
            url (str): Url to access

        Raises:
            HTTPError: Url not found or connection refused/timed out

        Returns:
            str: Page text
        """
        async with ClientSession(headers=self.headers) as session:
            try:
                async with session.get(url) as response:
                    if response.ok:
                        return await response.text()
                    else:
                        raise HTTPError(f"Cannot access website {url}")
            except aiohttp.ClientError:
                raise HTTPError(f"Cannot access website {url}")

    def _match_all_phone_numbers(self, text: str) -> list[str]:
        """Find phone numbers in text using pattern

        Args:
            text (str): Where to search phone numbers

        Returns:
            list[str]: Raw phone numbers
        """
        match = self.pattern.findall(text)
        return match

    def _postprocess_phones_list(self, phones: list[str]) -> list[str]:
        """Converting raw phone numbers to fit 8KKKXXXXXXX format

        Args:
            phones (list[str]): Raw phone numbers

        Returns:
            list[str]: Formatted phone numbers
        """
        output_list: list[str] = []
        for phone in phones:
            phone = phone[1:-1]
            res, _ = re.subn(r"[<>\"\(\)\s\+\-)]", "", phone)
            if len(res) == 7:
                res = "8495" + res
            elif len(res) == 10:
                res = "8" + res
            elif res.startswith("7"):
                res = "8" + res[1:]
            output_list.append(res)
        output_list = list(set(output_list))
        return output_list

    async def get_phone_numbers(self, url: str) -> list[str]:
        """Get phone number from webpage

        Args:
            url (str): Website url

        Raises:
            HTTPError: Url not found or connection refused/timed out

        Returns:
            list[str]: Phone numbers
        """
        text = await self._download_page(url)
        phones = self._match_all_phone_numbers(text)
        output = self._postprocess_phones_list(phones)
        print(output)
        return output
