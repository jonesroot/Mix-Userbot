################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV || EH KONTOL KALO PUNYA AKAL DIPAKE YA ANJING GAUSAH APUS² CREDIT MODAL NYOPAS LO BAJINGAN!!
"""
################################################################

import os

from removebg import RemoveBg

from Mix import *

__modles__ = "RemoveBg"
__help__ = """
Removal Background
• Perintah: `{0}rmbg` [balas ke foto/gambar] atau `{0}rmbg` [tautan yang menuju ke sebuah gambar]
• Penjelasan: Untuk menghapus latar belakang foto tersebut.
"""


async def rem_bg(gambar):
    rmbeg = RemoveBg("KxZHg1ZjxsiU5TLca4kjWptR", "error.log")
    hasil = rmbeg.remove_background_from_img_file("gambar")
    return hasil


@ky.ubot("rmbg|rbg", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    rep = m.reply_to_message
    pros = await m.reply(cgr("proses").format(em.proses))

    if rep and (
        rep.photo or rep.document and rep.document.mime_type.startswith("image/")
    ):
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
                    with open(output_image_path, "wb") as f:
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
            await m.reply_text(
                "Mohon balas ke gambar atau masukkan URL gambar.",
                reply_to_message_id=ReplyCheck(m),
            )

    await pros.delete()
