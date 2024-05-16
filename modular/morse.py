################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
 
 EH KONTOL BAJINGAN !! KALO MO PAKE DIKODE PAKE AJA BANGSAT!! GAUSAH APUS KREDIT NGENTOT
"""
################################################################


from Mix import *

__modles__ = "Morse"
__help__ = """
 Morse

• Perintah: `{0}emorse` [teks/balas pesan teks]
• Penjelasan: Untuk meng-encode teks menjadi sandi morse.

• Perintah: `{0}dmorse` [teks/balas pesan teks]
• Penjelasan: Untuk men-decode sandi morse.
"""


"""
@ky.ubot("emorse|dmorse")
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    if m.reply_to_message:
        kimi = m.reply_to_message.text or m.reply_to_message.caption
    else:
        kimi = "".join(m.command[1:])
    pros = await m.reply(cgr("proses").format(em.proses))
    if m.command[0] == "emorse":

        uri = f"https://gsamuel-morse-code-v1.p.rapidapi.com/"
        payload = { "text": kimi }
        headers = {
          "content-type": "application/json",
          "X-RapidAPI-Key": "24d6a3913bmsh3561d6af783658fp1a8240jsneef57a49ff14",
          "X-RapidAPI-Host": "gsamuel-morse-code-v1.p.rapidapi.com"
        }
        pot = requests.post(url, json=payload, headers=headers)
        if pot.status_code == 200:
            res = pot.json().get("encoded")
            await m.reply(f"{em.sukses} Encode Morse\n\n`{res}`")
        elif pot.status_code == 422:
            await m.reply(
                f"{em.gagal} Mohon gunakan teks dan angka, tidak dapat meng-encode morse emoji!!"
            )
        else:
            await m.reply(f"Error: {pot.status_code} {pot.text}")
    elif m.command[0] == "dmorse":
        uri = f"https://api.safone.dev/morse/decode?text={kimi}"
        pot = requests.get(uri)
        if pot.status_code == 200:
            res = pot.json().get("decoded")
            await m.reply(f"{em.sukses} Decode Morse\n\n`{res}`")
        else:
            await m.reply(f"Error: {pot.status_code} {pot.text}")
    else:
        await m.reply(
            f"{em.gagal} Perintah yang anda gunakan salah!! Silahkan lihat bantuan."
        )
    await pros.delete()
    return
"""


import gtts
from gpytranslate import Translator

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
    if m.reply_to_message:
        text = m.reply_to_message.text
    else:
        text = m.text.split(maxsplit=1)[1] if len(m.text.split()) > 1 else None

    if not text:
        await m.reply(
            "Silakan balas pesan atau masukkan teks setelah perintah /emorse."
        )
        return

    morse_text = to_morse(text)
    audio_filename = "emorse_audio.mp3"
    text_to_speech(c, morse_text, audio_filename)
    await m.reply_audio(audio_filename, caption=morse_text)
    os.remove(audio_filename)


@ky.ubot("dmorse", sudo=True)
async def _(c: nlx, m):
    if m.reply_to_message:
        morse = m.reply_to_message.text
    else:
        morse = m.text.split(maxsplit=1)[1] if len(m.text.split()) > 1 else None

    if not morse:
        await m.reply(
            "Silakan balas pesan atau masukkan sandi Morse setelah perintah /dmorse."
        )
        return

    decoded_text = from_morse(morse)
    audio_filename = "dmorse_audio.mp3"
    text_to_speech(c, decoded_text, audio_filename)
    await m.reply_audio(audio_filename, caption=decoded_text)
    os.remove(audio_filename)
