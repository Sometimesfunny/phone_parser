"""TESTS MIGHT NOT BE RELEVANT IF SITES ARE DOWN OR PHONE NUMBERS CHANGED"""


from contextlib import nullcontext
import pytest

from errors import HTTPError
from phone_parser import PhoneParser


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url, context, result",
    [
        ("https://hands.ru/company/about/", nullcontext(), ["84951370720"]),
        ("https://repetitors.info/", nullcontext(), ["84955405676"]),
        ("https://www.cdek.ru/ru/", nullcontext(), ["84950090405"]),
        ("https://uniqom.ru/", nullcontext(), ["84232790279"]),
        ("", pytest.raises(HTTPError), None),
        ("https://error.error/", pytest.raises(HTTPError), None),
    ],
)
async def test_phone_parser(url, context, result):
    parser = PhoneParser()
    with context:
        output = await parser.get_phone_numbers(url)
        assert output == result
