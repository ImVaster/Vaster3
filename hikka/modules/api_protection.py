# ÂŠī¸ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# đ https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# đ https://www.gnu.org/licenses/agpl-3.0.html

import asyncio
import io
import json
import logging
import random
import time

from telethon.tl import functions
from telethon.tl.tlobject import TLRequest
from telethon.tl.types import Message

from .. import loader, utils
from ..inline.types import InlineCall
from ..web.debugger import WebDebugger

logger = logging.getLogger(__name__)

GROUPS = [
    "auth",
    "account",
    "users",
    "contacts",
    "messages",
    "updates",
    "photos",
    "upload",
    "help",
    "channels",
    "bots",
    "payments",
    "stickers",
    "phone",
    "langpack",
    "folders",
    "stats",
]


CONSTRUCTORS = {
    (lambda x: x[0].lower() + x[1:])(
        method.__class__.__name__.rsplit("Request", 1)[0]
    ): method.CONSTRUCTOR_ID
    for method in utils.array_sum(
        [
            [
                method
                for method in dir(getattr(functions, group))
                if isinstance(method, TLRequest)
            ]
            for group in GROUPS
        ]
    )
}


@loader.tds
class APIRatelimiterMod(loader.Module):
    """Helps userbot avoid spamming Telegram API"""

    strings = {
        "name": "APILimiter",
        "warning": (
            "<emoji document_id=5312383351217201533>â ī¸</emoji>"
            " <b>WARNING!</b>\n\nYour account exceeded the limit of requests, specified"
            " in config. In order to prevent Telegram API Flood, userbot has been"
            " <b>fully frozen</b> for {} seconds. Further info is provided in attached"
            " file. \n\nIt is recommended to get help in <code>{prefix}support</code>"
            " group!\n\nIf you think, that it is an intended behavior, then wait until"
            " userbot gets unlocked and next time, when you will be going to perform"
            " such an operation, use <code>{prefix}suspend_api_protect</code> &lt;time"
            " in seconds&gt;"
        ),
        "args_invalid": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Invalid arguments</b>"
        ),
        "suspended_for": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>API Flood Protection"
            " is disabled for {} seconds</b>"
        ),
        "on": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>Protection enabled</b>"
        ),
        "off": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>Protection"
            " disabled</b>"
        ),
        "u_sure": "â ī¸ <b>Are you sure?</b>",
        "_cfg_time_sample": "Time sample through which the bot will count requests",
        "_cfg_threshold": "Threshold of requests to trigger protection",
        "_cfg_local_floodwait": (
            "Freeze userbot for this amount of time, if request limit exceeds"
        ),
        "_cfg_forbidden_methods": (
            "Forbid specified methods from being executed throughout external modules"
        ),
        "btn_no": "đĢ No",
        "btn_yes": "â Yes",
        "web_pin": (
            "đ <b>Click the button below to show Werkzeug debug PIN. Do not give it to"
            " anyone.</b>"
        ),
        "web_pin_btn": "đ Show Werkzeug PIN",
        "proxied_url": "đ Proxied URL",
        "local_url": "đ  Local URL",
        "debugger_disabled": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Web debugger is"
            " disabled, url is not available</b>"
        ),
    }

    strings_ru = {
        "warning": (
            "<emoji document_id=5312383351217201533>â ī¸</emoji>"
            " <b>ĐĐĐĐĐĐĐĐ!</b>\n\nĐĐēĐēĐ°ŅĐŊŅ Đ˛ŅŅĐĩĐģ ĐˇĐ° ĐģĐ¸ĐŧĐ¸ŅŅ ĐˇĐ°ĐŋŅĐžŅĐžĐ˛, ŅĐēĐ°ĐˇĐ°ĐŊĐŊŅĐĩ Đ˛"
            " ĐēĐžĐŊŅĐ¸ĐŗĐĩ. ĐĄ ŅĐĩĐģŅŅ ĐŋŅĐĩĐ´ĐžŅĐ˛ŅĐ°ŅĐĩĐŊĐ¸Ņ ŅĐģŅĐ´Đ° Telegram API, ŅĐˇĐĩŅĐąĐžŅ ĐąŅĐģ"
            " <b>ĐŋĐžĐģĐŊĐžŅŅŅŅ ĐˇĐ°ĐŧĐžŅĐžĐļĐĩĐŊ</b> ĐŊĐ° {} ŅĐĩĐēŅĐŊĐ´. ĐĐžĐŋĐžĐģĐŊĐ¸ŅĐĩĐģŅĐŊĐ°Ņ Đ¸ĐŊŅĐžŅĐŧĐ°ŅĐ¸Ņ"
            " ĐŋŅĐ¸ĐēŅĐĩĐŋĐģĐĩĐŊĐ° Đ˛ ŅĐ°ĐšĐģĐĩ ĐŊĐ¸ĐļĐĩ. \n\nĐ ĐĩĐēĐžĐŧĐĩĐŊĐ´ŅĐĩŅŅŅ ĐžĐąŅĐ°ŅĐ¸ŅŅŅŅ ĐˇĐ° ĐŋĐžĐŧĐžŅŅŅ Đ˛"
            " <code>{prefix}support</code> ĐŗŅŅĐŋĐŋŅ!\n\nĐŅĐģĐ¸ ŅŅ ŅŅĐ¸ŅĐ°ĐĩŅŅ, ŅŅĐž ŅŅĐž"
            " ĐˇĐ°ĐŋĐģĐ°ĐŊĐ¸ŅĐžĐ˛Đ°ĐŊĐŊĐžĐĩ ĐŋĐžĐ˛ĐĩĐ´ĐĩĐŊĐ¸Đĩ ŅĐˇĐĩŅĐąĐžŅĐ°, ĐŋŅĐžŅŅĐž ĐŋĐžĐ´ĐžĐļĐ´Đ¸, ĐŋĐžĐēĐ° ĐˇĐ°ĐēĐžĐŊŅĐ¸ŅŅŅ"
            " ŅĐ°ĐšĐŧĐĩŅ Đ¸ Đ˛ ŅĐģĐĩĐ´ŅŅŅĐ¸Đš ŅĐ°Đˇ, ĐēĐžĐŗĐ´Đ° ĐˇĐ°ĐŋĐģĐ°ĐŊĐ¸ŅŅĐĩŅŅ Đ˛ŅĐŋĐžĐģĐŊŅŅŅ ŅĐ°ĐēŅŅ"
            " ŅĐĩŅŅŅŅĐžĐˇĐ°ŅŅĐ°ŅĐŊŅŅ ĐžĐŋĐĩŅĐ°ŅĐ¸Ņ, Đ¸ŅĐŋĐžĐģŅĐˇŅĐš"
            " <code>{prefix}suspend_api_protect</code> &lt;Đ˛ŅĐĩĐŧŅ Đ˛ ŅĐĩĐēŅĐŊĐ´Đ°Ņ&gt;"
        ),
        "args_invalid": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĐĩĐ˛ĐĩŅĐŊŅĐĩ Đ°ŅĐŗŅĐŧĐĩĐŊŅŅ</b>"
        ),
        "suspended_for": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>ĐĐ°ŅĐ¸ŅĐ° API ĐžŅĐēĐģŅŅĐĩĐŊĐ°"
            " ĐŊĐ° {} ŅĐĩĐēŅĐŊĐ´</b>"
        ),
        "on": "<emoji document_id=5458450833857322148>đ</emoji> <b>ĐĐ°ŅĐ¸ŅĐ° Đ˛ĐēĐģŅŅĐĩĐŊĐ°</b>",
        "off": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>ĐĐ°ŅĐ¸ŅĐ° ĐžŅĐēĐģŅŅĐĩĐŊĐ°</b>"
        ),
        "u_sure": "<emoji document_id=5312383351217201533>â ī¸</emoji> <b>ĐĸŅ ŅĐ˛ĐĩŅĐĩĐŊ?</b>",
        "_cfg_time_sample": (
            "ĐŅĐĩĐŧĐĩĐŊĐŊĐžĐš ĐŋŅĐžĐŧĐĩĐļŅŅĐžĐē, ĐŋĐž ĐēĐžŅĐžŅĐžĐŧŅ ĐąŅĐ´ĐĩŅ ŅŅĐ¸ŅĐ°ŅŅŅŅ ĐēĐžĐģĐ¸ŅĐĩŅŅĐ˛Đž ĐˇĐ°ĐŋŅĐžŅĐžĐ˛"
        ),
        "_cfg_threshold": "ĐĐžŅĐžĐŗ ĐˇĐ°ĐŋŅĐžŅĐžĐ˛, ĐŋŅĐ¸ ĐēĐžŅĐžŅĐžĐŧ ĐąŅĐ´ĐĩŅ ŅŅĐ°ĐąĐ°ŅŅĐ˛Đ°ŅŅ ĐˇĐ°ŅĐ¸ŅĐ°",
        "_cfg_local_floodwait": (
            "ĐĐ°ĐŧĐžŅĐžĐˇĐ¸ŅŅ ŅĐˇĐĩŅĐąĐžŅĐ° ĐŊĐ° ŅŅĐž ĐēĐžĐģĐ¸ŅĐĩŅŅĐ˛Đž ŅĐĩĐēŅĐŊĐ´, ĐĩŅĐģĐ¸ ĐģĐ¸ĐŧĐ¸Ņ ĐˇĐ°ĐŋŅĐžŅĐžĐ˛ ĐŋŅĐĩĐ˛ŅŅĐĩĐŊ"
        ),
        "_cfg_forbidden_methods": (
            "ĐĐ°ĐŋŅĐĩŅĐ¸ŅŅ Đ˛ŅĐŋĐžĐģĐŊĐĩĐŊĐ¸Đĩ ŅĐēĐ°ĐˇĐ°ĐŊĐŊŅŅ ĐŧĐĩŅĐžĐ´ĐžĐ˛ Đ˛Đž Đ˛ŅĐĩŅ Đ˛ĐŊĐĩŅĐŊĐ¸Ņ ĐŧĐžĐ´ŅĐģŅŅ"
        ),
        "btn_no": "đĢ ĐĐĩŅ",
        "btn_yes": "â ĐĐ°",
        "web_pin": (
            "đ <b>ĐĐ°ĐļĐŧĐ¸ ĐŊĐ° ĐēĐŊĐžĐŋĐēŅ ĐŊĐ¸ĐļĐĩ, ŅŅĐžĐąŅ ĐŋĐžĐēĐ°ĐˇĐ°ŅŅ Werkzeug debug PIN. ĐĐĩ Đ´Đ°Đ˛Đ°Đš ĐĩĐŗĐž"
            " ĐŊĐ¸ĐēĐžĐŧŅ.</b>"
        ),
        "web_pin_btn": "đ ĐĐžĐēĐ°ĐˇĐ°ŅŅ Werkzeug PIN",
        "proxied_url": "đ ĐŅĐžĐēŅĐ¸ŅĐžĐ˛Đ°ĐŊĐŊĐ°Ņ ŅŅŅĐģĐēĐ°",
        "local_url": "đ  ĐĐžĐēĐ°ĐģŅĐŊĐ°Ņ ŅŅŅĐģĐēĐ°",
        "debugger_disabled": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĐĩĐą-ĐžŅĐģĐ°Đ´ŅĐ¸Đē ĐžŅĐēĐģŅŅĐĩĐŊ,"
            " ŅŅŅĐģĐēĐ° ĐŊĐĩĐ´ĐžŅŅŅĐŋĐŊĐ°</b>"
        ),
    }

    strings_fr = {
        "warning": (
            "<emoji document_id=5312383351217201533>â ī¸</emoji>"
            " <b>ATTENTION!</b>\n\nLe compte a dÃŠpassÃŠ les limites de requÃĒtes"
            " spÃŠcifiÃŠes dans la configuration. En vue de prÃŠvenir le flood de"
            " l'API Telegram, le userbot a ÃŠtÃŠ <b>complÃ¨tement gelÃŠ</b> pendant {}"
            " secondes. Des informations supplÃŠmentaires sont ajoutÃŠes dans le"
            " fichier ci-dessous.\n\nIl est recommandÃŠ de contacter le groupe"
            " <code>{prefix}support</code> pour obtenir de l'aide!\n\nSi vous"
            " pensez que le comportement du userbot a ÃŠtÃŠ planifiÃŠ, attendez"
            " simplement que le minuteur se termine et, la prochaine fois que"
            " vous prÃŠvoyez d'exÃŠcuter une opÃŠration aussi coÃģteuse en ressources,"
            " utilisez <code>{prefix}suspend_api_protect</code> &lt;temps en"
            " secondes&gt;"
        ),
        "args_invalid": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Arguments"
            " invalides</b>"
        ),
        "suspended_for": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>Protection API"
            " dÃŠsactivÃŠe pendant {} secondes</b>"
        ),
        "on": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>Protection activÃŠe</b>"
        ),
        "off": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>Protection"
            " dÃŠsactivÃŠe</b>"
        ),
        "u_sure": (
            "<emoji document_id=5312383351217201533>â ī¸</emoji> <b>Ãtes-vous sÃģr?</b>"
        ),
        "_cfg_time_sample": (
            "Intervalle de temps sur lequel le nombre de demandes sera comptÃŠ"
        ),
        "_cfg_threshold": "Seuil de demandes auquel la protection sera dÃŠclenchÃŠe",
        "_cfg_local_floodwait": (
            "Geler le userbot pendant cette durÃŠe de secondes si la limite de"
            " requÃĒtes est dÃŠpassÃŠe"
        ),
        "_cfg_forbidden_methods": (
            "Interdire l'exÃŠcution des mÃŠthodes spÃŠcifiÃŠes dans tous les modules"
            " externes"
        ),
        "btn_no": "đĢ Non",
        "btn_yes": "â Oui",
        "web_pin": (
            "đ <b>Cliquez sur le bouton ci-dessous pour afficher le code PIN de"
            " dÃŠbogage de Werkzeug. Ne le donnez pas Ã  personne.</b>"
        ),
        "web_pin_btn": "đ Afficher le code PIN de Werkzeug",
        "proxied_url": "đ Lien de proxification",
        "local_url": "đ  Lien local",
        "debugger_disabled": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Le dÃŠbogueur Web est"
            " dÃŠsactivÃŠ, le lien n'est pas disponible</b>"
        ),
    }

    strings_it = {
        "warning": (
            "<emoji document_id=5312383351217201533>â ī¸</emoji> <b>ATTENZIONE!</b>\n\nIl"
            " tuo account Ã¨ uscito dai limiti di richieste impostati nel file config."
            " Per evitare flood di richieste, il bot Ã¨ stato <b>completamente"
            " sospeso</b> per {} secondi. Ulteriori informazioni sono disponibili nel"
            " file allegato. \n\nTi consigliamo di unirti al gruppo"
            " <code>{prefix}support</code> per ulteriore assistenza!\n\nSe ritieni che"
            " questo sia un comportamento programmato del bot, puoi semplicemente"
            " aspettare che il timer finisca e, in seguito, quando pianifichi di"
            " eseguire operazioni cosÃŦ pesanti, usa"
            " <code>{prefix}suspend_api_protect</code> &lt;tempo in secondi&gt;"
        ),
        "args_invalid": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Argomenti non"
            " validi</b>"
        ),
        "suspended_for": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>Protezione API"
            " disattivata per {} secondi</b>"
        ),
        "on": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>Protezione"
            " attivata</b>"
        ),
        "off": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>Protezione"
            " disattivata</b>"
        ),
        "u_sure": (
            "<emoji document_id=5312383351217201533>â ī¸</emoji> <b>Sei sicuro?</b>"
        ),
        "_cfg_time_sample": (
            "Intervallo di tempo per il quale verranno conteggiate le richieste"
        ),
        "_cfg_threshold": (
            "Limite delle richieste, al di sopra del quale verrÃ  attivato"
            " il sistema di protezione"
        ),
        "_cfg_local_floodwait": (
            "Il bot verrÃ  sospeso per questo numero di secondi se il limite delle"
            " richieste viene superato"
        ),
        "_cfg_forbidden_methods": (
            "Vieta l'esecuzione di questi metodi in tutti i moduli esterni"
        ),
        "btn_no": "đĢ No",
        "btn_yes": "â SÃŦ",
        "web_pin": (
            "đ <b>Premi il pulsante qui sotto per mostrare il PIN di debug di Werkzeug."
            " Non darglielo a nessuno.</b>"
        ),
        "web_pin_btn": "đ Mostra PIN di Werkzeug",
        "proxied_url": "đ URL del proxy",
        "local_url": "đ  URL locale",
        "debugger_disabled": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Il debugger web Ã¨"
            " disabilitato, l'URL non Ã¨ disponibile</b>"
        ),
    }

    strings_de = {
        "warning": (
            "<emoji document_id=5312383351217201533>â ī¸</emoji>"
            " <b>Achtung!</b>\n\nDas Konto hat die in der Konfiguration angegebenen"
            " Grenzwerte fÃŧr Anfragen Ãŧberschritten. Um Telegram API-Flooding zu"
            " verhindern, wurde der <b>ganze Userbot</b> fÃŧr {} Sekunden"
            " eingefroren. Weitere Informationen finden Sie im unten angefÃŧgten"
            " Datei.\n\nWir empfehlen Ihnen, sich mit Hilfe der <code>{prefix}"
            "support</code> Gruppe zu helfen!\n\nWenn du denkst, dass dies"
            " geplantes Verhalten des Userbots ist, dann warte einfach, bis der"
            " Timer ablÃ¤uft und versuche beim nÃ¤chsten Mal, eine so ressourcen"
            " intensive Operation wie <code>{prefix}suspend_api_protect</code>"
            " &lt;Zeit in Sekunden&gt; zu planen."
        ),
        "args_invalid": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>UngÃŧltige"
            " Argumente</b>"
        ),
        "suspended_for": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>API Flood"
            " Protection ist fÃŧr {} Sekunden deaktiviert</b>"
        ),
        "on": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>Schutz aktiviert</b>"
        ),
        "off": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>Schutz deaktiviert</b>"
        ),
        "u_sure": "â ī¸ <b>Bist du sicher?</b>",
        "_cfg_time_sample": "Zeitintervall, in dem die Anfragen gezÃ¤hlt werden",
        "_cfg_threshold": (
            "Schwellenwert fÃŧr Anfragen, ab dem der Schutz aktiviert wird"
        ),
        "_cfg_local_floodwait": (
            "Einfrieren des Userbots fÃŧr diese Anzahl von Sekunden, wenn der Grenzwert"
            " Ãŧberschritten wird"
        ),
        "_cfg_forbidden_methods": "Verbotene Methoden in allen externen Modulen",
        "btn_no": "đĢ Nein",
        "btn_yes": "â Ja",
        "web_pin": (
            "đ <b>DrÃŧcke auf die SchaltflÃ¤che unten, um den Werkzeug debug PIN"
            " anzuzeigen. Gib ihn niemandem.</b>"
        ),
        "web_pin_btn": "đ Werkzeug PIN anzeigen",
        "proxied_url": "đ Proxied URL",
        "local_url": "đ  Lokale URL",
        "debugger_disabled": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Web-Debugger"
            " deaktiviert, Link nicht verfÃŧgbar</b>"
        ),
    }

    strings_tr = {
        "warning": (
            "<emoji document_id=5312383351217201533>â ī¸</emoji> <b>Dikkat!</b>\n\nHesap"
            " yapÄąlandÄąrmasÄąnda belirtilen sÄąnÄąr deÄerlerini aÅtÄą. Telegram API"
            " sÄązmalarÄąnÄą Ãļnlemek iÃ§in <b>tÃŧm Userbot</b> {} sanie donduruldu. Daha"
            " fazla bilgi iÃ§in aÅaÄÄąya eklenen dosyaya bakÄąn.\n\nLÃŧtfen"
            " <code>{prefix}support</code> grubu ile yardÄąm almak iÃ§in destek"
            " olun!\n\nEÄer bu, Userbot'un planlanmÄąÅ davranÄąÅÄą olduÄunu"
            " dÃŧÅÃŧnÃŧyorsanÄąz, zamanlayÄącÄą bittiÄinde ve"
            " <code>{prefix}suspend_api_protect</code> &lt;saniye cinsinden sÃŧre&gt;"
            " gibi kaynak tÃŧketen bir iÅlemi planladÄąÄÄąnÄązda yeniden deneyin."
        ),
        "args_invalid": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>GeÃ§ersiz"
            " argÃŧmanlar</b>"
        ),
        "suspended_for": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>API Flood korumasÄą {}"
            " saniyeliÄine durduruldu.</b>"
        ),
        "on": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>Koruma"
            " aktifleÅtirildi.</b>"
        ),
        "off": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>Koruma"
            " de-aktifleÅtirildi</b>"
        ),
        "u_sure": "â ī¸ <b>Emin misin?</b>",
        "_cfg_time_sample": "Saniyede sayÄąlan isteklerin zaman aralÄąÄÄą",
        "_cfg_threshold": "KorumanÄąn etkinleÅeceÄi sÄąnÄąr deÄeri",
        "_cfg_local_floodwait": (
            "Telegram API sÄąnÄąr deÄeri aÅÄąldÄąÄÄąnda kullanÄącÄą botu bir sÃŧre durdurulur"
        ),
        "_cfg_forbidden_methods": (
            "Belirtili metodlarÄąn harici modÃŧller tarafÄąndan Ã§alÄąÅtÄąrÄąlmasÄąnÄą yasakla"
        ),
        "btn_no": "đĢ HayÄąr",
        "btn_yes": "â Evet",
        "web_pin": (
            "đ <b>Werkzeug hata ayÄąklama PIN'ini gÃļstermek iÃ§in aÅaÄÄądaki dÃŧÄmeyi"
            " tÄąklayÄąn. Onu kimseye vermeyin.</b>"
        ),
        "web_pin_btn": "đ Werkzeug PIN'ini gÃļster",
        "proxied_url": "đ Proxied URL",
        "local_url": "đ  Lokal URL",
        "debugger_disabled": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Web-Debugger devre"
            " dÄąÅÄą, baÄlantÄą kullanÄąlamaz</b>"
        ),
    }

    strings_uz = {
        "warning": (
            "<emoji document_id=5312383351217201533>â ī¸</emoji>"
            " <b>Ogohlantirish!</b>\n\nBu hisob uchun konfiguratsiyada ko'rsatilgan"
            " chegaralar chegarani o'zgartirgan.\n\nTelegram API Flood"
            " to'xtatish uchun, bu <b>hammasi userbot</b> uchun {} sekundni"
            " blokirovka qilindi. Batafsil ma'lumot uchun pastdagi faylni o'qing.\n\n"
            "Yordam uchun <code>{prefix}support</code> guruhidan foydalaning!\n\nAgar"
            " siz hisobni botning yordamchisi bo'lishi kerak bo'lgan amalni bajarishga"
            " imkoniyat berishga o'xshaysiz, unda faqat blokirovkani to'xtatish uchun"
            " <code>{prefix}suspend_api_protect</code> &lt;sekund&gt; dan foydalaning."
        ),
        "args_invalid": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Noto'g'ri argument</b>"
        ),
        "suspended_for": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>API Flood"
            " himoya {} sekund uchun to'xtatildi</b>"
        ),
        "on": "<emoji document_id=5458450833857322148>đ</emoji> <b>Himoya yoqildi</b>",
        "off": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>Himoya o'chirildi</b>"
        ),
        "u_sure": "â ī¸ <b>Siz ishonchingiz komilmi?</b>",
        "_cfg_time_sample": "Sekundda qabul qilinadigan so'rovlar soni chegarasi",
        "_cfg_threshold": "Himoya yoqish uchun qiymatni chegaralash",
        "_cfg_local_floodwait": (
            "Foydalanuvchi botni ushbu soniya davomida blokirovka qiladi, agar"
            " chegaralar qiymati oshsa"
        ),
        "_cfg_forbidden_methods": "Barcha tashqi modullarda taqiqlangan usullar",
        "btn_no": "đĢ Yo'q",
        "btn_yes": "â Ha",
        "web_pin": (
            "đ <b>Werkzeug Debug PIN kodini ko'rsatish uchun quyidagi tugmani bosing."
            " Uni hech kimga bermang.</b>"
        ),
        "web_pin_btn": "đ Werkzeug PIN-ni ko'rsatish",
        "proxied_url": "đ Proxied URL",
        "local_url": "đ  Lokal URL",
        "debugger_disabled": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Web-Debugger"
            " o'chirilgan, ulanish mavjud emas</b>"
        ),
    }

    strings_es = {
        "warning": (
            "<emoji document_id=5312383351217201533>â ī¸</emoji>"
            " <b>ÂĄAdvertencia!</b>\n\nDe acuerdo con la configuraciÃŗn de esta cuenta,"
            " las siguientes limitaciones serÃĄn aplicadas.\n\nSe bloquearÃĄ <b>a todos"
            " los bots de los usuarios</b> por {} segundos para evitar el exceso de las"
            " limitaciones de Telegram API. Para mÃĄs informaciÃŗn, consulta el archivo"
            " siguiente.\n\nPara obtener ayuda, use el grupo"
            " <code>{prefix}support</code>!\n\nPara permitir que la cuenta funcione,"
            " use <code>{prefix}suspend_api_protect</code> para desbloquear."
        ),
        "args_invalid": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Argumentos"
            " invÃĄlidos</b>"
        ),
        "suspended_for": (
            "<emoji document_id=5458450833857322148>đ</emoji>"
            " <b>Se ha desactivado la protecciÃŗn de API por {} segundos</b>"
        ),
        "on": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>ProtecciÃŗn"
            " activada</b>"
        ),
        "off": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>ProtecciÃŗn"
            " desactivada</b>"
        ),
        "u_sure": "â ī¸ <b>ÂŋEstÃĄs seguro?</b>",
        "_cfg_time_sample": (
            "El tiempo en segundos durante el cual se exceden las limitaciones"
        ),
        "_cfg_threshold": "El valor por encima del cual se exceden las limitaciones",
        "_cfg_local_floodwait": (
            "El tiempo en segundos durante el cual se bloquea al usuario para el bot"
        ),
        "_cfg_forbidden_methods": (
            "Los comandos prohibidos por todas las extensiones externas"
        ),
        "btn_no": "đĢ No",
        "btn_yes": "â SÃ­",
        "web_pin": (
            "đ <b>Haga clic en el botÃŗn de abajo para mostrar el PIN de depuraciÃŗn de"
            " Werkzeug. No se lo des a nadie.</b>"
        ),
        "web_pin_btn": "đ Mostrar el PIN de Werkzeug",
        "proxied_url": "đ URL de proxy",
        "local_url": "đ  URL local",
        "debugger_disabled": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Web-Debugger"
            " desactivado, conexiÃŗn no disponible</b>"
        ),
    }

    strings_kk = {
        "warning": (
            "<emoji document_id=5312383351217201533>â ī¸</emoji>"
            " <b>ĐŅĐēĐĩŅŅŅ!</b>\n\nĐŌąĐģ ĐĩŅĐĩĐŋŅŅŌŖ ĐēĐžĐŊŅĐ¸ĐŗŅŅĐ°ŅĐ¸ŅŅŅĐŊĐ° ŅĶĐšĐēĐĩŅ, ĐēĐĩĐģĐĩŅŅ"
            " ŅĐĩĐēŅĐĩĐģĐŗĐĩĐŊ ŅĐ°ŅŅŅĐ°Ņ ŌĐžĐģĐ´Đ°ĐŊŅĐģĐ°Đ´Ņ.\n\nTelegram API Ō¯ĐģĐĩŅĐģĐĩŅŅĐŊĐĩĐŊ ŌĐžŅŌĐ°ĐģĐŧĐ°ŅŅ"
            " Ō¯ŅŅĐŊ, <b>ĐąĐ°ŅĐģŅŌ ĐŋĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŅŅĐģĐ°ŅĐ´ŅŌŖ ĐąĐžŅŅĐ°ŅŅ</b> {} ŅĐĩĐēŅĐŊĐ´ ŌŌąĐģŅĐŋŅĐ°ĐģĐ°Đ´Ņ."
            " ĐĶŠĐąŅŅĐĩĐē Đ°ŌĐŋĐ°ŅĐ°Ņ Ō¯ŅŅĐŊ ĐēĐĩĐģĐĩŅŅ ŅĐ°ĐšĐģĐ´Ņ ŌĐ°ŅĐ°ŌŖŅĐˇ.\n\nĐĐŊŅŌŅĐ°ĐŧĐ° Ō¯ŅŅĐŊ"
            " <code>{prefix}support</code> ŅĐžĐŋŅĐŊ ĐŋĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŌŖŅĐˇ!\n\nĐĐŗĐĩŅ ŅŅĐˇĐŗĐĩ"
            " ĐąŌąĐģ ĐĩŅĐĩĐŋŅŅŌŖ ĐąĐžŅŅŅŌŖ ĐēĶŠĐŧĐĩĐēŅŅŅŅ ĐąĐžĐģŅŅ ĐēĐĩŅĐĩĐē ĐąĐžĐģŅĐ°, ŌŌąĐģŅĐŋŅĐ°ĐģŅŅĐŊ ĶŠŅŅŅŅ Ō¯ŅŅĐŊ"
            " <code>{prefix}suspend_api_protect</code> &lt;ŅĐĩĐēŅĐŊĐ´&gt; ĐŋĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŌŖŅĐˇ."
        ),
        "args_invalid": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĐ°ŅĐ°ĐŧŅŅĐˇ"
            " Đ°ŅĐŗŅĐŧĐĩĐŊŅŅĐĩŅ</b>"
        ),
        "suspended_for": (
            "<emoji document_id=5458450833857322148>đ</emoji>"
            " <b>API Ō¯ĐģĐĩŅĐģĐĩŅŅĐŊ ŌĐžŅŌĐ°ĐģŅŅ {} ŅĐĩĐēŅĐŊĐ´ Ō¯ŅŅĐŊ ĶŠŅŅŅŅĐģĐ´Ņ</b>"
        ),
        "on": "<emoji document_id=5458450833857322148>đ</emoji> <b>ŌĐžŅŌĐ°ĐģŅ ŌĐžŅŅĐģĐ´Ņ</b>",
        "off": (
            "<emoji document_id=5458450833857322148>đ</emoji> <b>ŌĐžŅŌĐ°ĐģŅ ĶŠŅŅŅŅĐģĐ´Ņ</b>"
        ),
        "u_sure": "â ī¸ <b>ĐĄŅĐˇ ĶĐģŅĐŧĐ´ŅŅŅĐˇ ĐąĐĩ?</b>",
        "_cfg_time_sample": "API Ō¯ĐģĐĩŅĐģĐĩŅŅĐŊĐĩĐŊ ŌĐžŅŌĐ°ĐģŅŅ Ō¯ŅŅĐŊ ĐēĶŠŅŅĐĩŅŅĐģĐŗĐĩĐŊ ŅĐ°ŌŅŅ (ŅĐĩĐēŅĐŊĐ´)",
        "_cfg_threshold": "API Ō¯ĐģĐĩŅĐģĐĩŅŅĐŊĐĩĐŊ ŌĐžŅŌĐ°ĐģŅŅ Ō¯ŅŅĐŊ ĐēĶŠŅŅĐĩŅŅĐģĐŗĐĩĐŊ ŌĐ°ĐŊŅĐ°ĐģŅŌ",
        "_cfg_local_floodwait": "ĐĐžŅ Ō¯ŅŅĐŊ ĐŋĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŅŅĐŊŅ ŌŌąĐģŅĐŋŅĐ°ĐģŅ ŅĐ°ŌŅŅŅ (ŅĐĩĐēŅĐŊĐ´)",
        "_cfg_forbidden_methods": (
            "ĐĐ°ŅĐģŅŌ ŅŅŅŅŌŅ ŌĐžŅŅĐŧŅĐ°ĐģĐ°ŅĐ´ŅŌŖ ŌĐžĐģĐ´Đ°ĐŊŅĐģŅŅĐŊŅŌŖ ŅŅĐšŅĐŧ ŅĐ°ĐģŅĐŊŌĐ°ĐŊ ĐēĐžĐŧĐ°ĐŊĐ´Đ°ĐģĐ°ŅŅ"
        ),
        "btn_no": "đĢ ĐĐžŌ",
        "btn_yes": "â ĐĶ",
        "web_pin": (
            "đ <b>Werkzeug Đ´ĐĩĐąĐ°Đŗ PIN ĐēĐžĐ´ŅĐŊ ĐēĶŠŅŅĐĩŅŅ Ō¯ŅŅĐŊ ŅĶŠĐŧĐĩĐŊĐ´ĐĩĐŗŅ ŅŌ¯ĐšĐŧĐĩŅŅĐēŅŅ"
            " ĐąĐ°ŅŅŌŖŅĐˇ. ĐĐŊŅ ĐēŅĐŧŅŅĐŊĐĩ Đ´Đĩ ĐąĐĩŅĐŧĐĩŌŖŅĐˇ.</b>"
        ),
        "web_pin_btn": "đ Werkzeug PIN ĐēĐžĐ´ŅĐŊ ĐēĶŠŅŅĐĩŅŅ",
        "proxied_url": "đ ĐŅĐžĐēŅĐ¸ URL",
        "local_url": "đ  ĐĐĩŅĐŗŅĐģŅĐēŅŅ URL",
        "debugger_disabled": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Web-Debugger"
            " ĶŠŅŅŅŅĐģĐŗĐĩĐŊ, ĐąĐ°ĐšĐģĐ°ĐŊŅŅ ĐļĐžŌ</b>"
        ),
    }

    _ratelimiter = []
    _suspend_until = 0
    _lock = False

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "time_sample",
                15,
                lambda: self.strings("_cfg_time_sample"),
                validator=loader.validators.Integer(minimum=1),
            ),
            loader.ConfigValue(
                "threshold",
                100,
                lambda: self.strings("_cfg_threshold"),
                validator=loader.validators.Integer(minimum=10),
            ),
            loader.ConfigValue(
                "local_floodwait",
                30,
                lambda: self.strings("_cfg_local_floodwait"),
                validator=loader.validators.Integer(minimum=10, maximum=3600),
            ),
            loader.ConfigValue(
                "forbidden_methods",
                ["joinChannel", "importChatInvite"],
                lambda: self.strings("_cfg_forbidden_methods"),
                validator=loader.validators.MultiChoice(
                    [
                        "sendReaction",
                        "joinChannel",
                        "importChatInvite",
                    ]
                ),
                on_change=lambda: self._client.forbid_constructors(
                    map(
                        lambda x: CONSTRUCTORS[x], self.config["forbidden_constructors"]
                    )
                ),
            ),
        )

    async def client_ready(self):
        asyncio.ensure_future(self._install_protection())

    async def _install_protection(self):
        await asyncio.sleep(30)  # Restart lock
        if hasattr(self._client._call, "_old_call_rewritten"):
            raise loader.SelfUnload("Already installed")

        old_call = self._client._call

        async def new_call(
            sender: "MTProtoSender",  # type: ignore
            request: "TLRequest",  # type: ignore
            ordered: bool = False,
            flood_sleep_threshold: int = None,
        ):
            await asyncio.sleep(random.randint(1, 5) / 100)
            if time.perf_counter() > self._suspend_until and not self.get(
                "disable_protection",
                True,
            ):
                request_name = type(request).__name__
                self._ratelimiter += [[request_name, time.perf_counter()]]

                self._ratelimiter = list(
                    filter(
                        lambda x: time.perf_counter() - x[1]
                        < int(self.config["time_sample"]),
                        self._ratelimiter,
                    )
                )

                if (
                    len(self._ratelimiter) > int(self.config["threshold"])
                    and not self._lock
                ):
                    self._lock = True
                    report = io.BytesIO(
                        json.dumps(
                            self._ratelimiter,
                            indent=4,
                        ).encode("utf-8")
                    )
                    report.name = "local_fw_report.json"

                    await self.inline.bot.send_document(
                        self.tg_id,
                        report,
                        caption=self.strings("warning").format(
                            self.config["local_floodwait"],
                            prefix=self.get_prefix(),
                        ),
                    )

                    # It is intented to use time.sleep instead of asyncio.sleep
                    time.sleep(int(self.config["local_floodwait"]))
                    self._lock = False

            return await old_call(sender, request, ordered, flood_sleep_threshold)

        self._client._call = new_call
        self._client._old_call_rewritten = old_call
        self._client._call._hikka_overwritten = True
        logger.debug("Successfully installed ratelimiter")

    async def on_unload(self):
        if hasattr(self._client, "_old_call_rewritten"):
            self._client._call = self._client._old_call_rewritten
            delattr(self._client, "_old_call_rewritten")
            logger.debug("Successfully uninstalled ratelimiter")

    @loader.command(
        ru_doc="<Đ˛ŅĐĩĐŧŅ Đ˛ ŅĐĩĐēŅĐŊĐ´Đ°Ņ> - ĐĐ°ĐŧĐžŅĐžĐˇĐ¸ŅŅ ĐˇĐ°ŅĐ¸ŅŅ API ĐŊĐ° N ŅĐĩĐēŅĐŊĐ´",
        fr_doc="<secondes> - Congeler la protection de l'API pendant N secondes",
        it_doc="<tempo in secondi> - Congela la protezione API per N secondi",
        de_doc="<Sekunden> - API-Schutz fÃŧr N Sekunden einfrieren",
        tr_doc="<saniye> - API korumasÄąnÄą N saniye dondur",
        uz_doc="<soniya> - API himoyasini N soniya o'zgartirish",
        es_doc="<segundos> - Congela la protecciÃŗn de la API durante N segundos",
        kk_doc="<ŅĐĩĐēŅĐŊĐ´> - API ŌĐžŅŌĐ°ŅŅĐŊ N ŅĐĩĐēŅĐŊĐ´ŅŅĐē ŅĐ°ŌŅŅŅĐ° ŌŌąĐģŅĐŋŅĐ°Ņ",
    )
    async def suspend_api_protect(self, message: Message):
        """<time in seconds> - Suspend API Ratelimiter for n seconds"""
        args = utils.get_args_raw(message)

        if not args or not args.isdigit():
            await utils.answer(message, self.strings("args_invalid"))
            return

        self._suspend_until = time.perf_counter() + int(args)
        await utils.answer(message, self.strings("suspended_for").format(args))

    @loader.command(
        ru_doc="ĐĐēĐģŅŅĐ¸ŅŅ/Đ˛ŅĐēĐģŅŅĐ¸ŅŅ ĐˇĐ°ŅĐ¸ŅŅ API",
        fr_doc="Activer / dÃŠsactiver la protection de l'API",
        it_doc="Attiva/disattiva la protezione API",
        de_doc="API-Schutz einschalten / ausschalten",
        tr_doc="API korumasÄąnÄą aÃ§ / kapat",
        uz_doc="API himoyasini yoqish / o'chirish",
        es_doc="Activar / desactivar la protecciÃŗn de API",
        kk_doc="API ŌĐžŅŌĐ°ŅŅĐŊ ŌĐžŅŅ / ĐļĐžŅ",
    )
    async def api_fw_protection(self, message: Message):
        """Toggle API Ratelimiter"""
        await self.inline.form(
            message=message,
            text=self.strings("u_sure"),
            reply_markup=[
                {"text": self.strings("btn_no"), "action": "close"},
                {"text": self.strings("btn_yes"), "callback": self._finish},
            ],
        )

    @property
    def _debugger(self) -> WebDebugger:
        return logging.getLogger().handlers[0].web_debugger

    async def _show_pin(self, call: InlineCall):
        await call.answer(f"Werkzeug PIN: {self._debugger.pin}", show_alert=True)

    @loader.command(
        ru_doc="ĐĐžĐēĐ°ĐˇĐ°ŅŅ PIN Werkzeug",
        fr_doc="Afficher le PIN Werkzeug",
        it_doc="Mostra il PIN Werkzeug",
        de_doc="PIN-Werkzeug anzeigen",
        tr_doc="PIN aracÄąnÄą gÃļster",
        uz_doc="PIN vositasi ko'rsatish",
        es_doc="Mostrar herramienta PIN",
        kk_doc="PIN ŌŌąŅĐ°ĐģŅĐŊ ĐēĶŠŅŅĐĩŅŅ",
    )
    async def debugger(self, message: Message):
        """Show the Werkzeug PIN"""
        await self.inline.form(
            message=message,
            text=self.strings("web_pin"),
            reply_markup=[
                [
                    {
                        "text": self.strings("web_pin_btn"),
                        "callback": self._show_pin,
                    }
                ],
                [
                    {"text": self.strings("proxied_url"), "url": self._debugger.url},
                    {
                        "text": self.strings("local_url"),
                        "url": f"http://127.0.0.1:{self._debugger.port}",
                    },
                ],
            ],
        )

    async def _finish(self, call: InlineCall):
        state = self.get("disable_protection", True)
        self.set("disable_protection", not state)
        await call.edit(self.strings("on" if state else "off"))
