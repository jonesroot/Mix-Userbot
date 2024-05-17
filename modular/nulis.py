################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV || EH KONTOL KALO PUNYA AKAL DIPAKE YA ANJING GAUSAH APUS² CREDIT MODAL NYOPAS LO BAJINGAN!!
"""
################################################################

import os

from PIL import Image, ImageDraw, ImageFont

from Mix.core import *
from Mix import *

__modles__ = "Nulis"
__help__ = get_cgr("help_nul")


def write_on_image(text, filename="output.jpg", line_spacing=50, enter_spacing=9):
    template = Image.open("Mix/core/bahan.jpg")
    draw = ImageDraw.Draw(template)
    font = ImageFont.truetype("Mix/core/font.ttf", 32)
    margin_left = 290
    margin_right = 250
    margin_top = 350
    margin_bottom = 100

    x = margin_left
    y = margin_top
    max_width = template.width - margin_left - margin_right
    max_height = template.height - margin_top - margin_bottom

    paragraphs = text.split("\n")

    for paragraph in paragraphs:
        lines = []
        words = paragraph.split(" ")
        line = []
        for word in words:
            line.append(word)
            w, h = draw.textsize(" ".join(line), font=font)
            if w > max_width:
                lines.append(" ".join(line[:-1]))
                line = [word]
        lines.append(" ".join(line))

        for line in lines:
            draw.text((x, y), line, font=font, fill="black")
            y += h + line_spacing
            if y + h > max_height:
                break

        y += enter_spacing - line_spacing
        if y > max_height:
            break

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
