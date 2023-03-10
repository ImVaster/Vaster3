# ÂŠī¸ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# đ https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# đ https://www.gnu.org/licenses/agpl-3.0.html

import asyncio
import logging

from .. import loader, utils
from ..inline.types import BotInlineMessage, InlineCall

logger = logging.getLogger(__name__)


PRESETS = {
    "fun": [
        "https://mods.hikariatama.ru/aniquotes.py",
        "https://mods.hikariatama.ru/artai.py",
        "https://mods.hikariatama.ru/inline_ghoul.py",
        "https://mods.hikariatama.ru/lovemagic.py",
        "https://mods.hikariatama.ru/mindgame.py",
        "https://mods.hikariatama.ru/moonlove.py",
        "https://mods.hikariatama.ru/neko.py",
        "https://mods.hikariatama.ru/purr.py",
        "https://mods.hikariatama.ru/rpmod.py",
        "https://mods.hikariatama.ru/scrolller.py",
        "https://mods.hikariatama.ru/tictactoe.py",
        "https://mods.hikariatama.ru/trashguy.py",
        "https://mods.hikariatama.ru/truth_or_dare.py",
        "https://mods.hikariatama.ru/sticks.py",
        "https://mods.hikariatama.ru/premium_sticks.py",
        "https://heta.hikariatama.ru/MoriSummerz/ftg-mods/magictext.py",
        "https://heta.hikariatama.ru/HitaloSama/FTG-modules-repo/quotes.py",
        "https://heta.hikariatama.ru/HitaloSama/FTG-modules-repo/spam.py",
        "https://heta.hikariatama.ru/SkillsAngels/Modules/IrisLab.py",
        "https://heta.hikariatama.ru/Fl1yd/FTG-Modules/arts.py",
        "https://heta.hikariatama.ru/SkillsAngels/Modules/Complements.py",
        "https://heta.hikariatama.ru/Den4ikSuperOstryyPer4ik/Astro-modules/Compliments.py",
        "https://heta.hikariatama.ru/vsecoder/hikka_modules/mazemod.py",
    ],
    "chat": [
        "https://mods.hikariatama.ru/activists.py",
        "https://mods.hikariatama.ru/banstickers.py",
        "https://mods.hikariatama.ru/hikarichat.py",
        "https://mods.hikariatama.ru/inactive.py",
        "https://mods.hikariatama.ru/keyword.py",
        "https://mods.hikariatama.ru/tagall.py",
        "https://mods.hikariatama.ru/voicechat.py",
        "https://mods.hikariatama.ru/vtt.py",
        "https://heta.hikariatama.ru/SekaiYoneya/Friendly-telegram/BanMedia.py",
        "https://heta.hikariatama.ru/iamnalinor/FTG-modules/swmute.py",
        "https://heta.hikariatama.ru/GeekTG/FTG-Modules/filter.py",
    ],
    "service": [
        "https://mods.hikariatama.ru/account_switcher.py",
        "https://mods.hikariatama.ru/surl.py",
        "https://mods.hikariatama.ru/httpsc.py",
        "https://mods.hikariatama.ru/img2pdf.py",
        "https://mods.hikariatama.ru/latex.py",
        "https://mods.hikariatama.ru/pollplot.py",
        "https://mods.hikariatama.ru/sticks.py",
        "https://mods.hikariatama.ru/temp_chat.py",
        "https://mods.hikariatama.ru/vtt.py",
        "https://heta.hikariatama.ru/vsecoder/hikka_modules/accounttime.py",
        "https://heta.hikariatama.ru/vsecoder/hikka_modules/searx.py",
        "https://heta.hikariatama.ru/iamnalinor/FTG-modules/swmute.py",
    ],
    "downloaders": [
        "https://mods.hikariatama.ru/musicdl.py",
        "https://mods.hikariatama.ru/uploader.py",
        "https://mods.hikariatama.ru/porn.py",
        "https://mods.hikariatama.ru/web2file.py",
        "https://heta.hikariatama.ru/AmoreForever/amoremods/instsave.py",
        "https://heta.hikariatama.ru/CakesTwix/Hikka-Modules/tikcock.py",
        "https://heta.hikariatama.ru/CakesTwix/Hikka-Modules/InlineYouTube.py",
        "https://heta.hikariatama.ru/CakesTwix/Hikka-Modules/InlineSpotifyDownloader.py",
        "https://heta.hikariatama.ru/GeekTG/FTG-Modules/downloader.py",
        "https://heta.hikariatama.ru/Den4ikSuperOstryyPer4ik/Astro-modules/dl_yt_previews.py",
    ],
}


