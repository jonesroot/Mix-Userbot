################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV || EH KONTOL KALO PUNYA AKAL DIPAKE YA ANJING GAUSAH APUS² CREDIT MODAL NYOPAS LO BAJINGAN!!
"""
################################################################

import os

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
    try:
        with open(image_path, "rb") as img_file:
            input_image = Image.open(img_file)
            input_image = input_image.convert("RGBA")
            output_image = remove(input_image)
            output_image_path = "rmbg.png"
            output_image.save(output_image_path)
            input_image.close()
            return output_image_path
    except Exception as e:
        print(f"Error in rem_bg: {e}")
        return None


@ky.ubot("rmbg|rbg", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    rep = m.reply_to_message
    pros = await m.reply(cgr("proses").format(em.proses))

    if rep and rep.photo:
        photo = rep.photo.file_id
        photo_file_path = await c.download_media(photo)

        try:
            print(f"Downloaded photo to: {photo_file_path}")
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
