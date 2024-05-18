import asyncio
import os
import re

from Mix import *

__modles__ = "Convert"
__help__ = get_cgr("help_konpert")


@ky.ubot("toimg", sudo=True)
async def _(c: nlx, message):
    em = Emojik()
    em.initialize()
    try:
        pros = await message.reply(cgr("proses").format(em.proses))
        file_io = await c.dln(message.reply_to_message)
        file_io.name = "sticker.png"
        await c.send_photo(
            message.chat.id,
            file_io,
            caption=cgr("konpert_5").format(em.sukses, c.me.mention),
            reply_to_message_id=message.id,
        )
        await pros.delete()
    except Exception as e:
        await pros.delete()
        return await c.send_message(
            message.chat.id,
            cgr("err").format(em.gagal, e),
            reply_to_message_id=message.id,
        )


@ky.ubot("tosticker|tostick", sudo=True)
async def _(c: nlx, message):
    em = Emojik()
    em.initialize()
    try:
        if not message.reply_to_message or not message.reply_to_message.photo:
            return await message.reply_text(cgr("konpert_1").format(em.gagal))
        sticker = await c.download_media(
            message.reply_to_message.photo.file_id,
            f"sticker_{message.from_user.id}.webp",
        )
        await message.reply_sticker(sticker)
        os.remove(sticker)
    except Exception as e:
        await message.reply(cgr("err").format(em.gagal, e))


@ky.ubot("togif", sudo=True)
async def _(c: nlx, message):
    em = Emojik()
    em.initialize()
    pros = await message.reply(cgr("proses").format(em.proses))
    if not message.reply_to_message.sticker:
        return await pros.edit(cgr("konpert_6").format(em.gagal))
    await pros.edit(cgr("konpert_2").format(em.proses))
    file = await c.download_media(
        message.reply_to_message,
        f"gift_{message.from_user.id}.mp4",
    )
    try:
        await c.send_animation(message.chat.id, file, reply_to_message_id=message.id)
        os.remove(file)
        await pros.delete()
        return
    except Exception as error:
        await pros.edit(cgr("err").format(em.gagal, star(error)))
        return


@ky.ubot("toaudio", sudo=True)
async def _(c: nlx, message):
    em = Emojik()
    em.initialize()
    replied = message.reply_to_message
    pros = await message.reply(cgr("proses").format(em.proses))
    if not replied:
        return await pros.edit(cgr("konpert_7").format(em.gagal))
    if replied.video:
        await pros.edit(cgr("konpert_2").format(em.proses))
        file = await c.download_media(
            message=replied,
            file_name=f"toaudio_{replied.id}",
        )
        out_file = f"{file}.mp3"
        try:
            await pros.edit(cgr("konpert_8").format(em.proses))
            cmd = f"ffmpeg -i {file} -q:a 0 -map a {out_file}"
            await c.run_cmd(cmd)
            await pros.edit(cgr("konpert_9").format(em.proses))
            await c.send_voice(
                message.chat.id,
                voice=out_file,
                caption=cgr("konpert_5").format(em.sukses, c.me.mention),
                reply_to_message_id=message.id,
            )
            os.remove(file)
            os.remove(out_file)
            return await pros.delete()
        except Exception as error:
            os.remove(file)
            os.remove(out_file)
            return await pros.edit(str(error))
    else:
        os.remove(file)
        os.remove(out_file)
        return await pros.edit(cgr("konpert_7").format(em.gagal))


