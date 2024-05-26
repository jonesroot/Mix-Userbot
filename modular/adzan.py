import json

import requests

from Mix import *

__modles__ = "Adzan"
__help__ = get_cgr("help_ajan")


@ky.ubot("adzan", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    lok = c.get_text(m)
    pros = await m.reply(cgr("proses").format(em.proses))
    if not lok:
        await pros.edit(cgr("jan_1").format(em.gagal)
        return
    url = f"http://muslimsalat.com/{lok}.json?key=bd099c5825cbedb9aa934e255a81a5fc"
    req = requests.get(url)
    if req.status_code != 200:
        await pros.edit(cgr("jan_2").format(em.gagal, lok)
        return
    result = json.loads(req.text)
    txt = cgr("jan_3").format(lok)
    txt += cgr("jan_4").format(result['items'][0]['date_for']),
    txt += cgr("jan_5").format(result['query'], result['country']),
    txt += cgr("jan_6").format(result['items'][0]['shurooq']),
    txt += cgr("jan_7").format(result['items'][0]['fajr']),
    txt += cgr("jan_8").format(result['items'][0]['dhuhr']),
    txt += cgr("jqn_9").format(result['items'][0]['asr']),
    txt += cgr("jan_10").format(result['items'][0]['maghrib']),
    txt += cgr("jan_11").format(result['items'][0]['isha']),
    await m.reply(txt)
    await pros.delete()
    return
