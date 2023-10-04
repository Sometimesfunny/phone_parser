# Phone Parser

## Usage

```python
import asyncio
from phone_parser import PhoneParser, HTTPError

async def main():
    url = "https://example.com/"
    parser = PhoneParser()
    try:
        phone_numbers = await get_phone_numbers(url)
        print(phone_numbers)
    except HTTPError:
        print("Error occurred")

asyncio.run(main())
```

## Tests

```bash
pytest
```

Tests might not be relevant if site contents changed