get_efek = {
    "band_pass": '-filter_complex "bandpass=f=500:width_type=h:w=100"',
    "band_reject": '-filter_complex "bandreject=f=1000:width_type=h:w=100"',
    "bengek": '-filter_complex "rubberband=pitch=1.5"',
    "bitcrush": '-filter_complex "acrusher=level_in=10:level_out=16:bits=4:mode=log:aa=1"',
    "chorus": '-filter_complex "chorus=0.7:0.9:55:0.4:0.25:2"',
    "compressor": '-filter_complex "compand=points=-80/-105|-62/-80|-15.4/-15.4|0/-12|20/-7.6"',
    "delay": '-filter_complex "adelay=500|500"',
    "distortion": '-af "acompressor=threshold=-12dB:ratio=4:attack=20:release=100"',
    "echo": '-filter_complex "aecho=0.8:0.9:500|1000:0.2|0.1"',
    "fade_in": '-filter_complex "afade=t=in:st=0:d=5"',
    "fade_out": '-filter_complex "afade=t=out:st=150:d=5"',
    "fast": "-filter_complex \"afftfilt=real='hypot(re,im)*cos((random(0)*2-1)*2*3.14)':imag='hypot(re,im)*sin((random(1)*2-1)*2*3.14)':win_size=128:overlap=0.8\"",
    "flanger": '-filter_complex "flanger=delay=0.002:depth=0.7"',
    "high_pass": '-filter_complex "highpass=f=200"',
    "high_pitch": '-filter_complex "atempo=1.1"',
    "jedug": '-filter_complex "acrusher=level_in=8:level_out=18:bits=8:mode=log:aa=1"',
    "low_pass": '-filter_complex "lowpass=f=1000"',
    "low_pitch": '-filter_complex "rubberband=pitch=0.7"',
    "megaphone": "-filter_complex \"afftfilt=real='hypot(re,im)*cos((random(0)*2-1)*2*3.14)':imag='hypot(re,im)*sin((random(1)*2-1)*2*3.14)':win_size=512:overlap=0.75\"",
    "phaser": '-filter_complex "aphaser=type=t"',
    "phaser2": '-filter_complex "aphaser=type=t:decay=0.5"',
    "pitch_down": '-filter_complex "atempo=0.5"',
    "pitch_up": '-filter_complex "atempo=2.0"',
    "radio": '-af "equalizer=f=3000:width_type=h:width=200:g=-10"',
    "reverb": '-filter_complex "aecho=0.8:0.9:500|1000:0.2|0.1"',
    "reverse": '-filter_complex "areverse"',
    "reverse_echo": '-filter_complex "aecho=0.8:0.88:1000:0.5"',
    "robot": "-filter_complex \"afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=512:overlap=0.75\"",
    "stereo_widen": '-af "pan=stereo|c0<c0+0.5*c1|c1<c0+0.5*c1"',
    "telephone": '-filter_complex "[0:a][0:a]amix=inputs=2:duration=first:dropout_transition=2,volume=1.5[a]" -map "[a]"',
    "tremolo": '-filter_complex "tremolo=f=5:d=0.5"',
    "vibrato": '-filter_complex "vibrato=f=10"',
}


list_efek = [
    "band_pass",
    "band_reject",
    "bengek",
    "bitcrush",
    "chorus",
    "compressor",
    "delay",
    "distortion",
    "echo",
    "fade_in",
    "fade_out",
    "fast",
    "flanger",
    "high_pass",
    "high_pitch",
    "jedug",
    "low_pass",
    "low_pitch",
    "megaphone",
    "phaser",
    "phaser2",
    "pitch_down",
    "pitch_up",
    "radio",
    "reverb",
    "reverse",
    "reverse_echo",
    "robot",
    "stereo_widen",
    "telephone",
    "tremolo",
    "vibrato",
]


list_efek_deskripsi = {
    "band_pass": "Hanya melewati frekuensi tertentu.",
    "band_reject": "Memblokir frekuensi tertentu.",
    "bengek": "Suara seperti berbicara dengan mulut penuh.",
    "bitcrush": "Resolusi sampel berkurang.",
    "chorus": "Efek suara banyak.",
    "compressor": "Mengurangi dinamika suara.",
    "delay": "Mengulang suara dengan jeda waktu.",
    "distortion": "Suara terdistorsi.",
    "echo": "Efek gema atau pantulan suara.",
    "fade_in": "Meningkatkan volume bertahap.",
    "fade_out": "Mengurangi volume bertahap.",
    "fast": "Mempercepat suara.",
    "flanger": "Efek modulasi pada suara.",
    "high_pass": "Menghilangkan frekuensi rendah.",
    "high_pitch": "Meningkatkan pitch suara.",
    "jedug": "Efek kedapatan suara.",
    "low_pass": "Menghilangkan frekuensi tinggi.",
    "low_pitch": "Menurunkan pitch suara.",
    "megaphone": "Suara seperti megaphone.",
    "phaser": "Efek suara bergetar.",
    "phaser2": "Variasi efek phaser.",
    "pitch_down": "Menurunkan nada suara.",
    "pitch_up": "Meningkatkan nada suara.",
    "radio": "Suara seperti radio.",
    "reverb": "Efek suara gema.",
    "reverse": "Memutar suara ke belakang.",
    "reverse_echo": "Pantulan suara terbalik.",
    "robot": "Suara seperti robot.",
    "stereo_widen": "Suara terdengar lebih luas.",
    "telephone": "Suara seperti telepon.",
    "tremolo": "Efek getaran pada suara.",
    "vibrato": "Efek getaran kecil.",
}


@ky.ubot("list-efek|efeks|list-effects", sudo=True)
async def _(c: nlx, message):
    em = Emojik()
    em.initialize()

    daftar_efek = "\n".join(
        [
            f"• `{epek}` - {list_efek_deskripsi.get(epek, 'Coba Sendiri')}"
            for epek in list_efek
        ]
    )

    await message.reply(cgr("konpert_10").format(em.sukses, daftar_efek))


