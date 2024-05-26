import requests
from gpytranslate import Translator

from Mix import *

__modles__ = "Joke"
__help__ = get_cgr("help_joko")


async def kitatr(c, txt):
    cokk = Translator()
    bhs = c._translate[c.me.id]["negara"]
    src = await cokk.detect(txt)
    gasin = await cokk.translate(txt, sourcelang=src, targetlang=bhs)
    return gasin.text


async def get_joke():
    url = "https://jokes-always.p.rapidapi.com/joke"
    headers = {
        "X-RapidAPI-Key": "24d6a3913bmsh3561d6af783658fp1a8240jsneef57a49ff14",
        "X-RapidAPI-Host": "jokes-always.p.rapidapi.com",
    }
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        data = res.json().get("data")
        print(data)
        return data
    else:
        print(f"Error: {res.status_code} - {res.text}")
        return None


@ky.ubot("joke|jokes", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    joke = await get_joke()
    if joke:
        question, answer = joke.split("?", 1)
        question += "?"
        translated_question = await kitatr(c, question)
        translated_answer = await kitatr(c, answer.strip())
        response = cgr("joko_1").format(
            em.sukses, translated_question, translated_answer
        )
        await pros.edit(response)
    else:
        await pros.edit(cgr("joko_2").format(em.gagal))
