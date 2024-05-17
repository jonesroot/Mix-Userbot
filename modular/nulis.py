################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV || EH KONTOL KALO PUNYA AKAL DIPAKE YA ANJING GAUSAH APUS² CREDIT MODAL NYOPAS LO BAJINGAN!!
"""
################################################################

import os

from Mix import *

__modles__ = "Nulis"
__help__ = get_cgr("help_nul")


"""
async def nulis(text):
    meki = SafoneAPI()
    imgs = await meki.write(text)
    media = []

    if isinstance(imgs, BytesIO):
        img_paths = ["nulis.png"]
    else:
        img_paths = [f"nulis_{i+1}.png" for i in range(len(imgs))]

    if isinstance(imgs, BytesIO):
        imgs = [imgs]

    for i, img in enumerate(imgs):
        img_path = img_paths[i]
        with open(img_path, "wb") as file:
            file.write(img.getvalue())
        media.append(InputMediaPhoto(img_path))
    return media


@ky.ubot("nulis|write", sudo=True)
async def _(c, m):
    em = Emojik()
    em.initialize()
    rep = m.reply_to_message
    if rep:
        text = rep.text or rep.caption
    else:
        text = m.text.split(None, 1)[1]
    prose = await m.reply(cgr("proses").format(em.proses))
    try:
        meko = await nulis(text)
    except Exception as er:
        await m.reply(cgr("err").format(em.gagal, er))
        return
    await m.reply_media_group(meko, reply_to_message_id=ReplyCheck(m))
    await prose.delete()
    try:
        for mm in meko:
            os.remove(mm.media)
    except:
        pass
    return
"""


import os

from PIL import Image, ImageDraw, ImageFont

from Mix.core import *


def write_on_image(text, filename="output.jpg", line_spacing=50, enter_spacing=9):
    template = Image.open("Mix/core/bahan.jpg")
    draw = ImageDraw.Draw(template)
    font = ImageFont.truetype("Mix/core/font.ttf", 32)
    x, y = 285, 350
    paragraphs = text.split("\n")

    for paragraph in paragraphs:
        lines = []
        words = paragraph.split(" ")
        line = []
        for word in words:
            line.append(word)
            w, h = draw.textsize(" ".join(line), font=font)
            if w > template.width - 170:
                lines.append(" ".join(line[:-1]))
                line = [word]
        lines.append(" ".join(line))

        for line in lines:
            draw.text((x, y), line, font=font, fill="black")
            y += h + line_spacing
        y += enter_spacing - line_spacing
    template.save(filename)


@ky.ubot("nulis", sudo=True)
async def _(c: nlx, m):
    if m.reply_to_message:
        text = m.reply_to_message.text or m.reply_to_message.caption
    else:
        text = m.text.split(maxsplit=1)[1] if len(m.text.split()) > 1 else None

    if not text:
        await m.reply("Silakan balas pesan atau masukkan teks setelah perintah.")
        return

    output_filename = "output.jpg"
    write_on_image(text, output_filename)
    await m.reply_photo(photo=output_filename)
    os.remove(output_filename)
