<p align=center>
    <img src="https://upload.wikimedia.org/wikipedia/fi/thumb/2/2a/Veolia-logo.svg/250px-Veolia-logo.svg.png"/>
</p>

<p>
    <a href="https://pypi.org/project/veolia-api/"><img src="https://img.shields.io/pypi/v/veolia-api.svg"/></a>
    <a href="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white"><img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white" /></a>
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" /></a>
    <a href="https://github.com/Jezza34000/veolia-api/actions"><img src="https://github.com/Jezza34000/veolia-api/workflows/CI/badge.svg"/></a>
</p>

Python wrapper for using Veolia API : https://www.eau.veolia.fr/

## Installation

```bash
pip install veolia-api
```

## Usage

```python
"""Example of usage of the Veolia API"""

import asyncio
import logging

from veolia_api.veolia_api import ConsumptionType, VeoliaAPI

logging.basicConfig(level=logging.DEBUG)


async def main() -> None:

    api = VeoliaAPI("username", "password")
    await api.login()

    try:
        ### Get the consumption data for the year 2024
        data = await api.get_consumption_data(ConsumptionType.YEARLY, 2024)
        print(data)

        ### Get the consumption data for Octobre 2024
        data = await api.get_consumption_data(ConsumptionType.MONTHLY, 2024, 10)
        print(data)

        #### Get the alerts set for the account
        data = await api.get_alerts()
        print(data)

        ### Set the alerts for the account
        alerts = AlertSettings(
            daily_enabled=True,
            daily_threshold=550,
            daily_contact_email=True,
            daily_contact_sms=True,
            monthly_enabled=True,
            monthly_threshold=8,
            monthly_contact_email=True,
            monthly_contact_sms=True
        )
        data = await api.set_alerts(alerts)
        print(data)
        
    finally:
        await api.close()


if __name__ == "__main__":
    asyncio.run(main())

```
