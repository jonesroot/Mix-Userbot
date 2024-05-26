################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################

import os

import gtts
from gpytranslate import Translator

from Mix import *
from Mix.core.parser import kode_bahasa

__modles__ = "Translate"
__help__ = get_cgr("help_transmart")


@ky.ubot("tts", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    if m.reply_to_message:
        bhs = c._translate[c.me.id]["negara"]
        kata = m.reply_to_message.text or m.reply_to_message.caption
    else:
        if len(m.command) < 2:
            await pros.edit(cgr("tr_1").format(em.gagal, m.command))
        else:
            bhs = c._translate[c.me.id]["negara"]
            kata = m.text.split(None, 1)[1]
    gts = gtts.gTTS(kata, lang=bhs)
    gts.save("trs.oog")
    rep = m.reply_to_message or m
    try:
        await c.send_voice(
            chat_id=m.chat.id,
            voice="trs.oog",
            reply_to_message_id=rep.id,
        )
        await pros.delete()
        os.remove("trs.oog")
        return
    except Exception as er:
        await pros.edit(cgr("err").format(em.gagal, er))
        return
    except FileNotFoundError:
        pass


@ky.ubot("tr", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    trans = Translator()
    rep = m.reply_to_message
    pros = await m.reply(cgr("proses").format(em.proses))
    if rep and (rep.text or rep.caption):
        txt = rep.text or rep.caption
    elif len(m.text.split(None, 1)) > 1:
        txt = m.text.split(None, 1)[1]
    else:
        txt = None

    if not txt:
        await pros.edit(cgr("tr_1").format(em.gagal, m.text))
        return

    try:
        src = await trans.detect(txt)
        bhs = c._translate[c.me.id]["negara"]
        trsl = await trans(txt, sourcelang=src, targetlang=bhs)
        reply = cgr("tr_2").format(em.sukses, trsl.text)
        await pros.delete()
        await c.send_message(
            m.chat.id, reply, reply_to_message_id=(rep.id if rep else m.id)
        )
    except Exception as e:
        await pros.edit(cgr("err").format(em.gagal, str(e)))


@ky.ubot("lang", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    try:
        bhs_list = "\n".join(
            f"- **{lang}**: `{code}`" for lang, code in kode_bahasa.items()
        )
        await m.reply(cgr("tr_3").format(em.sukses, bhs_list))
        return
    except Exception as e:
        await m.reply(cgr("err").format(em.gagal, e))
        return


@ky.ubot("setlang", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    if len(m.command) < 2:
        await pros.edit(cgr("tr_4").format(em.gagal, m.text, get_prefix))
        return
    for lang, code in kode_bahasa.items():
        kd = m.text.split(None, 1)[1]
        if kd.lower() == code.lower():
            c._translate[c.me.id] = {"negara": kd}
            await pros.edit(cgr("tr_5").format(em.sukses, kd, lang))
            return
    await pros.edit(cgr("tr_6").format(em.gagal, m))
    return
