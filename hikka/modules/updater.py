# ÂŠī¸ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# đ https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# đ https://www.gnu.org/licenses/agpl-3.0.html

import asyncio
import contextlib
import logging
import os
import subprocess
import sys
import time
import typing

import git
from git import GitCommandError, Repo
from telethon.extensions.html import CUSTOM_EMOJIS
from telethon.tl.functions.messages import (
    GetDialogFiltersRequest,
    UpdateDialogFilterRequest,
)
from telethon.tl.types import DialogFilter, Message

from .. import loader, main, utils, version
from .._internal import restart
from ..inline.types import InlineCall

logger = logging.getLogger(__name__)


@loader.tds
class UpdaterMod(loader.Module):
    """Updates itself"""

    strings = {
        "name": "Updater",
        "source": (
            "<emoji document_id=5456255401194429832>đ</emoji> <b>Read the source code"
            " from</b> <a href='{}'>here</a>"
        ),
        "restarting_caption": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>Your {} is"
            " restarting...</b>"
        ),
        "downloading": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>Downloading"
            " updates...</b>"
        ),
        "installing": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>Installing"
            " updates...</b>"
        ),
        "success": (
            "<emoji document_id=5326015457155620929>âą</emoji> <b>Restart successful!"
            " {}</b>\n<i>But still loading modules...</i>\n<i>Restart took {}s</i>"
        ),
        "origin_cfg_doc": "Git origin URL, for where to update from",
        "btn_restart": "đ Restart",
        "btn_update": "đ§­ Update",
        "restart_confirm": "â <b>Are you sure you want to restart?</b>",
        "secure_boot_confirm": (
            "â <b>Are you sure you want to restart in secure boot mode?</b>"
        ),
        "update_confirm": (
            "â <b>Are you sure you"
            " want to update?\n\n<a"
            ' href="https://github.com/hikariatama/Hikka/commit/{}">{}</a> â¤ <a'
            ' href="https://github.com/hikariatama/Hikka/commit/{}">{}</a></b>'
        ),
        "no_update": "đ¸ <b>You are on the latest version, pull updates anyway?</b>",
        "cancel": "đĢ Cancel",
        "lavhost_update": (
            "<emoji document_id=5469986291380657759>âī¸</emoji> <b>Your {} is"
            " updating...</b>"
        ),
        "full_success": (
            "<emoji document_id=5301096082674032190>đ</emoji> <b>Userbot is fully"
            " loaded! {}</b>\n<i>Full restart took {}s</i>"
        ),
        "secure_boot_complete": (
            "<emoji document_id=5472308992514464048>đ</emoji> <b>Secure boot completed!"
            " {}</b>\n<i>Restart took {}s</i>"
        ),
    }

    strings_ru = {
        "source": (
            "<emoji document_id=5456255401194429832>đ</emoji> <b>ĐŅŅĐžĐ´ĐŊŅĐš ĐēĐžĐ´ ĐŧĐžĐļĐŊĐž"
            " ĐŋŅĐžŅĐ¸ŅĐ°ŅŅ</b> <a href='{}'>ĐˇĐ´ĐĩŅŅ</a>"
        ),
        "restarting_caption": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>ĐĸĐ˛ĐžŅ {}"
            " ĐŋĐĩŅĐĩĐˇĐ°ĐŗŅŅĐļĐ°ĐĩŅŅŅ...</b>"
        ),
        "downloading": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>ĐĄĐēĐ°ŅĐ¸Đ˛Đ°ĐŊĐ¸Đĩ"
            " ĐžĐąĐŊĐžĐ˛ĐģĐĩĐŊĐ¸Đš...</b>"
        ),
        "installing": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>ĐŖŅŅĐ°ĐŊĐžĐ˛ĐēĐ°"
            " ĐžĐąĐŊĐžĐ˛ĐģĐĩĐŊĐ¸Đš...</b>"
        ),
        "success": (
            "<emoji document_id=5326015457155620929>âą</emoji> <b>ĐĐĩŅĐĩĐˇĐ°ĐŗŅŅĐˇĐēĐ°"
            " ŅŅĐŋĐĩŅĐŊĐ°! {}</b>\n<i>ĐĐž ĐŧĐžĐ´ŅĐģĐ¸ ĐĩŅĐĩ ĐˇĐ°ĐŗŅŅĐļĐ°ŅŅŅŅ...</i>\n<i>ĐĐĩŅĐĩĐˇĐ°ĐŗŅŅĐˇĐēĐ°"
            " ĐˇĐ°ĐŊŅĐģĐ° {} ŅĐĩĐē</i>"
        ),
        "full_success": (
            "<emoji document_id=5301096082674032190>đ</emoji> <b>ĐŽĐˇĐĩŅĐąĐžŅ ĐŋĐžĐģĐŊĐžŅŅŅŅ"
            " ĐˇĐ°ĐŗŅŅĐļĐĩĐŊ! {}</b>\n<i>ĐĐžĐģĐŊĐ°Ņ ĐŋĐĩŅĐĩĐˇĐ°ĐŗŅŅĐˇĐēĐ° ĐˇĐ°ĐŊŅĐģĐ° {} ŅĐĩĐē</i>"
        ),
        "secure_boot_complete": (
            "<emoji document_id=5472308992514464048>đ</emoji> <b>ĐĐĩĐˇĐžĐŋĐ°ŅĐŊĐ°Ņ ĐˇĐ°ĐŗŅŅĐˇĐēĐ°"
            " ĐˇĐ°Đ˛ĐĩŅŅĐĩĐŊĐ°! {}</b>\n<i>ĐĐĩŅĐĩĐˇĐ°ĐŗŅŅĐˇĐēĐ° ĐˇĐ°ĐŊŅĐģĐ° {} ŅĐĩĐē</i>"
        ),
        "origin_cfg_doc": "ĐĄŅŅĐģĐēĐ°, Đ¸Đˇ ĐēĐžŅĐžŅĐžĐš ĐąŅĐ´ŅŅ ĐˇĐ°ĐŗŅŅĐļĐ°ŅŅŅŅ ĐžĐąĐŊĐžĐ˛ĐģĐĩĐŊĐ¸Ņ",
        "btn_restart": "đ ĐĐĩŅĐĩĐˇĐ°ĐŗŅŅĐˇĐ¸ŅŅŅŅ",
        "btn_update": "đ§­ ĐĐąĐŊĐžĐ˛Đ¸ŅŅŅŅ",
        "restart_confirm": "â <b>ĐĸŅ ŅĐ˛ĐĩŅĐĩĐŊ, ŅŅĐž ŅĐžŅĐĩŅŅ ĐŋĐĩŅĐĩĐˇĐ°ĐŗŅŅĐˇĐ¸ŅŅŅŅ?</b>",
        "secure_boot_confirm": (
            "â <b>ĐĸŅ ŅĐ˛ĐĩŅĐĩĐŊ, ŅŅĐž"
            " ŅĐžŅĐĩŅŅ ĐŋĐĩŅĐĩĐˇĐ°ĐŗŅŅĐˇĐ¸ŅŅŅŅ Đ˛ ŅĐĩĐļĐ¸ĐŧĐĩ ĐąĐĩĐˇĐžĐŋĐ°ŅĐŊĐžĐš ĐˇĐ°ĐŗŅŅĐˇĐēĐ¸?</b>"
        ),
        "update_confirm": (
            "â <b>ĐĸŅ ŅĐ˛ĐĩŅĐĩĐŊ, ŅŅĐž"
            " ŅĐžŅĐĩŅŅ ĐžĐąĐŊĐžĐ˛Đ¸ŅŅŅŅ?\n\n<a"
            ' href="https://github.com/hikariatama/Hikka/commit/{}">{}</a> â¤ <a'
            ' href="https://github.com/hikariatama/Hikka/commit/{}">{}</a></b>'
        ),
        "no_update": "đ¸ <b>ĐŖ ŅĐĩĐąŅ ĐŋĐžŅĐģĐĩĐ´ĐŊŅŅ Đ˛ĐĩŅŅĐ¸Ņ. ĐĐąĐŊĐžĐ˛Đ¸ŅŅŅŅ ĐŋŅĐ¸ĐŊŅĐ´Đ¸ŅĐĩĐģŅĐŊĐž?</b>",
        "cancel": "đĢ ĐŅĐŧĐĩĐŊĐ°",
        "_cls_doc": "ĐĐąĐŊĐžĐ˛ĐģŅĐĩŅ ŅĐˇĐĩŅĐąĐžŅ",
        "lavhost_update": (
            "<emoji document_id=5469986291380657759>âī¸</emoji> <b>ĐĸĐ˛ĐžĐš {}"
            " ĐžĐąĐŊĐžĐ˛ĐģŅĐĩŅŅŅ...</b>"
        ),
    }

    strings_fr = {
        "source": (
            "<emoji document_id=5456255401194429832>đ</emoji> <b>Le code source peut"
            " ÃĒtre lu</b> <a href='{}'>ici</a>"
        ),
        "restarting_caption": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>Votre {}"
            " se redÃŠmarre...</b>"
        ),
        "downloading": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>TÃŠlÃŠchargement"
            " des mises Ã  jour...</b>"
        ),
        "installing": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>Installation"
            " des mises Ã  jour...</b>"
        ),
        "success": (
            "<emoji document_id=5326015457155620929>âą</emoji> <b>RedÃŠmarrage rÃŠussi!"
            " {}</b>\n<i>Mais les modules sont toujours en cours de"
            " chargement...</i>\n<i>RedÃŠmarrer a pris {} s</i>"
        ),
        "full_success": (
            "<emoji document_id=5301096082674032190>đ</emoji> <b>L'utilisateur est"
            " totalement chargÃŠ! {}</b>\n<i>RedÃŠmarrer a pris {} s</i>"
        ),
        "secure_boot_complete": (
            "<emoji document_id=5472308992514464048>đ</emoji> <b>Le dÃŠmarrage sÃŠcurisÃŠ"
            " est terminÃŠ! {}</b>\n<i>RedÃŠmarrer a pris {} s</i>"
        ),
        "origin_cfg_doc": (
            "Le lien Ã  partir duquel les mises Ã  jour seront tÃŠlÃŠchargÃŠes"
        ),
        "btn_restart": "đ RedÃŠmarrer",
        "btn_update": "đ§­ Mettre Ã  jour",
        "restart_confirm": "â <b>Ãtes-vous sÃģr de vouloir redÃŠmarrer?</b>",
        "secure_boot_confirm": (
            "â <b>Ãtes-vous sÃģr de vouloir redÃŠmarrer en mode dÃŠmarrage sÃŠcurisÃŠ?</b>"
        ),
        "update_confirm": (
            "â <b>Ãtes-vous sÃģr de vouloir"
            " mettre Ã  jour?</b>\n\n<a"
            ' href="https://github.com/hikariatama/Hikka/commit/{}">{}</a> â¤ <a'
            ' href="https://github.com/hikariatama/Hikka/commit/{}">{}</a></b>'
        ),
        "no_update": (
            "đ¸ <b>Vous avez la derniÃ¨re version. Mettez-vous Ã  jour de force?</b>"
        ),
        "cancel": "đĢ Annuler",
        "_cls_doc": "Mettre Ã  jour l'utilisateur",
        "lavhost_update": (
            "<emoji document_id=5469986291380657759>âī¸</emoji> <b>Votre {}"
            " est en cours de mise Ã  jour ...</b>"
        ),
    }

    strings_it = {
        "source": (
            "<emoji document_id=5456255401194429832>đ</emoji> <b>Il codice sorgente puÃ˛"
            " essere letto</b> <a href='{}'>qui</a>"
        ),
        "restarting_caption": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>Il tuo {}"
            " si sta riavviando...</b>"
        ),
        "downloading": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>Download"
            " aggiornamenti in corso...</b>"
        ),
        "installing": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>Installazione"
            " aggiornamenti in corso...</b>"
        ),
        "success": (
            "<emoji document_id=5326015457155620929>âą</emoji> <b>Riavvio"
            " completato! {}</b>\n<i>Ma i moduli stanno ancora caricando...</i>\n<i>Il"
            " riavvio ha richiesto {} secondi</i>"
        ),
        "full_success": (
            "<emoji document_id=5301096082674032190>đ</emoji> <b>Hikka Ã¨ stato"
            " completamente caricato! {}</b>\n<i>Il riavvio completo ha richiesto {}"
            " secondi</i>"
        ),
        "secure_boot_complete": (
            "<emoji document_id=5472308992514464048>đ</emoji> <b>Avvio sicuro"
            " completato! {}</b>\n<i>Il riavvio ha richiesto {} secondi</i>"
        ),
        "origin_cfg_doc": "Il link da cui scaricare gli aggiornamenti",
        "btn_restart": "đ Riavvio",
        "btn_update": "đ§­ Aggiorna",
        "restart_confirm": "â <b>Sei sicuro di voler riavviare?</b>",
        "secure_boot_confirm": (
            "â <b>Sei sicuro di voler riavviare in modalitÃ  avvio sicuro?</b>"
        ),
        "update_confirm": (
            "â <b>Sei sicuro di"
            " voler aggiornare?\n\n<a"
            ' href="https://github.com/hikariatama/Hikka/commit/{}">{}</a> â¤ <a'
            ' href="https://github.com/hikariatama/Hikka/commit/{}">{}</a></b>'
        ),
        "no_update": "đ¸ <b>Sei giÃ  aggiornato. Forzare l'aggiornamento?</b>",
        "cancel": "đĢ Annulla",
        "_cls_doc": "Aggiorna il tuo userbot",
        "lavhost_update": (
            "<emoji document_id=5469986291380657759>âī¸</emoji> <b>Il tuo {}"
            " sta per essere aggiornato...</b>"
        ),
    }

    strings_de = {
        "source": (
            "<emoji document_id=5456255401194429832>đ</emoji> <b>Der Quellcode kann"
            " hier</b> <a href='{}'>gelesen</a> <b>werden</b>"
        ),
        "restarting_caption": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>Dein {}"
            " wird neugestartet...</b>"
        ),
        "downloading": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>Updates"
            " werden heruntergeladen...</b>"
        ),
        "installing": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>Updates"
            " werden installiert...</b>"
        ),
        "success": (
            "<emoji document_id=5326015457155620929>âą</emoji> <b>Neustart erfolgreich!"
            " {}</b>\n<i>Aber Module werden noch geladen...</i>\n<i>Neustart dauerte {}"
            " Sekunden</i>"
        ),
        "full_success": (
            "<emoji document_id=5301096082674032190>đ</emoji> <b>Dein Userbot ist"
            " vollstÃ¤ndig geladen! {}</b>\n<i>VollstÃ¤ndiger Neustart dauerte {}"
            " Sekunden</i>"
        ),
        "secure_boot_complete": (
            "<emoji document_id=5472308992514464048>đ</emoji> <b>Sicherer Bootvorgang"
            " abgeschlossen! {}</b>\n<i>Neustart dauerte {} Sekunden</i>"
        ),
        "origin_cfg_doc": "Link, von dem Updates heruntergeladen werden",
        "btn_restart": "đ Neustart",
        "btn_update": "đ§­ Update",
        "restart_confirm": "â <b>Bist du sicher, dass du neustarten willst?</b>",
        "secure_boot_confirm": (
            "â <b>Bist du sicher, dass du in den sicheren Modus neustarten willst?</b>"
        ),
        "update_confirm": (
            "â <b>Bist du sicher, dass"
            " du updaten willst?\n\n<a"
            ' href="https://github.com/hikariatama/Hikka/commit/{}">{}</a> â¤ <a'
            ' href="https://github.com/hikariatama/Hikka/commit/{}">{}</a></b>'
        ),
        "no_update": (
            "đ¸ <b>Du hast die neueste Version. Willst du trotzdem updaten?</b>"
        ),
        "cancel": "đĢ Abbrechen",
        "_cls_doc": "Aktualisiert den Userbot",
        "lavhost_update": (
            "<emoji document_id=5469986291380657759>âī¸</emoji> <b>Dein {}"
            " wird aktualisiert...</b>"
        ),
    }

    strings_tr = {
        "source": (
            "<emoji document_id=5456255401194429832>đ</emoji> <b>Kaynak kodunu"
            "</b>  <a href='{}'>buradan oku</a>"
        ),
        "restarting": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>{}"
            " yeniden baÅlatÄąlÄąyor...</b>"
        ),
        "restarting_caption": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>{}"
            " yeniden baÅlatÄąlÄąyor...</b>"
        ),
        "downloading": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>GÃŧncelleme"
            " indiriliyor...</b>"
        ),
        "installing": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>GÃŧncelleme"
            " kuruluyor...</b>"
        ),
        "success": (
            "<emoji document_id=5326015457155620929>âą</emoji> <b>Yeniden baÅlatma"
            " baÅarÄąlÄą! {}</b>\n<i>ModÃŧller yÃŧkleniyor...</i>\n<i>Yeniden baÅlatma {}"
            " saniye sÃŧrdÃŧ</i>"
        ),
        "full_success": (
            "<emoji document_id=5301096082674032190>đ</emoji> <b>KullanÄącÄą botunuz"
            " tamamen yÃŧklendi! {}</b>\n<i>Toplam yeniden baÅlatma {} saniye sÃŧrdÃŧ</i>"
        ),
        "secure_boot_complete": (
            "<emoji document_id=5472308992514464048>đ</emoji> <b>GÃŧvenli mod baÅarÄąyla"
            " tamamlandÄą! {}</b>\n<i>Yeniden baÅlatma {} saniye sÃŧrdÃŧ</i>"
        ),
        "origin_cfg_doc": "Git kaynak URL, gÃŧncelleme indirilecek kaynak",
        "btn_restart": "đ Yeniden baÅlat",
        "btn_update": "đ§­ GÃŧncelle",
        "restart_confirm": "â <b>GerÃ§ekten yeniden baÅlatmak istiyor musunuz?</b>",
        "secure_boot_confirm": (
            "â <b>GerÃ§ekten gÃŧvenli modda yeniden baÅlatmak istiyor musunuz?</b>"
        ),
        "update_confirm": (
            "â <b>GerÃ§ekten gÃŧncellemek istiyor musunuz?\n\n<a"
            ' href="https://github.com/hikariatama/Hikka/commit/{}">{}</a> â¤ <a'
            ' href="https://github.com/hikariatama/Hikka/commit/{}">{}</a></b>'
        ),
        "no_update": "đ¸ <b>Zaten son sÃŧrÃŧmÃŧnÃŧz. GÃŧncelleme yapmak ister misiniz?</b>",
        "cancel": "đĢ Ä°ptal",
        "_cls_doc": "KullanÄącÄą botunu gÃŧnceller",
        "lavhost_update": (
            "<emoji document_id=5469986291380657759>âī¸</emoji> <b>{}"
            " gÃŧncelleniyor...</b>"
        ),
    }

    strings_uz = {
        "restarting": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>{}"
            " qayta ishga tushirilmoqda...</b>"
        ),
        "restarting_caption": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>{}"
            " qayta ishga tushirilmoqda...</b>"
        ),
        "downloading": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>Yangilanish"
            " yuklanmoqda...</b>"
        ),
        "installing": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>Yangilanish"
            " o'rnatilmoqda...</b>"
        ),
        "success": (
            "<emoji document_id=5326015457155620929>âą</emoji> <b>Qayta ishga tushirish"
            " muvaffaqiyatli yakunlandi! {}</b>\n<i>Modullar"
            " yuklanmoqda...</i>\n<i>Qayta ishga tushirish {} soniya davom etdi</i>"
        ),
        "full_success": (
            "<emoji document_id=5301096082674032190>đ</emoji> <b>Sizning botingiz"
            " to'liq yuklandi! {}</b>\n<i>Jami qayta ishga tushirish {} soniya davom"
            " etdi</i>"
        ),
        "secure_boot_complete": (
            "<emoji document_id=5472308992514464048>đ</emoji> <b>Xavfsiz rejim"
            " muvaffaqiyatli yakunlandi! {}</b>\n<i>Qayta ishga tushirish {} soniya"
            " davom etdi</i>"
        ),
        "origin_cfg_doc": "dan yangilanish yuklanadi",
        "btn_restart": "đ Qayta ishga tushirish",
        "btn_update": "đ§­ Yangilash",
        "restart_confirm": "â <b>Haqiqatan ham qayta ishga tushirmoqchimisiz?</b>",
        "secure_boot_confirm": (
            "â <b>Haqiqatan ham xavfsiz rejimda qayta ishga tushirmoqchimisiz?</b>"
        ),
        "update_confirm": (
            "â <b>Haqiqatan ham yangilamoqchimisiz?\n\n<a"
            ' href="https://github.com/hikariatama/Hikka/commit/{}">{}</a> â¤ <a'
            ' href="https://github.com/hikariatama/Hikka/commit/{}">{}</a></b>'
        ),
        "no_update": (
            "đ¸ <b>Siz allaqachon eng so'nggi versiyasiz. Yangilamoqchimisiz?</b>"
        ),
        "cancel": "đĢ Bekor qilish",
        "_cls_doc": "Foydalanuvchi botini yangilaydi",
        "lavhost_update": (
            "<emoji document_id=5469986291380657759>âī¸</emoji> <b>{}"
            " yangilanmoqda...</b>"
        ),
    }

    strings_es = {
        "restarting": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>{} Reiniciando...</b>"
        ),
        "restarting_caption": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>{} Reiniciando...</b>"
        ),
        "downloading": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>Descargando la"
            " actualizaciÃŗn...</b>"
        ),
        "installing": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>Instalando la"
            " actualizaciÃŗn...</b>"
        ),
        "success": (
            "<emoji document_id=5326015457155620929>âą</emoji> <b>Reiniciado con ÃŠxito!"
            " {}</b>\n<i>Descargando mÃŗdulos...</i>\n<i>Reiniciado en {} segundos</i>"
        ),
        "full_success": (
            "<emoji document_id=5301096082674032190>đ</emoji> <b>ÂĄBot actualizado con"
            " ÃŠxito! {}</b>\n<i>Reiniciado en {} segundos</i>"
        ),
        "secure_boot_complete": (
            "<emoji document_id=5472308992514464048>đ</emoji> <b>ÂĄModo de arranque"
            " seguro activado! {}</b>\n<i>Reiniciado en {} segundos</i>"
        ),
        "origin_cfg_doc": "Descargar actualizaciÃŗn desde",
        "btn_restart": "đ Reiniciar",
        "btn_update": "đ§­ Actualizar",
        "restart_confirm": "â <b>ÂŋQuieres reiniciar?</b>",
        "secure_boot_confirm": (
            "â <b>ÂŋQuieres reiniciar en modo de arranque seguro?</b>"
        ),
        "update_confirm": (
            "â <b>ÂŋQuieres actualizar?\n\n<a"
            ' href="https://github.com/hikariatama/Hikka/commit/{}">{}</a> â¤ <a'
            ' href="https://github.com/hikariatama/Hikka/commit/{}">{}</a></b>'
        ),
        "no_update": "đ¸ <b>Esta es la Ãēltima versiÃŗn. ÂŋQuieres actualizar?</b>",
        "cancel": "đĢ Cancelar",
        "_cls_doc": "El usuario reinicia el bot",
        "lavhost_update": (
            "<emoji document_id=5328274090262275771>âī¸</emoji> <b>{}"
            " Actualizando...</b>"
        ),
    }

    strings_kk = {
        "source": (
            "<emoji document_id=5456255401194429832>đ</emoji> <b>ĐĐ°ŅŅĐ°ĐŋŌŅ ĐēĐžĐ´Ņ</b> <a"
            ' href="{}">ĐąŌąĐģ ĐļĐĩŅĐ´Đĩ</a> ŌĐ°ŅĐ°ŅŌĐ° ĐąĐžĐģĐ°Đ´Ņ'
        ),
        "restarting_caption": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>ĐĸĐ˛ĐžĐš {}"
            " ĐŋĐĩŅĐĩĐˇĐ°ĐŗŅŅĐļĐ°ĐĩŅŅŅ...</b>"
        ),
        "downloading": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>ĐĐ°ŌŖĐ°ŅŅŅĐģĐ°ŅĐ´Ņ"
            " ĐļŌ¯ĐēŅĐĩŅ...</b>"
        ),
        "installing": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>ĐĐ°ŌŖĐ°ŅŅŅĐģĐ°ŅĐ´Ņ"
            " ĐžŅĐŊĐ°ŅŅ...</b>"
        ),
        "success": (
            "<emoji document_id=5326015457155620929>âą</emoji> <b>ĐĐ°ŌŖĐ°ŅŅŅ ŅĶŅŅŅ"
            " Đ°ŅŌŅĐ°ĐģĐ´Ņ! {}</b>\n<i>ĐŅŅĐ°Ō ĐŧĐžĐ´ŅĐģŅĐ´ĐĩŅ ĶĐģŅ ĐļŌ¯ĐēŅĐĩĐģŅĐ´Đĩ...</i>\n<i>ĐĐ°ŌŖĐ°ŅŅŅ"
            " {} ŅĐĩĐēŅĐŊĐ´ŌĐ° Đ°ŅŌŅĐ°ĐģĐ´Ņ</i>"
        ),
        "full_success": (
            "<emoji document_id=5301096082674032190>đ</emoji> <b>ĐŽĐˇĐĩŅĐąĐžŅ ŅĐžĐģŅŌ"
            " ĐļŌ¯ĐēŅĐĩĐģĐ´Ņ! {}</b>\n<i>ĐĸĐžĐģŅŌ ĐļĐ°ŌŖĐ°ŅŅŅ {} ŅĐĩĐēŅĐŊĐ´ŌĐ° Đ°ŅŌŅĐ°ĐģĐ´Ņ</i>"
        ),
        "secure_boot_complete": (
            "<emoji document_id=5472308992514464048>đ</emoji> <b>ĐĐĩĐˇĐŋĐĩĐēĐĩ ŅĐĩĐļĐ¸ĐŧŅ"
            " Đ°ŅŌŅĐ°ĐģĐ´Ņ! {}</b>\n<i>ĐĐ°ŌŖĐ°ŅŅŅ {} ŅĐĩĐēŅĐŊĐ´ŌĐ° Đ°ŅŌŅĐ°ĐģĐ´Ņ</i>"
        ),
        "origin_cfg_doc": "ĐĐ°ŌŖĐ°ŅŅŅĐģĐ°ŅĐ´Ņ ĐļŌ¯ĐēŅĐĩŅ Ō¯ŅŅĐŊ ŅŅĐģŅĐĩĐŧĐĩ",
        "btn_restart": "đ ĐĐ°ŌŖĐ°ŅŅŅ",
        "btn_update": "đ§­ ĐĐ°ŌŖĐ°ŅŅŅ",
        "restart_confirm": "â <b>ĐĄĐĩĐŊ ĐļĐ°ŌŖĐ°ŅŅŅŌĐ° ŅĐĩĐŊŅĐŧĐ´ŅŅŅĐŊ ĐąĐĩ?</b>",
        "secure_boot_confirm": (
            "â <b>ĐĄĐĩĐŊ ĐąŌąĐģ ĐąĐĩŅŅŅ ĐąĐĩĐˇĐŋĐĩĐēĐĩ ŅĐĩĐļĐ¸ĐŧŅĐŊĐ´Đĩ ĐļĐ°ŌŖĐ°ŅŅŅŌĐ° ŅĐĩĐŊŅĐŧĐ´ŅŅŅĐŊ ĐąĐĩ?</b>"
        ),
        "update_confirm": (
            "â <b>ĐĄĐĩĐŊ ĐļĐ°ŌŖĐ°ŅŅŅŌĐ° ŅĐĩĐŊŅĐŧĐ´ŅŅŅĐŊ ĐąĐĩ?\n\n<a"
            ' href="https://github.com/hikariatama/Hikka/commit/{}">{}</a> â¤ <a'
            ' href="https://github.com/hikariatama/Hikka/commit/{}">{}</a></b>'
        ),
        "no_update": (
            "đ¸ <b>ĐĄŅĐˇĐ´ŅŌŖ ŅĐžŌŖŌŅ ĐŊŌąŅŌĐ°ĐŊŅŌŖŅĐˇ ĐąĐ°Ņ. ĐĄŅĐˇ ĐļĐ°ŌŖĐ°ŅŅŅŌĐ° ĐŧŌ¯ĐŧĐēŅĐŊĐ´ŅĐē ĐąĐĩŅĐĩĐ´Ņ ĐŧĐĩ?</b>"
        ),
        "cancel": "đĢ ĐĐ°Ņ ŅĐ°ŅŅŅ",
        "_cls_doc": "ĐŽĐˇĐĩŅĐąĐžŅŅŅ ĐļĐ°ŌŖĐ°ŅŅŅ",
        "lavhost_update": (
            "<emoji document_id=5469986291380657759>âī¸</emoji> <b>ĐĄŅĐˇĐ´ŅŌŖ {}"
            " ĐļĐ°ŌŖĐ°ŅŅŅŌĐ° ĐąĐ°ŅŅĐ°ĐģĐ´Ņ...</b>"
        ),
    }

    strings_tt = {
        "source": (
            "<emoji document_id=5456255401194429832>đ</emoji> <b>Đ§ŅĐŗĐ°ĐŊĐ°Đē ĐēĐžĐ´ŅĐŊ <a"
            " href='{}'>ĐŧĐžĐŊĐ´Đ°</a> ŅĐēŅĐŋ ĐąŅĐģĐ°</b>"
        ),
        "restarting_caption": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>ĐĄĐĩĐˇĐŊĐĩŌŖ {} ŅŌŖĐ°Đ´Đ°ĐŊ"
            " ĐąĐ°ŅĐģĐ°ĐŊĐ°...</b>"
        ),
        "downloading": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>Đ¯ŌŖĐ°ŅŅŅĐģĐ°ŅĐŊŅ"
            " ĐšĶŠĐēĐģĶŌ¯...</b>"
        ),
        "installing": (
            "<emoji document_id=5328274090262275771>đ</emoji> <b>Đ¯ŌŖĐ°ŅŅŅĐģĐ°Ņ"
            " ŅŅĐŊĐ°ŅŅŅŅŅ...</b>"
        ),
        "success": (
            "<emoji document_id=5326015457155620929>âą</emoji> <b>Đ¯ŌŖĐ°ŅŅŅ ĐąĐĩŅŅĐĩ! {}</b>\n"
            "<i>ĐĶĐēĐ¸ĐŊ ĐŧĐžĐ´ŅĐģŅĐģĶŅ ĶĐģĐĩ ĐšĶŠĐēĐģĶĐŊĶ...</i>\n<i>Đ¯ŌŖĐ°ŅŅŅ {} ŅĐĩĐē Đ´ĶĐ˛Đ°Đŧ Đ¸ŅŅĐĩ</i>"
        ),
        "full_success": (
            "<emoji document_id=5301096082674032190>đ</emoji> <b>ĐŽĐˇĐĩŅĐąĐžŅ ŅŅĐģŅŅŅĐŊŅĐ°"
            " ĐšĶŠĐēĐģĶĐŊĐŗĶĐŊ! {}</b>\n<i>ĐĸŅĐģŅ ŅŌŖĐ°Đ´Đ°ĐŊ ĐąĐ°ŅĐģĐ°Ņ {} ŅĐĩĐē Đ´ĶĐ˛Đ°Đŧ Đ¸ŅŅĐĩ</i>"
        ),
        "secure_boot_complete": (
            "<emoji document_id=5472308992514464048>đ</emoji> <b>ĐŅŅĐēŅĐŊŅŅŅŅĐˇ ĐšĶŠĐēĐģĶŌ¯"
            " ŅĶĐŧĐ°ĐŧĐģĐ°ĐŊĐ´Ņ! {}</b>\n<i>Đ¯ŌŖĐ°ŅŅŅ {} ŅĐĩĐē Đ´ĶĐ˛Đ°Đŧ Đ¸ŅŅĐĩ</i>"
        ),
        "origin_cfg_doc": "Đ¯ŌŖĐ°ŅŅŅĐģĐ°Ņ ĐšĶŠĐēĐģĶĐŊĶŅĶĐē ŅŅĐģŅĐ°ĐŧĐ°",
        "btn_restart": "đ ĐĐ°ĐąŅĐˇŅ",
        "btn_update": "đ§­ Đ¯ŌŖĐ°ŅŅ",
        "restart_confirm": "â <b>ĐĸŅ ŅĐ˛ĐĩŅĐĩĐŊ, ŅŅĐž ŅĐžŅĐĩŅŅ ĐŋĐĩŅĐĩĐˇĐ°ĐŗŅŅĐˇĐ¸ŅŅŅŅ?</b>",
        "secure_boot_confirm": "â <b>ĐĄĐĩĐˇ ŅŌŖĐ°Đ´Đ°ĐŊ ĐąĐ°ŅĐģĐ°ŅĐŗĐ° ŅĐĩĐģĐ¸ŅĐĩĐˇĐŧĐĩ?</b>",
        "update_confirm": (
            "â <b>ĐĄĐĩĐˇ ŅŌŖĐ°ŅŅŅŅĐŗĐ° ŅĐĩĐģĐ¸ŅĐĩĐˇĐŧĐĩ?\n\n<a"
            ' href="https://github.com/hikariatama/Hikka/commit/{}">{}</a> â¤ <a'
            ' href="https://github.com/hikariatama/Hikka/commit/{}">{}</a></b>'
        ),
        "no_update": "đ¸ <b>ĐĄĐĩĐˇĐŊĐĩŌŖ ŅĐžŌŖĐŗŅ Đ˛ĐĩŅŅĐ¸ŅĐŗĐĩĐˇ ĐąĐ°Ņ. Đ¯ŌŖĐ°ŅŅŅ ĐŧĶŌĐąŌ¯ŅĐ¸ĐŧĐĩ?</b>",
        "cancel": "đĢ ĐĐĩŅĐĩŅŌ¯",
        "_cls_doc": "ĐŽĐˇĐĩŅĐąĐžŅĐŊŅ ŅŌŖĐ°ŅŅĐ°",
        "lavhost_update": (
            "<emoji document_id=5328274090262275771>âī¸</emoji> <b>ĐĄĐĩĐˇĐŊĐĩŌŖ {}"
            " ŅŌŖĐ°ŅŅŅĐģĐ°...</b>"
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "GIT_ORIGIN_URL",
                "https://github.com/hikariatama/Hikka",
                lambda: self.strings("origin_cfg_doc"),
                validator=loader.validators.Link(),
            )
        )

    @loader.owner
    @loader.command(
        ru_doc="ĐĐĩŅĐĩĐˇĐ°ĐŗŅŅĐļĐ°ĐĩŅ ŅĐˇĐĩŅĐąĐžŅ",
        fr_doc="RedÃŠmarre le bot",
        it_doc="Riavvia il bot",
        de_doc="Startet den Userbot neu",
        tr_doc="KullanÄącÄą botunu yeniden baÅlatÄąr",
        uz_doc="Foydalanuvchi botini qayta ishga tushiradi",
        es_doc="Reinicia el bot",
        kk_doc="ĐŌ¯ĐēŅĐĩĐŗĐĩĐŊ ĐąĐžŅŅŅ ŌĐ°ĐšŅĐ° ĐļŌ¯ĐēŅĐĩĐšĐ´Ņ",
    )
    async def restart(self, message: Message):
        """Restarts the userbot"""
        args = utils.get_args_raw(message)
        secure_boot = any(trigger in args for trigger in {"--secure-boot", "-sb"})
        try:
            if (
                "-f" in args
                or not self.inline.init_complete
                or not await self.inline.form(
                    message=message,
                    text=self.strings(
                        "secure_boot_confirm" if secure_boot else "restart_confirm"
                    ),
                    reply_markup=[
                        {
                            "text": self.strings("btn_restart"),
                            "callback": self.inline_restart,
                            "args": (secure_boot,),
                        },
                        {"text": self.strings("cancel"), "action": "close"},
                    ],
                )
            ):
                raise
        except Exception:
            await self.restart_common(message, secure_boot)

    async def inline_restart(self, call: InlineCall, secure_boot: bool = False):
        await self.restart_common(call, secure_boot=secure_boot)

    async def process_restart_message(self, msg_obj: typing.Union[InlineCall, Message]):
        self.set(
            "selfupdatemsg",
            msg_obj.inline_message_id
            if hasattr(msg_obj, "inline_message_id")
            else f"{utils.get_chat_id(msg_obj)}:{msg_obj.id}",
        )

    async def restart_common(
        self,
        msg_obj: typing.Union[InlineCall, Message],
        secure_boot: bool = False,
    ):
        if (
            hasattr(msg_obj, "form")
            and isinstance(msg_obj.form, dict)
            and "uid" in msg_obj.form
            and msg_obj.form["uid"] in self.inline._units
            and "message" in self.inline._units[msg_obj.form["uid"]]
        ):
            message = self.inline._units[msg_obj.form["uid"]]["message"]
        else:
            message = msg_obj

        if secure_boot:
            self._db.set(loader.__name__, "secure_boot", True)

        msg_obj = await utils.answer(
            msg_obj,
            self.strings("restarting_caption").format(
                utils.get_platform_emoji()
                if self._client.hikka_me.premium
                and CUSTOM_EMOJIS
                and isinstance(msg_obj, Message)
                else "Hikka"
            ),
        )

        await self.process_restart_message(msg_obj)

        self.set("restart_ts", time.time())

        await self._db.remote_force_save()

        if "LAVHOST" in os.environ:
            os.system("lavhost restart")
            return

        with contextlib.suppress(Exception):
            await main.hikka.web.stop()

        handler = logging.getLogger().handlers[0]
        handler.setLevel(logging.CRITICAL)

        for client in self.allclients:
            # Terminate main loop of all running clients
            # Won't work if not all clients are ready
            if client is not message.client:
                await client.disconnect()

        await message.client.disconnect()
        restart()

    async def download_common(self):
        try:
            repo = Repo(os.path.dirname(utils.get_base_dir()))
            origin = repo.remote("origin")
            r = origin.pull()
            new_commit = repo.head.commit
            for info in r:
                if info.old_commit:
                    for d in new_commit.diff(info.old_commit):
                        if d.b_path == "requirements.txt":
                            return True
            return False
        except git.exc.InvalidGitRepositoryError:
            repo = Repo.init(os.path.dirname(utils.get_base_dir()))
            origin = repo.create_remote("origin", self.config["GIT_ORIGIN_URL"])
            origin.fetch()
            repo.create_head("master", origin.refs.master)
            repo.heads.master.set_tracking_branch(origin.refs.master)
            repo.heads.master.checkout(True)
            return False

    @staticmethod
    def req_common():
        # Now we have downloaded new code, install requirements
        logger.debug("Installing new requirements...")
        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    os.path.join(
                        os.path.dirname(utils.get_base_dir()),
                        "requirements.txt",
                    ),
                    "--user",
                ],
                check=True,
            )
        except subprocess.CalledProcessError:
            logger.exception("Req install failed")

    @loader.owner
    @loader.command(
        ru_doc="ĐĄĐēĐ°ŅĐ¸Đ˛Đ°ĐĩŅ ĐžĐąĐŊĐžĐ˛ĐģĐĩĐŊĐ¸Ņ ŅĐˇĐĩŅĐąĐžŅĐ°",
        fr_doc="TÃŠlÃŠcharge les mises Ã  jour du bot",
        it_doc="Scarica gli aggiornamenti del bot",
        de_doc="LÃ¤dt Updates fÃŧr den Userbot herunter",
        tr_doc="Userbot gÃŧncellemelerini indirir",
        uz_doc="Userbot yangilanishlarini yuklaydi",
        es_doc="Descarga las actualizaciones del bot",
        kk_doc="ĐŌ¯ĐšĐĩ ĐļĐ°ŌŖĐ°ŅŅŅĐģĐ°ŅŅĐŊ ĐļŌ¯ĐēŅĐĩĐšĐ´Ņ",
    )
    async def update(self, message: Message):
        """Downloads userbot updates"""
        try:
            args = utils.get_args_raw(message)
            current = utils.get_git_hash()
            upcoming = next(
                git.Repo().iter_commits(f"origin/{version.branch}", max_count=1)
            ).hexsha
            if (
                "-f" in args
                or not self.inline.init_complete
                or not await self.inline.form(
                    message=message,
                    text=self.strings("update_confirm").format(
                        current, current[:8], upcoming, upcoming[:8]
                    )
                    if upcoming != current
                    else self.strings("no_update"),
                    reply_markup=[
                        {
                            "text": self.strings("btn_update"),
                            "callback": self.inline_update,
                        },
                        {"text": self.strings("cancel"), "action": "close"},
                    ],
                )
            ):
                raise
        except Exception:
            await self.inline_update(message)

    async def inline_update(
        self,
        msg_obj: typing.Union[InlineCall, Message],
        hard: bool = False,
    ):
        # We don't really care about asyncio at this point, as we are shutting down
        if hard:
            os.system(f"cd {utils.get_base_dir()} && cd .. && git reset --hard HEAD")

        try:
            if "LAVHOST" in os.environ:
                msg_obj = await utils.answer(
                    msg_obj,
                    self.strings("lavhost_update").format(
                        "</b><emoji document_id=5192756799647785066>âī¸</emoji><emoji"
                        " document_id=5193117564015747203>âī¸</emoji><emoji"
                        " document_id=5195050806105087456>âī¸</emoji><emoji"
                        " document_id=5195457642587233944>âī¸</emoji><b>"
                        if self._client.hikka_me.premium
                        and CUSTOM_EMOJIS
                        and isinstance(msg_obj, Message)
                        else "lavHost"
                    ),
                )
                await self.process_restart_message(msg_obj)
                os.system("lavhost update")
                return

            with contextlib.suppress(Exception):
                msg_obj = await utils.answer(msg_obj, self.strings("downloading"))

            req_update = await self.download_common()

            with contextlib.suppress(Exception):
                msg_obj = await utils.answer(msg_obj, self.strings("installing"))

            if req_update:
                self.req_common()

            await self.restart_common(msg_obj)
        except GitCommandError:
            if not hard:
                await self.inline_update(msg_obj, True)
                return

            logger.critical("Got update loop. Update manually via .terminal")

    @loader.unrestricted
    @loader.command(
        ru_doc="ĐĐžĐēĐ°ĐˇĐ°ŅŅ ŅŅŅĐģĐēŅ ĐŊĐ° Đ¸ŅŅĐžĐ´ĐŊŅĐš ĐēĐžĐ´ ĐŋŅĐžĐĩĐēŅĐ°",
        fr_doc="Affiche le lien vers le code source du projet",
        it_doc="Mostra il link al codice sorgente del progetto",
        de_doc="Zeigt den Link zum Quellcode des Projekts an",
        tr_doc="Proje kaynak kodu baÄlantÄąsÄąnÄą gÃļsterir",
        uz_doc="Loyihaning manba kodiga havola ko'rsatadi",
        es_doc="Muestra el enlace al cÃŗdigo fuente del proyecto",
        kk_doc="ĐĐžĐąĐ°ĐŊŅŌŖ ŌĐ°ĐšĐŊĐ°Ņ ĐēĐžĐ´ŅĐŊĐ° ŅŅĐģŅĐĩĐŧĐĩ ĐēĶŠŅŅĐĩŅĐĩĐ´Ņ",
    )
    async def source(self, message: Message):
        """Links the source code of this project"""
        await utils.answer(
            message,
            self.strings("source").format(self.config["GIT_ORIGIN_URL"]),
        )

    async def client_ready(self):
        if self.get("selfupdatemsg") is not None:
            try:
                await self.update_complete()
            except Exception:
                logger.exception("Failed to complete update!")

        if self.get("do_not_create", False):
            return

        try:
            await self._add_folder()
        except Exception:
            logger.exception("Failed to add folder!")

        self.set("do_not_create", True)

    async def _add_folder(self):
        folders = await self._client(GetDialogFiltersRequest())

        if any(getattr(folder, "title", None) == "hikka" for folder in folders):
            return

        try:
            folder_id = (
                max(
                    folders,
                    key=lambda x: x.id,
                ).id
                + 1
            )
        except ValueError:
            folder_id = 2

        try:
            await self._client(
                UpdateDialogFilterRequest(
                    folder_id,
                    DialogFilter(
                        folder_id,
                        title="hikka",
                        pinned_peers=(
                            [
                                await self._client.get_input_entity(
                                    self._client.loader.inline.bot_id
                                )
                            ]
                            if self._client.loader.inline.init_complete
                            else []
                        ),
                        include_peers=[
                            await self._client.get_input_entity(dialog.entity)
                            async for dialog in self._client.iter_dialogs(
                                None,
                                ignore_migrated=True,
                            )
                            if dialog.name
                            in {
                                "hikka-logs",
                                "hikka-onload",
                                "hikka-assets",
                                "hikka-backups",
                                "hikka-acc-switcher",
                                "silent-tags",
                            }
                            and dialog.is_channel
                            and (
                                dialog.entity.participants_count == 1
                                or dialog.entity.participants_count == 2
                                and dialog.name in {"hikka-logs", "silent-tags"}
                            )
                            or (
                                self._client.loader.inline.init_complete
                                and dialog.entity.id
                                == self._client.loader.inline.bot_id
                            )
                            or dialog.entity.id
                            in [
                                1554874075,
                                1697279580,
                                1679998924,
                            ]  # official hikka chats
                        ],
                        emoticon="đą",
                        exclude_peers=[],
                        contacts=False,
                        non_contacts=False,
                        groups=False,
                        broadcasts=False,
                        bots=False,
                        exclude_muted=False,
                        exclude_read=False,
                        exclude_archived=False,
                    ),
                )
            )
        except Exception:
            logger.critical(
                "Can't create Hikka folder. Possible reasons are:\n"
                "- User reached the limit of folders in Telegram\n"
                "- User got floodwait\n"
                "Ignoring error and adding folder addition to ignore list"
            )

    async def update_complete(self):
        logger.debug("Self update successful! Edit message")
        start = self.get("restart_ts")
        try:
            took = round(time.time() - start)
        except Exception:
            took = "n/a"

        msg = self.strings("success").format(utils.ascii_face(), took)
        ms = self.get("selfupdatemsg")

        if ":" in str(ms):
            chat_id, message_id = ms.split(":")
            chat_id, message_id = int(chat_id), int(message_id)
            await self._client.edit_message(chat_id, message_id, msg)
            return

        await self.inline.bot.edit_message_text(
            inline_message_id=ms,
            text=self.inline.sanitise_text(msg),
        )

    async def full_restart_complete(self, secure_boot: bool = False):
        start = self.get("restart_ts")

        try:
            took = round(time.time() - start)
        except Exception:
            took = "n/a"

        self.set("restart_ts", None)

        ms = self.get("selfupdatemsg")
        msg = self.strings(
            "secure_boot_complete" if secure_boot else "full_success"
        ).format(utils.ascii_face(), took)

        if ms is None:
            return

        self.set("selfupdatemsg", None)

        if ":" in str(ms):
            chat_id, message_id = ms.split(":")
            chat_id, message_id = int(chat_id), int(message_id)
            await self._client.edit_message(chat_id, message_id, msg)
            await asyncio.sleep(60)
            await self._client.delete_messages(chat_id, message_id)
            return

        await self.inline.bot.edit_message_text(
            inline_message_id=ms,
            text=self.inline.sanitise_text(msg),
        )