@loader.tds
class Presets(loader.Module):
    """Suggests new Hikka users a packs of modules to load"""

    strings = {
        "name": "Presets",
        "_fun_title": "đĒŠ Entertainment modules",
        "_fun_desc": "Fun modules â animations, spam, entertainment, etc.",
        "_chat_title": "đĨ Group Administration Helpers",
        "_chat_desc": (
            "The collection of tools which will help to moderate your group chat â"
            " filters, notes, voice recognition, etc."
        ),
        "_service_title": "âī¸ Useful modules",
        "_service_desc": (
            "Really useful modules â account management, link shortener, search engine,"
            " etc."
        ),
        "_downloaders_title": "đĨ Downloaders",
        "_downloaders_desc": (
            "The collection of tools which will help you download/upload files from/to"
            " different sources â YouTube, TikTok, Instagram, Spotify, VK Music, etc."
        ),
        "welcome": (
            "đ <b>Hi there! Tired of scrolling through endless modules in channels? Let"
            " me suggest you some pre-made collections. If you need to call this menu"
            " again, simply send /presets to this bot!</b>"
        ),
        "preset": (
            "<b>{}:</b>\nâšī¸ <i>{}</i>\n\nâ <b>Modules in this collection:</b>\n\n{}"
        ),
        "back": "đ Back",
        "install": "đĻ Install",
        "installing": (
            "<emoji document_id=5451732530048802485>âŗ</emoji> <b>Installing preset"
            "</b> <code>{}</code><b>...</b>"
        ),
        "installing_module": (
            "<emoji document_id=5451732530048802485>âŗ</emoji> <b>Installing preset"
            "</b> <code>{}</code> <b>({}/{} modules)...</b>\n\n<emoji"
            " document_id=5188377234380954537>đ</emoji> <i>Installing module"
            " {}...</i>"
        ),
        "installed": (
            "<emoji document_id=5436040291507247633>đ</emoji> <b>Preset"
            "</b> <code>{}</code> <b>installed!</b>"
        ),
        "already_installed": "â [Installed]",
    }

    strings_ru = {
        "_fun_title": "đĒŠ Đ Đ°ĐˇĐ˛ĐģĐĩĐēĐ°ŅĐĩĐģŅĐŊŅĐĩ ĐŧĐžĐ´ŅĐģĐ¸",
        "_fun_desc": "ĐĐ°ĐąĐ°Đ˛ĐŊŅĐĩ ĐŧĐžĐ´ŅĐģĐ¸ â Đ°ĐŊĐ¸ĐŧĐ°ŅĐ¸Đ¸, ŅĐŋĐ°Đŧ, Đ¸ĐŗŅŅ, Đ¸ Đ´Ņ.",
        "_chat_title": "đĨ ĐĐžĐ´ŅĐģĐ¸ Đ°Đ´ĐŧĐ¸ĐŊĐ¸ŅŅŅĐ¸ŅĐžĐ˛Đ°ĐŊĐ¸Ņ ŅĐ°ŅĐ°",
        "_chat_desc": (
            "ĐĐžĐģĐģĐĩĐēŅĐ¸Ņ ĐŧĐžĐ´ŅĐģĐĩĐš, ĐēĐžŅĐžŅŅĐĩ ĐŋĐžĐŧĐžĐŗŅŅ Đ˛Đ°Đŧ Đ°Đ´ĐŧĐ¸ĐŊĐ¸ŅŅŅĐ¸ŅĐžĐ˛Đ°ŅŅ ŅĐ°Ņ â ŅĐ¸ĐģŅŅŅŅ,"
            " ĐˇĐ°ĐŧĐĩŅĐēĐ¸, ŅĐ°ŅĐŋĐžĐˇĐŊĐ°Đ˛Đ°ĐŊĐ¸Đĩ ŅĐĩŅĐ¸, Đ¸ Đ´Ņ."
        ),
        "_service_title": "âī¸ ĐĐžĐģĐĩĐˇĐŊŅĐĩ ĐŧĐžĐ´ŅĐģĐ¸",
        "_service_desc": (
            "ĐĐĩĐšŅŅĐ˛Đ¸ŅĐĩĐģŅĐŊĐž ĐŋĐžĐģĐĩĐˇĐŊŅĐĩ ĐŧĐžĐ´ŅĐģĐ¸ â ŅĐŋŅĐ°Đ˛ĐģĐĩĐŊĐ¸Đĩ Đ°ĐēĐēĐ°ŅĐŊŅĐžĐŧ, ŅĐžĐēŅĐ°ŅĐ¸ŅĐĩĐģŅ ŅŅŅĐģĐžĐē,"
            " ĐŋĐžĐ¸ŅĐēĐžĐ˛Đ¸Đē, Đ¸ Đ´Ņ."
        ),
        "_downloaders_title": "đĨ ĐĐ°ĐŗŅŅĐˇŅĐ¸ĐēĐ¸",
        "_downloaders_desc": (
            "ĐĐžĐģĐģĐĩĐēŅĐ¸Ņ ĐŧĐžĐ´ŅĐģĐĩĐš, ĐēĐžŅĐžŅŅĐĩ ĐŋĐžĐŧĐžĐŗŅŅ Đ˛Đ°Đŧ ĐˇĐ°ĐŗŅŅĐļĐ°ŅŅ ŅĐ°ĐšĐģŅ Đ˛/Đ¸Đˇ ŅĐ°ĐˇĐģĐ¸ŅĐŊŅŅ(-Đĩ)"
            " Đ¸ŅŅĐžŅĐŊĐ¸ĐēĐžĐ˛(-Đ¸) â YouTube, TikTok, Instagram, Spotify, VK ĐŅĐˇŅĐēĐ°, Đ¸ Đ´Ņ."
        ),
        "welcome": (
            "đ <b>ĐŅĐ¸Đ˛ĐĩŅ! ĐŖŅŅĐ°Đģ ĐģĐ¸ŅŅĐ°ŅŅ ĐąĐĩŅŅĐ¸ŅĐģĐĩĐŊĐŊĐžĐĩ ĐēĐžĐģĐ¸ŅĐĩŅŅĐ˛Đž ĐŧĐžĐ´ŅĐģĐĩĐš Đ˛ ĐēĐ°ĐŊĐ°ĐģĐ°Ņ? ĐĐžĐŗŅ"
            " ĐŋŅĐĩĐ´ĐģĐžĐļĐ¸ŅŅ ŅĐĩĐąĐĩ ĐŊĐĩŅĐēĐžĐģŅĐēĐž ĐŗĐžŅĐžĐ˛ŅŅ ĐŊĐ°ĐąĐžŅĐžĐ˛. ĐŅĐģĐ¸ ŅĐĩĐąĐĩ ĐŋĐžĐŊĐ°Đ´ĐžĐąĐ¸ŅŅŅ ĐŋĐžĐ˛ŅĐžŅĐŊĐž"
            " Đ˛ŅĐˇĐ˛Đ°ŅŅ ŅŅĐž ĐŧĐĩĐŊŅ, ĐžŅĐŋŅĐ°Đ˛Ņ ĐŧĐŊĐĩ ĐēĐžĐŧĐ°ĐŊĐ´Ņ /presets</b>"
        ),
        "preset": "<b>{}:</b>\nâšī¸ <i>{}</i>\n\nâ <b>ĐĐžĐ´ŅĐģĐ¸ Đ˛ ŅŅĐžĐŧ ĐŊĐ°ĐąĐžŅĐĩ:</b>\n\n{}",
        "back": "đ ĐĐ°ĐˇĐ°Đ´",
        "install": "đĻ ĐŖŅŅĐ°ĐŊĐžĐ˛Đ¸ŅŅ",
        "installing": (
            "<emoji document_id=5451732530048802485>âŗ</emoji> <b>ĐŖŅŅĐ°ĐŊĐžĐ˛ĐēĐ° ĐŊĐ°ĐąĐžŅĐ°"
            " >/b><code>{}</code><b>...</b>"
        ),
        "installing_module": (
            "<emoji document_id=5451732530048802485>âŗ</emoji> <b>ĐŖŅŅĐ°ĐŊĐžĐ˛ĐēĐ° ĐŊĐ°ĐąĐžŅĐ°"
            "</b> <code>{}</code> <b>({}/{} ĐŧĐžĐ´ŅĐģĐĩĐš)...</b>\n\n<emoji"
            " document_id=5188377234380954537>đ</emoji> <i>ĐŖŅŅĐ°ĐŊĐžĐ˛ĐēĐ° ĐŧĐžĐ´ŅĐģŅ {}...</i>"
        ),
        "installed": (
            "<emoji document_id=5436040291507247633>đ</emoji> <b>ĐĐ°ĐąĐžŅ"
            "</b> <code>{}</code> <b>ŅŅŅĐ°ĐŊĐžĐ˛ĐģĐĩĐŊ!</b>"
        ),
        "already_installed": "â [ĐŖŅŅĐ°ĐŊĐžĐ˛ĐģĐĩĐŊ]",
    }

    strings_fr = {
        "_fun_title": "đĒŠ Modules de divertissement",
        "_fun_desc": "Modules amusants - animations, spam, jeux, etc.",
        "_chat_title": "đĨ Modules d'administration de chat",
        "_chat_desc": (
            "Collection de modules qui vous aideront Ã  administrer votre chat -"
            " filtres, notes, reconnaissance vocale, etc."
        ),
        "_service_title": "âī¸ Modules utiles",
        "_service_desc": (
            "Vraiment des modules utiles - gestion de compte, raccourcisseur d'URL,"
            " moteur de recherche, etc."
        ),
        "_downloaders_title": "đĨ TÃŠlÃŠchargeurs",
        "_downloaders_desc": (
            "Collection de modules qui vous aideront Ã  tÃŠlÃŠcharger des fichiers Ã "
            " partir de/vers diverses sources - YouTube, TikTok, Instagram, Spotify, VK"
            " Music, etc."
        ),
        "welcome": (
            "đ <b>Bonjour! Vous ÃĒtes fatiguÃŠ d'effectuer un balayage infini de modules"
            " dans les canaux? Je peux vous proposer quelques ensembles prÃĒts Ã "
            " l'emploi. Si vous avez besoin d'appeler Ã  nouveau ce menu, envoyez-moi la"
            " commande /presets</b>"
        ),
        "preset": (
            "<b>{}:</b>\nâšī¸ <i>{}</i>\n\nâ <b>Modules dans cet ensemble:</b>\n\n{}"
        ),
        "back": "đ Retour",
        "install": "đĻ Installer",
        "installing": (
            "<emoji document_id=5451732530048802485>âŗ</emoji> <b>Installation de"
            " l'ensemble >/b><code>{}</code><b>...</b>"
        ),
        "installing_module": (
            "<emoji document_id=5451732530048802485>âŗ</emoji> <b>Installation de"
            " l'ensemble</b> <code>{}</code> <b>({}/{} modules)...</b>\n\n<emoji"
            " document_id=5188377234380954537>đ</emoji> <i>Installation du module"
            " {}...</i>"
        ),
        "installed": (
            "<emoji document_id=5436040291507247633>đ</emoji> <b>L'ensemble"
            "</b> <code>{}</code> <b>est installÃŠ!</b>"
        ),
        "already_installed": "â [InstallÃŠ]",
    }

    strings_it = {
        "_fun_title": "đĒŠ Moduli divertenti",
        "_fun_desc": "Moduli divertenti, animazioni, spam, giochi e altro.",
        "_chat_title": "đĨ Moduli di amministrazione del gruppo",
        "_chat_desc": (
            "Una raccolta di moduli che ti aiuteranno ad amministrare il tuo gruppo,"
            " filtri, note, riconoscimento vocale e altro."
        ),
        "_service_title": "âī¸ Moduli utili",
        "_service_desc": (
            "Moduli veramente utili, gestione account, url shortener, motore di ricerca"
            " e altro."
        ),
        "_downloaders_title": "đĨ Downloaders",
        "_downloaders_desc": (
            "Una raccolta di moduli che ti aiuteranno a scaricare file da diversi"
            " fonti, YouTube, TikTok, Instagram, Spotify, VK Music e altro."
        ),
        "welcome": (
            "đ <b>Ciao! Ti annoiato a scorrere interminabili liste di moduli nei"
            " canali? Posso offrirti alcuni pacchetti predefiniti. Se vuoi richiamare"
            " questo menu, inviami il comando /presets</b>"
        ),
        "preset": (
            "<b>{}:</b>\nâšī¸ <i>{}</i>\n\nâ <b>Moduli in questo pacchetto:</b>\n\n{}"
        ),
        "back": "đ Indietro",
        "install": "đĻ Installa",
        "installing": (
            "<emoji document_id=5451732530048802485>âŗ</emoji> <b>Installazione"
            " pacchetto >/b><code>{}</code><b>...</b>"
        ),
        "installing_module": (
            "<emoji document_id=5451732530048802485>âŗ</emoji> <b>Installazione"
            " pacchetto</b> <code>{}</code> <b>({}/{} moduli)...</b>\n\n<emoji"
            " document_id=5188377234380954537>đ</emoji> <i>Installazione modulo"
            " {}...</i>"
        ),
        "installed": (
            "<emoji document_id=5436040291507247633>đ</emoji> <b>Pacchetto"
            "</b> <code>{}</code> <b>installato!</b>"
        ),
        "already_installed": "â [Installato]",
    }

    strings_de = {
        "_fun_title": "đĒŠ SpaÃmodule",
        "_fun_desc": "SpaÃmodule â Animationen, Spam, Spiele, und mehr.",
        "_chat_title": "đĨ Chat-Administration",
        "_chat_desc": (
            "Eine Sammlung von Modulen, die dir helfen, deinen Chat zu verwalten â"
            " Filter, Notizen, Spracherkennung, und mehr."
        ),
        "_service_title": "âī¸ NÃŧtzliche Module",
        "_service_desc": (
            "Wirklich nÃŧtzliche Module â Account-Management, Link-Shortener,"
            " Suchmaschine, und mehr."
        ),
        "_downloaders_title": "đĨ Download-Module",
        "_downloaders_desc": (
            "Eine Sammlung von Modulen, die dir helfen, Dateien aus/ins Internet zu"
            " laden â YouTube, TikTok, Instagram, Spotify, VK-Musik, und mehr."
        ),
        "welcome": (
            "đ <b>Hallo! Hast du genug von der ewigen Liste von Modulen in den KanÃ¤len?"
            " Ich kann dir ein paar fertige Sammlungen anbieten. Wenn du dieses MenÃŧ"
            " erneut aufrufen mÃļchtest, schicke mir /presets</b>"
        ),
        "preset": (
            "<b>{}:</b>\nâšī¸ <i>{}</i>\n\nâ <b>Module in dieser Sammlung:</b>\n\n{}"
        ),
        "back": "đ ZurÃŧck",
        "install": "đĻ Installieren",
        "installing": (
            "<emoji document_id=5451732530048802485>âŗ</emoji> <b>Installiere Sammlung"
            "</b> <code>{}</code><b>...</b>"
        ),
        "installing_module": (
            "<emoji document_id=5451732530048802485>âŗ</emoji> <b>Installiere Sammlung"
            "</b> <code>{}</code> <b>({}/{} Module)...</b>\n\n<emoji"
            " document_id=5188377234380954537>đ</emoji> <i>Installiere Modul"
            " {}...</i>"
        ),
        "installed": (
            "<emoji document_id=5436040291507247633>đ</emoji> <b>Sammlung"
            "</b> <code>{}</code> <b>installiert!</b>"
        ),
        "already_installed": "â [Installiert]",
    }

    strings_tr = {
        "_fun_title": "đĒŠ EÄlence ModÃŧlleri",
        "_fun_desc": "EÄlence modÃŧlleri â Animasyonlar, spam, oyunlar, vb.",
        "_chat_title": "đĨ Sohbet YÃļnetimi",
        "_chat_desc": (
            "Sohbetinizi yÃļnetmenize yardÄąmcÄą olacak bir modÃŧl koleksiyonu â"
            " filtreler, notlar, ses tanÄąma, vb."
        ),
        "_service_title": "âī¸ FaydalÄą ModÃŧller",
        "_service_desc": (
            "GerÃ§ekten faydalÄą modÃŧller â hesap yÃļnetimi, URL kÄąsaltma servisi,"
            " arama motoru, vb."
        ),
        "_downloaders_title": "đĨ Ä°ndirme ModÃŧlleri",
        "_downloaders_desc": (
            "Ä°nternetten dosyalarÄą indirmenize yardÄąmcÄą olacak bir modÃŧl koleksiyonu â"
            " YouTube, TikTok, Instagram, Spotify, VK MÃŧzik, vb."
        ),
        "welcome": (
            "đ <b>Merhaba! Kanallardaki sonsuz modÃŧl listesinden sÄąkÄąldÄąn mÄą? Sana"
            " birkaÃ§ hazÄąr koleksiyon sunabilirim. Bu menÃŧyÃŧ tekrar gÃļrÃŧntÃŧlemek"
            " istersen, /presets komutunu kullanabilirsin</b>"
        ),
        "preset": (
            "<b>{}:</b>\nâšī¸ <i>{}</i>\n\nâ <b>Bu koleksiyonda bulunan"
            " modÃŧller:</b>\n\n{}"
        ),
        "back": "đ Geri",
        "install": "đĻ Kur",
        "installing": (
            "<emoji document_id=5451732530048802485>âŗ</emoji> <b>Koleksiyon"
            "</b> <code>{}</code> <b>kuruluyor...</b>"
        ),
        "installing_module": (
            "<emoji document_id=5451732530048802485>âŗ</emoji> <b>Koleksiyon"
            "</b> <code>{}</code> <b>({}/{} modÃŧl) kuruluyor...</b>\n\n<emoji"
            " document_id=5188377234380954537>đ</emoji> <i>ModÃŧl {} kuruluyor...</i>"
        ),
        "installed": (
            "<emoji document_id=5436040291507247633>đ</emoji> <b>Koleksiyon"
            "</b> <code>{}</code> <b>kuruldu!</b>"
        ),
        "already_installed": "â [Zaten Kurulu]",
    }

    strings_uz = {
        "_fun_title": "đĒŠ Qiziqarli modullar",
        "_fun_desc": "Qiziqarli modullar â animatsiya, spam, o'yin, va boshqa.",
        "_chat_title": "đĨ Chat boshqarish modullar",
        "_chat_desc": (
            "Chat boshqarish modullar uchun yordam beruvchi koleksiya ham mavjud â"
            " filtrlar, qaydlar, tili aniqlash, va boshqa."
        ),
        "_service_title": "âī¸ Foydali modullar",
        "_service_desc": (
            "Foydali modullar â hisobni boshqarish, havola qisqartirish,"
            " qidiruv injini, va boshqa."
        ),
        "_downloaders_title": "đĨ Yuklab oluvchilar",
        "_downloaders_desc": (
            "Internetdan fayllarni yuklab olish uchun yordam beruvchi koleksiya ham"
            " mavjud â YouTube, TikTok, Instagram, Spotify, VK Music, va boshqa."
        ),
        "welcome": (
            "đ <b>Salom! Kanallarda son-sanoqsiz modullarni almashtirishdan"
            " charchadingizmi? Men sizga tayyor to'plamlarni taklif qila olaman. Agar"
            " siz ushbu menyuni yana chaqirib olishingiz kerak bo'lsa, /presets"
            " buyrug'ini menga yuboring</b>"
        ),
        "preset": (
            "<b>{}:</b>\nâšī¸ <i>{}</i>\n\nâ <b>Koleksiyada mavjud modullar:</b>\n\n{}"
        ),
        "back": "đ Orqaga",
        "install": "đĻ O'rnatish",
        "installing": (
            "<emoji document_id=5451732530048802485>âŗ</emoji> <b>Koleksiyani"
            "</b> <code>{}</code> <b>o'rnatilmoqda...</b>"
        ),
        "installing_module": (
            "<emoji document_id=5451732530048802485>âŗ</emoji> <b>Koleksiyani"
            "</b> <code>{}</code> <b>({}/{} modul) o'rnatilmoqda...</b>\n\n<emoji"
            " document_id=5188377234380954537>đ</emoji> <i>Modul {}"
            " o'rnatilmoqda...</i>"
        ),
        "installed": (
            "<emoji document_id=5436040291507247633>đ</emoji> <b>Koleksiyani"
            "</b> <code>{}</code> <b>o'rnatildi!</b>"
        ),
        "already_installed": "â [O'rnatilgan]",
    }

    strings_es = {
        "_fun_title": "đĒŠ MÃŗdulos divertidos",
        "_fun_desc": "MÃŗdulos divertidos â animaciones, spam, juegos, etc.",
        "_chat_title": "đĨ MÃŗdulos de administraciÃŗn de chat",
        "_chat_desc": (
            "TambiÃŠn hay ayuda para mÃŗdulos de administraciÃŗn de chat â filtros, "
            "registros, detecciÃŗn de idiomas, etc."
        ),
        "_service_title": "âī¸ MÃŗdulos Ãētiles",
        "_service_desc": (
            "MÃŗdulos Ãētiles â administraciÃŗn de cuentas, acortamiento de enlaces, "
            "motores de bÃēsqueda, etc."
        ),
        "_downloaders_title": "đĨ Descargadores",
        "_downloaders_desc": (
            "TambiÃŠn hay ayuda â YouTube, TikTok, Instagram, Spotify, etc."
        ),
        "welcome": (
            "đ <b>ÂĄHola! ÂŋTe sorprendiÃŗ ver muchos mÃŗdulos en el canal?"
            "TambiÃŠn hay algunas colecciones predefinidas. Para volver a abrir este"
            "menÃē, envÃ­e el comando /presets</b>"
        ),
        "preset": (
            "<b>{}:</b>\nâšī¸ <i>{}</i>\n\nâ <b>MÃŗdulos incluidos en la"
            " colecciÃŗn:</b>\n\n{}"
        ),
        "back": "đ AtrÃĄs",
        "install": "đĻ Instalar",
        "installing": (
            "<emoji document_id=5451732530048802485>âŗ</emoji> <b>Instalando la"
            " colecciÃŗn</b> <code>{}</code><b>...</b>"
        ),
        "installing_module": (
            "<emoji document_id=5451732530048802485>âŗ</emoji> <b>Instalando la"
            " colecciÃŗn</b> <code>{}</code> <b>({}/{} mÃŗdulos)...</b>\n\n<emoji"
            " document_id=5188377234380954537>đ</emoji> <i>Instalando el mÃŗdulo"
            " {}...</i>"
        ),
        "installed": (
            "<emoji document_id=5436040291507247633>đ</emoji> <b>ÂĄColecciÃŗn"
            "</b> <code>{}</code> <b>instalada!</b>"
        ),
        "already_installed": "â [ÂĄYa instalado!]",
    }

    strings_kk = {
        "_fun_title": "đĒŠ ŌŌąŅĐŧĐĩŅŅŅ ĐŧĐžĐ´ŅĐģĐ´ĐĩŅ",
        "_fun_desc": (
            "ŌŌąŅĐŧĐĩŅŅŅ ĐŧĐžĐ´ŅĐģĐ´ĐĩŅ â Đ°ĐŊĐ¸ĐŧĐ°ŅĐ¸ŅĐģĐ°Ņ, ĐļĐžĐŊĐ´Đ°Đš ĐļĐ°ĐˇŅ, ĐžĐšŅĐŊĐ´Đ°Ņ, ĐļĶĐŊĐĩ ĐąĐ°ŅŌĐ°ĐģĐ°Ņ."
        ),
        "_chat_title": "đĨ ĐĐĩĐģŅĐģŅĐēŅŅ ĐŧĐžĐ´ŅĐģĐ´ĐĩŅ",
        "_chat_desc": (
            "ĐĸŅŅĐēĐĩĐģĐŗŅĐģĐĩŅĐ´Ņ ŌĐ°ĐŧŅĐ°ĐŧĐ°ŅŅĐˇ ĐĩŅŅ, ĐĩŅĐēĐĩŅŅŅ, ŅĶŠĐšĐģĐĩŅŅĐ´Ņ ĐąŅĐģĐ´ŅŅŅ, ĐļĶĐŊĐĩ ĐąĐ°ŅŌĐ°ĐģĐ°ŅĐ´ŅŌŖ"
            " ŅŅŅĐēĐĩĐģĐŗŅĐģĐĩŅŅĐŊ ŌĐ°ĐŧŅĐ°ĐŧĐ°ŅŅĐˇ ĐĩŅŅ Ō¯ŅŅĐŊ ĐŧĐžĐ´ŅĐģĐ´ĐĩŅĐ´ŅŌŖ ŅŅĐˇŅĐŧŅ â ŅŅŅĐēĐĩĐģĐŗŅĐģĐĩŅ,"
            " ĐĩŅĐēĐĩŅŅŅĐģĐĩŅ, ŅĶŠĐšĐģĐĩŅŅĐ´Ņ ĐąŅĐģĐ´ŅŅŅ, ĐļĶĐŊĐĩ ĐąĐ°ŅŌĐ°ĐģĐ°Ņ."
        ),
        "_service_title": "âī¸ ŌĐ°ĐļĐĩŅŅŅ ĐŧĐžĐ´ŅĐģĐ´ĐĩŅ",
        "_service_desc": (
            "ŌĐ°ĐļĐĩŅŅŅ ĐŧĐžĐ´ŅĐģĐ´ĐĩŅ â Đ°ĐēĐēĐ°ŅĐŊŅŅ ĐąĐ°ŅŌĐ°ŅŅ, ŅŅĐģŅĐĩĐŧĐĩĐŊŅ ŌŅŅŌĐ°ŅĐ°Đŋ, ŅĐˇĐ´ĐĩŅŅŅ, ĐļĶĐŊĐĩ"
            " ĐąĐ°ŅŌĐ°ĐģĐ°Ņ."
        ),
        "_downloaders_title": "đĨ ĐŌ¯ĐēŅĐĩŅŅŅĐģĐĩŅ",
        "_downloaders_desc": (
            "ĐŌ¯ĐēŅĐĩŅŅŅĐģĐĩŅ ŅŅĐˇŅĐŧŅ â YouTube, TikTok, Instagram, Spotify, VK ĐŅĐˇŅĐēĐ°, ĐļĶĐŊĐĩ"
            " ĐąĐ°ŅŌĐ°ĐģĐ°Ņ Ō¯ŅŅĐŊ ŅĐ°ĐšĐģĐ´Đ°ŅĐ´Ņ ĐļŌ¯ĐēŅĐĩŅĐŗĐĩ ĐļĶĐŊĐĩ ŌĐ°ĐšŅĐ° ĐļŌ¯ĐēŅĐĩĐŋ Đ°ĐģŅŌĐ° ĐēĶŠĐŧĐĩĐēŅĐĩŅĐĩĐ´Ņ."
        ),
        "welcome": (
            "đ <b>ĐĄĶĐģĐĩĐŧĐĩŅŅŅĐˇ ĐąĐĩ! ĐĐ´Đ°ĐŧĐ´Đ°ŅĐ´ŅŌŖ ĐēĐ°ĐŊĐ°ĐģĐ´Đ°ŅŅĐŊĐ´Đ°ŌŅ ĐąĐĩŅĐēŅĐŊŅŅ ĐŧĐžĐ´ŅĐģĐ´ĐĩŅĐ´Ņ ŅĐ°ŌŖĐ´Đ°ŅŌĐ°"
            " ŌŌąĐŊĐ´ŅŌŅŌŖŅĐˇ ĐąĐ°Ņ ĐąĐ°? ĐĐĩĐŊ ĐąŅĐˇĐ´ŅŌŖ ĐļŌ¯ĐēŅĐĩĐģĐŗĐĩĐŊ ĐŊĐ°ĐąĐžŅĐģĐ°ŅĐ´ŅŌŖ ĐąŅŅĐŊĐĩŅĐĩ ŅŅĐˇŅĐŧŅĐŊ ŅŅĐˇĐŗĐĩ"
            " ŌąŅŅĐŊĐ°ĐŧŅĐŊ. ĐĐŗĐĩŅ ŅŅĐˇĐ´Đĩ ĐąŌąĐģ ĐŧĐĩĐŊŅĐ´Ņ ŌĐ°ĐšŅĐ° ŌĐžŅŅĐģŅŌĐ° ĐąĐžĐģŅĐ°, /presets ĐēĐžĐŧĐ°ĐŊĐ´Đ°ŅŅĐŊ"
            " ĐļŅĐąĐĩŅŅŌŖŅĐˇ</b>"
        ),
        "preset": "<b>{}:</b>\nâšī¸ <i>{}</i>\n\nâ <b>ĐŌąĐģ ĐŊĐ°ĐąĐžŅĐ´Đ°ŌŅ ĐŧĐžĐ´ŅĐģĐ´ĐĩŅ:</b>\n\n{}",
        "back": "đ ĐŅŅŌĐ°",
        "install": "đĻ ĐŅĐŊĐ°ŅŅ",
        "installing": (
            "<emoji document_id=5451732530048802485>âŗ</emoji> <b>ĐŅĐŊĐ°ŅŅ ĐŊĐ°ĐąĐžŅŅ"
            " >/b><code>{}</code><b>...</b>"
        ),
        "installing_module": (
            "<emoji document_id=5451732530048802485>âŗ</emoji> <b>ĐŅĐŊĐ°ŅŅ ĐŊĐ°ĐąĐžŅŅ"
            "</b> <code>{}</code> <b>({}/{} ĐŧĐžĐ´ŅĐģĐ´ĐĩŅ)...</b>\n\n<emoji"
            " document_id=5188377234380954537>đ</emoji> <i>ĐĐžĐ´ŅĐģŅ ĐžŅĐŊĐ°ŅŅ {}...</i>"
        ),
        "installed": (
            "<emoji document_id=5436040291507247633>đ</emoji> <b>ĐĐ°ĐąĐžŅ"
            "</b> <code>{}</code> <b>ĐžŅĐŊĐ°ŅŅĐģĐ´Ņ!</b>"
        ),
        "already_installed": "â [ĐŅĐŊĐ°ŅŅĐģĐ´Ņ]",
    }

    async def client_ready(self):
        self._markup = utils.chunks(
            [
                {
                    "text": self.strings(f"_{preset}_title"),
                    "callback": self._preset,
                    "args": (preset,),
                }
                for preset in PRESETS
            ],
            1,
        )

        if self.get("sent"):
            return

        self.set("sent", True)
        await self._menu()

    async def _menu(self):
        await self.inline.bot.send_message(
            self._client.tg_id,
            self.strings("welcome"),
            reply_markup=self.inline.generate_markup(self._markup),
        )

    async def _back(self, call: InlineCall):
        await call.edit(self.strings("welcome"), reply_markup=self._markup)

    async def _install(self, call: InlineCall, preset: str):
        await call.delete()
        m = await self._client.send_message(
            self.inline.bot_id,
            self.strings("installing").format(preset),
        )
        for i, module in enumerate(PRESETS[preset]):
            await m.edit(
                self.strings("installing_module").format(
                    preset, i, len(PRESETS[preset]), module
                )
            )
            try:
                await self.lookup("loader").download_and_install(module, None)
            except Exception:
                logger.exception("Failed to install module %s", module)

            await asyncio.sleep(1)

        if self.lookup("loader").fully_loaded:
            self.lookup("loader").update_modules_in_db()

        await m.edit(self.strings("installed").format(preset))
        await self._menu()

    def _is_installed(self, link: str) -> bool:
        return any(
            link.strip().lower() == installed.strip().lower()
            for installed in self.lookup("loader").get("loaded_modules", {}).values()
        )

    async def _preset(self, call: InlineCall, preset: str):
        await call.edit(
            self.strings("preset").format(
                self.strings(f"_{preset}_title"),
                self.strings(f"_{preset}_desc"),
                "\n".join(
                    map(
                        lambda x: x[0],
                        sorted(
                            [
                                (
                                    "{} <b>{}</b>".format(
                                        (
                                            self.strings("already_installed")
                                            if self._is_installed(link)
                                            else "âĢī¸"
                                        ),
                                        link.rsplit("/", maxsplit=1)[1].split(".")[0],
                                    ),
                                    int(self._is_installed(link)),
                                )
                                for link in PRESETS[preset]
                            ],
                            key=lambda x: x[1],
                            reverse=True,
                        ),
                    )
                ),
            ),
            reply_markup=[
                {"text": self.strings("back"), "callback": self._back},
                {
                    "text": self.strings("install"),
                    "callback": self._install,
                    "args": (preset,),
                },
            ],
        )

    async def aiogram_watcher(self, message: BotInlineMessage):
        if message.text != "/presets" or message.from_user.id != self._client.tg_id:
            return

        await self._menu()
