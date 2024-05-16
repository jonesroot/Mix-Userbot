# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

# from countryinfo import CountryInfo

import requests

from Mix import *

__modles__ = "Negara"
__help__ = """
 Kota
• Perintah: `{0}negara` [query]
• Penjelasan: Untuk mencari info tentang Negara tersebut.
"""


def get_colok(kontol):
    url = f"https://restcountries.com/v3.1/name/{kontol}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            info = {
                "name": data[0]["name"]["common"],
                "alt_spellings": ", ".join(data[0]["altSpellings"]),
                "area": data[0]["area"],
                "borders": (
                    ", ".join(data[0]["borders"])
                    if "borders" in data[0]
                    else "Tidak ada perbatasan"
                ),
                "calling_code": "+".join(
                    data[0]["idd"]["root"] + suffix
                    for suffix in data[0]["idd"]["suffixes"]
                ),
                "capital": ", ".join(data[0]["capital"]),
                "currencies": (
                    ", ".join(data[0]["currencies"].keys())
                    if "currencies" in data[0]
                    else "Tidak ada mata uang"
                ),
                "flag": data[0]["flags"]["png"],
                "demonym": data[0]["demonyms"]["eng"]["m"],
                "iso": data[0]["cca2"],
                "languages": ", ".join(data[0]["languages"].keys()),
                "population": data[0]["population"],
                "region": data[0]["region"],
                "subregion": data[0]["subregion"],
                "timezones": ", ".join(data[0]["timezones"]),
                "top_level_domain": ", ".join(data[0]["tld"]),
                "wikipedia": data[0]["flags"],
            }
            return info
            print(info)
    return None


@ky.ubot("negara", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    rep = c.get_text(m)
    country_info = get_colok(rep)
    if country_info:
        response_message = f"**Nama negara:-** `{country_info['name']}`\n"
        response_message += (
            f"**Ejaan Alternatif:-** `{country_info['alt_spellings']}`\n"
        )
        response_message += (
            f"**Wilayah Negara:-** `{country_info['area']}` kilometer persegi\n"
        )
        response_message += f"**Perbatasan:-** `{country_info['borders']}`\n"
        response_message += f"**Kode Panggilan:-** `{country_info['calling_code']}`\n"
        response_message += f"**Ibukota Negara:-** `{country_info['capital']}`\n"
        response_message += f"**Mata uang negara:-** `{country_info['currencies']}`\n"
        response_message += f"**Bendera Negara:-** [Link]({country_info['flag']})\n"
        response_message += f"**Demonim:-** `{country_info['demonym']}`\n"
        response_message += f"**Nama ISO:-** `{country_info['iso']}`\n"
        response_message += f"**Bahasa:-** `{country_info['languages']}`\n"
        response_message += f"**Populasi:-** `{country_info['population']}`\n"
        response_message += f"**Wilayah:-** `{country_info['region']}`\n"
        response_message += f"**Sub Wilayah:-** `{country_info['subregion']}`\n"
        response_message += f"**Zona waktu:-** `{country_info['timezones']}`\n"
        response_message += (
            f"**Top Level Domain:-** `{country_info['top_level_domain']}`\n"
        )
        await pros.edit(response_message, disable_web_page_preview=True)
    else:
        await pros.edit("Maaf, informasi tidak ditemukan.")
