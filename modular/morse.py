################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
 
 EH KONTOL BAJINGAN !! KALO MO PAKE DIKODE PAKE AJA BANGSAT!! GAUSAH APUS KREDIT NGENTOT
"""
################################################################


import gtts

from Mix import *

__modles__ = "Morse"
__help__ = """
 Morse

• Perintah: `{0}emorse` [teks/balas pesan teks]
• Penjelasan: Untuk meng-encode teks menjadi sandi morse.

• Perintah: `{0}dmorse` [teks/balas pesan teks]
• Penjelasan: Untuk men-decode sandi morse.
"""


MORSE_CODE_DICT = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    ", ": "--..--",
    ".": ".-.-.-",
    "?": "..--..",
    "/": "-..-.",
    "-": "-....-",
    "(": "-.--.",
    ")": "-.--.-",
    " ": "/",
}


REVERSE_MORSE_CODE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}


def to_morse(text):
    return " ".join(MORSE_CODE_DICT.get(char.upper(), "") for char in text)


def from_morse(morse):
    return "".join(REVERSE_MORSE_CODE_DICT.get(char, "") for char in morse.split())


def text_to_speech(c, text, filename):
    bhs = c._translate[c.me.id]["negara"]
    gts = gtts.gTTS(text, lang=bhs)
    gts.save(filename)


@ky.ubot("emorse", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    if m.reply_to_message:
        text = m.reply_to_message.text
    else:
        text = m.text.split(maxsplit=1)[1] if len(m.text.split()) > 1 else None
    pros = await m.reply(cgr("proses").format(em.proses))
    if not text:
        await pros.edit(
            f"{em.gagal} Silakan balas pesan atau masukkan teks setelah perintah /emorse."
        )
        return

    morse_text = to_morse(text)
    audio_filename = "emorse.ogg"
    text_to_speech(c, morse_text, audio_filename)
    await m.reply_audio(audio_filename, caption=morse_text)
    await pros.delete()
    os.remove(audio_filename)


@ky.ubot("dmorse", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    if m.reply_to_message:
        morse = m.reply_to_message.text
    else:
        morse = m.text.split(maxsplit=1)[1] if len(m.text.split()) > 1 else None
    pros = await m.reply(cgr("proses").format(em.proses))
    if not morse:
        await pros.edit(
            f"{em.gagal} Silakan balas pesan atau masukkan sandi Morse setelah perintah /dmorse."
        )
        return
    decoded_text = from_morse(morse)
    audio_filename = "dmorse.ogg"
    text_to_speech(c, decoded_text, audio_filename)
    await m.reply_audio(audio_filename, caption=decoded_text)
    await pros.delete()
    os.remove(audio_filename)
