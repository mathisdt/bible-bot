#!/usr/bin/env python3
import locale
import logging
import sys

from mastodon import Mastodon

import verse
from config import Config

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s [%(levelname)s] %(message)s',
                    stream=sys.stdout)

config = Config("mastodon")

mastodon = Mastodon(
    access_token=config.access_token,
    api_base_url=config.api_base_url
)
NL = "\n"
mastodon.status_post(
    f'{f"{config.header}{NL}{NL}" if config.header else ""}{verse.get_message()}{f"{NL}{NL}{config.footer}" if config.footer else ""}')
