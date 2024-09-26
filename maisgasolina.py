# ------------------------------------------------------------------------
#  Created by Martin J. Laubach on 2024-09-24
#  Copyright © 2024 Martin J. Laubach. All rights reserved.
# ------------------------------------------------------------------------
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
# ------------------------------------------------------------------------
"""Fetch fuel price from maisgaolina for use in home assistant"""

from __future__ import annotations

# ------------------------------------------------------------------------
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
def decode_maisgasolina(ciphertext: str) -> str:
    """Decodes values like static.maisgasolina.com/script.18.js"""

    plaintext: list[str] = []

    if not ciphertext:
        return ciphertext

    ciphertext = ciphertext[2:]

    idx = 0
    while True:
        c1 = alphabet.index(ciphertext[idx])
        c2 = alphabet.index(ciphertext[idx + 1])
        c3 = alphabet.index(ciphertext[idx + 2])
        c4 = alphabet.index(ciphertext[idx + 3])
        idx += 4

        l = (c1 << 18) | (c2 << 12) | (c3 << 6) | c4

        o1 = (l >> 16) & 255
        o2 = (l >> 8) & 255
        o3 = l & 255
        if c3 == 64:
            plaintext.append(chr(o1))
        elif c4 == 64:
            plaintext.extend((chr(o1), chr(o2)))
        else:
            plaintext.extend((chr(o1), chr(o2), chr(o3)))

        if idx >= len(ciphertext):
            break

    return ''.join(plaintext)[2:]

# assert decode_maisgasolina("P0MjQxLjQ5NQ==") == '1.495'
# assert decode_maisgasolina("pMMjcxLjM5NQ==") == '1.395'
# assert decode_maisgasolina("ELMTcxLjU2OQ==") == '1.569'
# assert decode_maisgasolina("ydMjQxLjYzOQ==") == '1.639'
# assert decode_maisgasolina("h7MTYxLjQ0NQ==") == '1.445'

import argparse
import json
import requests
import sys
from bs4 import BeautifulSoup as bs
import soupsieve as sv

URL = 'https://www.maisgasolina.com/posto/{}/'

def main() -> int:
    parser = argparse.ArgumentParser(
        description='Fetch the current price of fuel from MaisGasolina',
    )

    parser.add_argument('-s', '--station', action='store', type=int, required=True)      # option that takes a value
    parser.add_argument('-p', '--product', action='store', default='diesel', choices=('diesel', 'sc95', 'sc98', 'dplus'))      # option that takes a value
    args = parser.parse_args()
    assert args.station is not None, 'Station number is required'

    url = URL.format(args.station)

    r = requests.get(url)
    r.raise_for_status()

    error = False
    price: str = ''
    result = { 'status': 'OK', 'station': args.station, 'product': args.product, 'source': url }
    try:
        soup = bs(r.text, 'html.parser')
        selector = ['#station', '.precos', f'.{args.product}', '~', 'div', 'div.encoded']

        station_name = soup.select_one('#station .name [itemprop=name]').text.strip()  # pyright: ignore[reportOptionalMemberAccess]
        result['station_name'] = station_name

        price_encoded = soup.select_one(' '.join(selector)).attrs['data-price']  # pyright: ignore[reportOptionalMemberAccess]
        price = decode_maisgasolina(price_encoded)
        result['price'] = price

        updated = soup.select_one('#station .priceInfo .actualizacao')
        updated_info = list(updated.children)[-1]  # pyright: ignore[reportOptionalMemberAccess]
        result['updated'] = updated_info.text.strip()

    except (AttributeError, KeyError, IndexError) as ex:
        print(f"Could not extract requested data: {ex}", file=sys.stderr)
        result['status'] = 'ERROR'
        result['error'] = str(ex)
        error = True

    print(json.dumps(result))

    return 0 if not error else 4


if __name__ == "__main__":
    raise SystemExit(main())