@ky.ubot("efek|effect|voifek", sudo=True)
async def _(c: nlx, message):
    em = Emojik()
    em.initialize()
    args = c.get_arg(message)
    reply = message.reply_to_message
    prefix = await c.get_prefix(c.me.id)
    pros = await message.reply(cgr("konpert_11").format(em.proses, args))

    try:
        if reply and args in get_efek:
            converted_file = "converted_audio.mp3"
            indir = f"audio_{message.chat.id}.mp3"
            if os.path.exists(converted_file):
                os.remove(converted_file)
            if os.path.exists(indir):
                os.remove(indir)
            indir = await c.download_media(reply, file_name=indir)
            process = await asyncio.create_subprocess_shell(
                f"ffmpeg -i '{indir}' {get_efek[args]} {converted_file}"
            )
            await process.communicate()
            if os.path.exists(converted_file):
                await message.reply_voice(
                    open(converted_file, "rb"),
                    caption=cgr("konpert_12").format(em.sukses, args),
                )
                await pros.delete()
                if os.path.exists(converted_file):
                    os.remove(converted_file)
                if os.path.exists(indir):
                    os.remove(indir)
            else:
                await pros.edit(cgr("konpert_14").format(em.gagal))

        else:
            await pros.edit(
                cgr("konpert_13").format(em.gagal, next((p) for p in prefix))
            )

    except Exception as e:
        await pros.edit(cgr("err").format(em.gagal, e))


async def stt_cmd(c, m, upload_url, pros):
    em = Emojik()
    em.initialize()
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(upload_url)
    if transcript.text:
        await pros.edit(
            cgr("konpert_21").format(em.sukses, c.me.mention, transcript.text)
        )
        os.remove(upload_url)
    else:
        await pros.edit(cgr("konpert_22").format(em.gagal))
        os.remove(upload_url)


@ky.ubot("stt", sudo=True)
async def transcribe_audio(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))

    if m.reply_to_message and (m.reply_to_message.audio or m.reply_to_message.voice):
        if m.reply_to_message.audio:
            upload_url = await c.download_media(
                m.reply_to_message.audio.file_id, file_name="stt.mp3"
            )
        elif m.reply_to_message.voice:
            upload_url = await c.download_media(
                m.reply_to_message.voice.file_id, file_name="stt.ogg"
            )
        await stt_cmd(c, m, upload_url, pros)
    elif m.command and len(m.command) > 1:
        url = m.command[1]
        if re.match(r"^https?://.*\.(mp3|ogg)$", url):
            await stt_cmd(c, m, url, pros)
        else:
            await pros.edit(
                f"{em.gagal} URL yang diberikan bukan URL audio yang valid."
            )
    else:
        await pros.edit(
            f"{em.gagal} Mohon balas pesan dengan audio atau berikan URL audio yang valid untuk mentranskripsinya."
        )


from pyrogram import enums
from pyrogram.raw.functions.messages import DeleteHistory


async def send_photo_and_get_anime(photo_path, c):
    bod = "mix_22225_bot"
    try:
        await c.unblock_user("mix_22225_bot")
        jir = await c.resolve_peer("mix_22225_bot")
        await c.send_message(bod, "/start")
        await c.send_photo(bod, photo_path)
        await asyncio.sleep(7)
        try:
            async for jmbt in nlx.search_messages(
                bod, filter=enums.MessagesFilter.PHOTO, limit=1
            ):
                if jmbt.photo:
                    file_path = await c.download_media(jmbt.photo.file_id)
                    await c.invoke(DeleteHistory(peer=jir, max_id=0, revoke=True))
                    return file_path
        except Exception as e:
            print("Error:", str(e))
            return None
    except Exception as e:
        print("Error:", str(e))
        return None


@ky.ubot("toanime", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    rep = m.reply_to_message
    pros = await m.reply(cgr("proses").format(em.proses))

    if rep.photo:
        photo = rep.photo.file_id
        photo_file_path = await c.download_media(photo)

        try:
            anime_photo_path = await send_photo_and_get_anime(photo_file_path, c)
            if anime_photo_path:
                await c.send_photo(
                    m.chat.id,
                    anime_photo_path,
                    caption=f"{em.sukses} Berhasil!",
                    reply_to_message_id=ReplyCheck(m),
                )
                os.remove(anime_photo_path)
        except Exception as e:
            await m.reply_text(
                f"Terjadi kesalahan: {str(e)}", reply_to_message_id=ReplyCheck(m)
            )
        finally:
            if os.path.exists(photo_file_path):
                os.remove(photo_file_path)
    else:
        await m.reply_text(
            "Mohon balas ke gambar untuk mengonversinya ke gaya anime.",
            reply_to_message_id=ReplyCheck(m),
        )

    await pros.delete()
