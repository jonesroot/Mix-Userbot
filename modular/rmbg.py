################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV || EH KONTOL KALO PUNYA AKAL DIPAKE YA ANJING GAUSAH APUS² CREDIT MODAL NYOPAS LO BAJINGAN!!
"""
################################################################

import io
import os

import requests
from PIL import Image
from rembg import remove

from Mix import *

__modles__ = "RemoveBg"
__help__ = """
Removal Background
• Perintah: `{0}rmbg` [balas ke foto] atau `{0}rbg` [balas ke foto]
• Penjelasan: Untuk menghapus latar belakang foto tersebut.
"""


async def rem_bg(image_path):
    with open(image_path, "rb") as img_file:
        input_image = Image.open(img_file)
        output_image = remove(input_image)
        output_image_path = "rmbg.png"
        output_image.save(output_image_path)
        return output_image_path


@ky.ubot("rmbg|rbg", sudo=True)
async def _(c, m):
    em = Emojik()
    em.initialize()
    rep = m.reply_to_message
    pros = await m.reply(cgr("proses").format(em.proses))

    if rep and rep.photo:
        photo = rep.photo[-1]
        photo_file_path = await rep.download_media(photo)

        try:
            hasil = await rem_bg(photo_file_path)
            if hasil:
                await m.reply_document(hasil, reply_to_message_id=ReplyCheck(m))
                os.remove(hasil)
            else:
                await m.reply_text(
                    "Maaf, terjadi kesalahan dalam menghapus latar belakang gambar.",
                    reply_to_message_id=ReplyCheck(m),
                )
        except Exception as e:
            await m.reply_text(
                f"Terjadi kesalahan: {str(e)}", reply_to_message_id=ReplyCheck(m)
            )
        finally:
            if os.path.exists(photo_file_path):
                os.remove(photo_file_path)
    else:
        await m.reply_text("Mohon balas ke gambar.", reply_to_message_id=ReplyCheck(m))

    await pros.delete()


def remove_background_from_url(image_url, output_path):
    response = requests.get(image_url)
    input_image = Image.open(io.BytesIO(response.content))
    output_image = remove(input_image)
    output_image.save(output_path)


# Contoh penggunaan
# image_url = "https://example.com/input.jpg"
# output_image_path = "output.png"
# remove_background_from_url(image_url, output_image_path)
