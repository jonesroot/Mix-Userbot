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

from Mix import *

__modles__ = "RemoveBg"
__help__ = """
Removal Background
• Perintah: `{0}rmbg` [balas ke foto/gambar] atau `{0}rmbg` [tautan yang menuju ke sebuah gambar]
• Penjelasan: Untuk menghapus latar belakang foto tersebut.
"""


async def rem_bg(image_path):
    url = 'https://api.removal.ai/3.0/remove'
    headers = {
        'accept': 'application/json',
        'Rm-Token': '45FA9185-021A-E498-FF97-1A8DB4C76666',
    }
    files = {
        'image_file': (image_path, open(image_path, 'rb'), 'image/jpeg')
    }

    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        data = response.json()
        high_res_url = data.get('high_resolution')
        
        if high_res_url:
            high_res_image = requests.get(high_res_url)
            output_image_path = "rmbg.png"
            with open(output_image_path, 'wb') as f:
                f.write(high_res_image.content)
            return output_image_path
        else:
            raise ValueError("Gambar resolusi tinggi tidak ditemukan dalam respons.")
    else:
        response.raise_for_status()


@ky.ubot("rmbg|rbg", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    rep = m.reply_to_message
    pros = await m.reply(cgr("proses").format(em.proses))

    if rep and (rep.photo or rep.document and rep.document.mime_type.startswith("image/")):
        photo = rep.photo.file_id if rep.photo else rep.document.file_id
        photo_file_path = await c.download_media(photo)

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
        args = m.text.split(maxsplit=1)
        if len(args) > 1:
            image_url = args[1]
            output_image_path = "input_image.jpg"
            
            try:
                response = requests.get(image_url)
                if response.status_code == 200:
                    with open(output_image_path, 'wb') as f:
                        f.write(response.content)
                    hasil = await rem_bg(output_image_path)
                    if hasil:
                        await m.reply_document(hasil, reply_to_message_id=ReplyCheck(m))
                        os.remove(hasil)
                    else:
                        await m.reply_text(
                            "Maaf, terjadi kesalahan dalam menghapus latar belakang gambar.",
                            reply_to_message_id=ReplyCheck(m),
                        )
                else:
                    await m.reply_text(
                        f"Gagal mengunduh gambar dari URL: {image_url}",
                        reply_to_message_id=ReplyCheck(m),
                    )
            except Exception as e:
                await m.reply_text(
                    f"Terjadi kesalahan: {str(e)}", reply_to_message_id=ReplyCheck(m)
                )
            finally:
                if os.path.exists(output_image_path):
                    os.remove(output_image_path)
        else:
            await m.reply_text("Mohon balas ke gambar atau masukkan URL gambar.", reply_to_message_id=ReplyCheck(m))

    await pros.delete()
