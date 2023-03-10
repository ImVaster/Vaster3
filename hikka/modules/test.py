# ÂŠī¸ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# đ https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# đ https://www.gnu.org/licenses/agpl-3.0.html

import inspect
import logging
import os
import random
import time
import typing
from io import BytesIO

from telethon.tl.types import Message

from .. import loader, main, utils
from ..inline.types import InlineCall

logger = logging.getLogger(__name__)

DEBUG_MODS_DIR = os.path.join(utils.get_base_dir(), "debug_modules")

if not os.path.isdir(DEBUG_MODS_DIR):
    os.mkdir(DEBUG_MODS_DIR, mode=0o755)

for mod in os.scandir(DEBUG_MODS_DIR):
    os.remove(mod.path)


@loader.tds
class TestMod(loader.Module):
    """Perform operations based on userbot self-testing"""

    _memory = {}

    strings = {
        "name": "Tester",
        "set_loglevel": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Please specify"
            " verbosity as an integer or string</b>"
        ),
        "no_logs": (
            "<emoji document_id=5363948200291998612>đ¤ˇââī¸</emoji> <b>You don't have any"
            " logs at verbosity</b> <code>{}</code><b>.</b>"
        ),
        "logs_caption": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>Hikka logs with"
            " verbosity</b> <code>{}</code>\n\n<emoji"
            " document_id=6318902906900711458>âĒī¸</emoji> <b>Version:"
            " {}.{}.{}</b>{}"
        ),
        "suspend_invalid_time": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Invalid time to"
            " suspend</b>"
        ),
        "suspended": (
            "<emoji document_id=5452023368054216810>đĨļ</emoji> <b>Bot suspended"
            " for</b> <code>{}</code> <b>seconds</b>"
        ),
        "results_ping": (
            "<emoji document_id=5431449001532594346>âĄī¸</emoji> <b>Telegram ping:</b>"
            " <code>{}</code> <b>ms</b>\n<emoji"
            " document_id=5445284980978621387>đ</emoji> <b>Uptime: {}</b>"
        ),
        "ping_hint": (
            "<emoji document_id=5472146462362048818>đĄ</emoji> <i>Telegram ping mostly"
            " depends on Telegram servers latency and other external factors and has"
            " nothing to do with the parameters of server on which userbot is"
            " installed</i>"
        ),
        "confidential": (
            "â ī¸ <b>Log level</b> <code>{}</code> <b>may reveal your confidential info,"
            " be careful</b>"
        ),
        "confidential_text": (
            "â ī¸ <b>Log level</b> <code>{0}</code> <b>may reveal your confidential info,"
            " be careful</b>\n<b>Type</b> <code>.logs {0} force_insecure</code> <b>to"
            " ignore this warning</b>"
        ),
        "choose_loglevel": "đââī¸ <b>Choose log level</b>",
        "bad_module": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Module not found</b>"
        ),
        "debugging_enabled": (
            "<emoji document_id=5332533929020761310>â</emoji> <b>Debugging mode enabled"
            " for module</b> <code>{0}</code>\n<i>Go to directory named"
            " `debug_modules`, edit file named `{0}.py` and see changes in real"
            " time</i>"
        ),
        "debugging_disabled": (
            "<emoji document_id=5332533929020761310>â</emoji> <b>Debugging disabled</b>"
        ),
        "send_anyway": "đ¤ Send anyway",
        "cancel": "đĢ Cancel",
        "logs_cleared": "đ <b>Logs cleared</b>",
    }

    strings_ru = {
        "set_loglevel": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐŖĐēĐ°ĐļĐ¸ ŅŅĐžĐ˛ĐĩĐŊŅ ĐģĐžĐŗĐžĐ˛"
            " ŅĐ¸ŅĐģĐžĐŧ Đ¸ĐģĐ¸ ŅŅŅĐžĐēĐžĐš</b>"
        ),
        "no_logs": (
            "<emoji document_id=5363948200291998612>đ¤ˇââī¸</emoji> <b>ĐŖ ŅĐĩĐąŅ ĐŊĐĩŅ ĐģĐžĐŗĐžĐ˛"
            " ŅŅĐžĐ˛ĐŊŅ</b> <code>{}</code><b>.</b>"
        ),
        "logs_caption": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>ĐĐžĐŗĐ¸ Hikka ŅŅĐžĐ˛ĐŊŅ"
            "</b> <code>{}</code>\n\n<emoji document_id=6318902906900711458>âĒī¸</emoji>"
            " <b>ĐĐĩŅŅĐ¸Ņ: {}.{}.{}</b>{}"
        ),
        "debugging_enabled": (
            "<emoji document_id=5332533929020761310>â</emoji> <b>Đ ĐĩĐļĐ¸Đŧ ŅĐ°ĐˇŅĐ°ĐąĐžŅŅĐ¸ĐēĐ°"
            " Đ˛ĐēĐģŅŅĐĩĐŊ Đ´ĐģŅ ĐŧĐžĐ´ŅĐģŅ</b> <code>{0}</code>\n<i>ĐŅĐŋŅĐ°Đ˛ĐģŅĐšŅŅ Đ˛ Đ´Đ¸ŅĐĩĐēŅĐžŅĐ¸Ņ"
            " `debug_modules`, Đ¸ĐˇĐŧĐĩĐŊŅĐš ŅĐ°ĐšĐģ `{0}.py`, Đ¸ ŅĐŧĐžŅŅĐ¸ Đ¸ĐˇĐŧĐĩĐŊĐĩĐŊĐ¸Ņ Đ˛ ŅĐĩĐļĐ¸ĐŧĐĩ"
            " ŅĐĩĐ°ĐģŅĐŊĐžĐŗĐž Đ˛ŅĐĩĐŧĐĩĐŊĐ¸</i>"
        ),
        "debugging_disabled": (
            "<emoji document_id=5332533929020761310>â</emoji> <b>Đ ĐĩĐļĐ¸Đŧ ŅĐ°ĐˇŅĐ°ĐąĐžŅŅĐ¸ĐēĐ°"
            " Đ˛ŅĐēĐģŅŅĐĩĐŊ</b>"
        ),
        "suspend_invalid_time": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĐĩĐ˛ĐĩŅĐŊĐžĐĩ Đ˛ŅĐĩĐŧŅ"
            " ĐˇĐ°ĐŧĐžŅĐžĐˇĐēĐ¸</b>"
        ),
        "suspended": (
            "<emoji document_id=5452023368054216810>đĨļ</emoji> <b>ĐĐžŅ ĐˇĐ°ĐŧĐžŅĐžĐļĐĩĐŊ ĐŊĐ°</b>"
            " <code>{}</code> <b>ŅĐĩĐēŅĐŊĐ´</b>"
        ),
        "results_ping": (
            "<emoji document_id=5431449001532594346>âĄī¸</emoji> <b>ĐĄĐēĐžŅĐžŅŅŅ ĐžŅĐēĐģĐ¸ĐēĐ°"
            " Telegram:</b> <code>{}</code> <b>ms</b>\n<emoji"
            " document_id=5445284980978621387>đ</emoji> <b>ĐŅĐžŅĐģĐž Ņ ĐŋĐžŅĐģĐĩĐ´ĐŊĐĩĐš"
            " ĐŋĐĩŅĐĩĐˇĐ°ĐŗŅŅĐˇĐēĐ¸: {}</b>"
        ),
        "ping_hint": (
            "<emoji document_id=5472146462362048818>đĄ</emoji> <i>ĐĄĐēĐžŅĐžŅŅŅ ĐžŅĐēĐģĐ¸ĐēĐ°"
            " Telegram Đ˛ ĐąĐžĐģŅŅĐĩĐš ŅŅĐĩĐŋĐĩĐŊĐ¸ ĐˇĐ°Đ˛Đ¸ŅĐ¸Ņ ĐžŅ ĐˇĐ°ĐŗŅŅĐļĐĩĐŊĐŊĐžŅŅĐ¸ ŅĐĩŅĐ˛ĐĩŅĐžĐ˛ Telegram Đ¸"
            " Đ´ŅŅĐŗĐ¸Ņ Đ˛ĐŊĐĩŅĐŊĐ¸Ņ ŅĐ°ĐēŅĐžŅĐžĐ˛ Đ¸ ĐŊĐ¸ĐēĐ°Đē ĐŊĐĩ ŅĐ˛ŅĐˇĐ°ĐŊĐ° Ņ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐ°ĐŧĐ¸ ŅĐĩŅĐ˛ĐĩŅĐ°, ĐŊĐ°"
            " ĐēĐžŅĐžŅŅĐš ŅŅŅĐ°ĐŊĐžĐ˛ĐģĐĩĐŊ ŅĐˇĐĩŅĐąĐžŅ</i>"
        ),
        "confidential": (
            "â ī¸ <b>ĐŖŅĐžĐ˛ĐĩĐŊŅ ĐģĐžĐŗĐžĐ˛</b> <code>{}</code> <b>ĐŧĐžĐļĐĩŅ ŅĐžĐ´ĐĩŅĐļĐ°ŅŅ ĐģĐ¸ŅĐŊŅŅ"
            " Đ¸ĐŊŅĐžŅĐŧĐ°ŅĐ¸Ņ, ĐąŅĐ´Ņ ĐžŅŅĐžŅĐžĐļĐĩĐŊ</b>"
        ),
        "confidential_text": (
            "â ī¸ <b>ĐŖŅĐžĐ˛ĐĩĐŊŅ ĐģĐžĐŗĐžĐ˛</b> <code>{0}</code> <b>ĐŧĐžĐļĐĩŅ ŅĐžĐ´ĐĩŅĐļĐ°ŅŅ ĐģĐ¸ŅĐŊŅŅ"
            " Đ¸ĐŊŅĐžŅĐŧĐ°ŅĐ¸Ņ, ĐąŅĐ´Ņ ĐžŅŅĐžŅĐžĐļĐĩĐŊ</b>\n<b>ĐĐ°ĐŋĐ¸ŅĐ¸</b> <code>.logs {0}"
            " force_insecure</code><b>, ŅŅĐžĐąŅ ĐžŅĐŋŅĐ°Đ˛Đ¸ŅŅ ĐģĐžĐŗĐ¸ Đ¸ĐŗĐŊĐžŅĐ¸ŅŅŅ"
            " ĐŋŅĐĩĐ´ŅĐŋŅĐĩĐļĐ´ĐĩĐŊĐ¸Đĩ</b>"
        ),
        "choose_loglevel": "đââī¸ <b>ĐŅĐąĐĩŅĐ¸ ŅŅĐžĐ˛ĐĩĐŊŅ ĐģĐžĐŗĐžĐ˛</b>",
        "_cmd_doc_dump": "ĐĐžĐēĐ°ĐˇĐ°ŅŅ Đ¸ĐŊŅĐžŅĐŧĐ°ŅĐ¸Ņ Đž ŅĐžĐžĐąŅĐĩĐŊĐ¸Đ¸",
        "_cmd_doc_logs": (
            "<ŅŅĐžĐ˛ĐĩĐŊŅ> - ĐŅĐŋŅĐ°Đ˛ĐģŅĐĩŅ ĐģĐžĐŗ-ŅĐ°ĐšĐģ. ĐŖŅĐžĐ˛ĐŊĐ¸ ĐŊĐ¸ĐļĐĩ WARNING ĐŧĐžĐŗŅŅ ŅĐžĐ´ĐĩŅĐļĐ°ŅŅ"
            " ĐģĐ¸ŅĐŊŅŅ Đ¸ĐŊŅĐžĐŧŅĐ°ŅĐ¸Ņ."
        ),
        "_cmd_doc_suspend": "<Đ˛ŅĐĩĐŧŅ> - ĐĐ°ĐŧĐžŅĐžĐˇĐ¸ŅŅ ĐąĐžŅĐ° ĐŊĐ° ĐŊĐĩĐēĐžŅĐžŅĐžĐĩ Đ˛ŅĐĩĐŧŅ",
        "_cmd_doc_ping": "ĐŅĐžĐ˛ĐĩŅŅĐĩŅ ŅĐēĐžŅĐžŅŅŅ ĐžŅĐēĐģĐ¸ĐēĐ° ŅĐˇĐĩŅĐąĐžŅĐ°",
        "_cls_doc": "ĐĐŋĐĩŅĐ°ŅĐ¸Đ¸, ŅĐ˛ŅĐˇĐ°ĐŊĐŊŅĐĩ Ņ ŅĐ°ĐŧĐžŅĐĩŅŅĐ¸ŅĐžĐ˛Đ°ĐŊĐ¸ĐĩĐŧ",
        "send_anyway": "đ¤ ĐŅĐĩ ŅĐ°Đ˛ĐŊĐž ĐžŅĐŋŅĐ°Đ˛Đ¸ŅŅ",
        "cancel": "đĢ ĐŅĐŧĐĩĐŊĐ°",
        "logs_cleared": "đ <b>ĐĐžĐŗĐ¸ ĐžŅĐ¸ŅĐĩĐŊŅ</b>",
    }

    strings_fr = {
        "set_loglevel": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>SpÃŠcifiez le niveau de"
            " journalisation en nombre ou en chaÃŽne</b>"
        ),
        "no_logs": (
            "<emoji document_id=5363948200291998612>đ¤ˇââī¸</emoji> <b>Vous n'avez pas de"
            " journaux niveau</b> <code>{}</code><b>.</b>"
        ),
        "logs_caption": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>Journal Hikka niveau"
            "</b> <code>{}</code>\n\n<emoji document_id=6318902906900711458>âĒī¸</emoji>"
            " <b>Version: {}.{}.{}</b>{}"
        ),
        "debugging_enabled": (
            "<emoji document_id=5332533929020761310>â</emoji> <b>Mode dÃŠveloppeur"
            " activÃŠ pour le module</b> <code>{0}</code>\n<i>Allez dans le dossier"
            " `debug_modules`, modifier le fichier `{0}.py`, et voir les modifications"
            " en temps rÃŠel</i>"
        ),
        "debugging_disabled": (
            "<emoji document_id=5332533929020761310>â</emoji> <b>Mode dÃŠveloppeur"
            " dÃŠsactivÃŠ</b>"
        ),
        "suspend_invalid_time": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Temps de suspension"
            " invalide</b>"
        ),
        "suspended": (
            "<emoji document_id=5452023368054216810>đĨļ</emoji> <b>Le bot est suspendu"
            " pour</b> <code>{}</code> <b>secondes</b>"
        ),
        "results_ping": (
            "<emoji document_id=5431449001532594346>âĄī¸</emoji> <b>Vitesse de rÃŠponse"
            " Telegram:</b> <code>{}</code> <b>ms</b>\n<emoji"
            " document_id=5445284980978621387>đ</emoji> <b>PassÃŠ depuis la derniÃ¨re"
            " redÃŠmarrage: {}</b>"
        ),
        "ping_hint": (
            "<emoji document_id=5472146462362048818>đĄ</emoji> <i>La vitesse de rÃŠponse"
            " Telegram est en grande partie dÃŠpendante de la charge des serveurs"
            " Telegram et d'autres facteurs externes et n'a aucun rapport avec les"
            " paramÃ¨tres du serveur, sur lequel l'usagerbot est installÃŠ</i>"
        ),
        "confidential": (
            "â ī¸ <b>Niveau de journaux</b> <code>{}</code> <b>peut contenir des"
            " informations personnelles, soyez prudent</b>"
        ),
        "confidential_text": (
            "â ī¸ <b>Niveau de journaux</b> <code>{0}</code> <b>peut contenir des"
            " informations personnelles, soyez prudent</b>\n<b>Ecris</b> <code>.logs"
            " {0} force_insecure</code><b>, pour envoyer les journaux en ignorant"
            " l'avertissement</b>"
        ),
        "choose_loglevel": "đââī¸ <b>Choisissez le niveau de journaux</b>",
        "_cmd_doc_dump": "Afficher les informations du message",
        "_cmd_doc_logs": (
            "<niveau> - Envoyer le fichier journal. Les niveaux infÃŠrieurs Ã  WARNING"
            " peuvent contenir des informations personnelles."
        ),
        "_cmd_doc_suspend": (
            "<temps> - Mettre en pause l'utilisateurbot pendant un certain temps"
        ),
        "_cmd_doc_ping": "VÃŠrifie la vitesse de rÃŠponse de l'utilisateurbot",
        "_cls_doc": "OpÃŠrations liÃŠes Ã  l'auto-test",
        "send_anyway": "đ¤ Envoyer quand mÃĒme",
        "cancel": "đĢ Annuler",
        "logs_cleared": "đ <b>Les journaux ont ÃŠtÃŠ nettoyÃŠs</b>",
    }

    strings_it = {
        "set_loglevel": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Specifica il livello"
            " dei log</b>"
        ),
        "no_logs": (
            "<emoji document_id=5363948200291998612>đ¤ˇââī¸</emoji> <b>Non hai log"
            " di livello</b> <code>{}</code><b>.</b>"
        ),
        "logs_caption": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>Log di Hikka a livello"
            "</b> <code>{}</code>\n\n<emoji document_id=6318902906900711458>âĒī¸</emoji>"
            " <b>Versione: {}.{}.{}</b>{}"
        ),
        "debugging_enabled": (
            "<emoji document_id=5332533929020761310>â</emoji> <b>ModalitÃ  sviluppatore"
            " abilitata per il modulo</b> <code>{0}</code>\n<i>Vai nella cartella"
            " `debug_modules`, modifica il file `{0}.py`, e guarda i cambiamenti in"
            " tempo reale</i>"
        ),
        "debugging_disabled": (
            "<emoji document_id=5332533929020761310>â</emoji> <b>ModalitÃ  sviluppatore"
            " disabilitata</b>"
        ),
        "suspend_invalid_time": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Tempo di sospensione"
            " non valido</b>"
        ),
        "suspended": (
            "<emoji document_id=5452023368054216810>đĨļ</emoji> <b>Il bot Ã¨ stato sospeso"
            " per</b> <code>{}</code> <b>secondi</b>"
        ),
        "results_ping": (
            "<emoji document_id=5431449001532594346>âĄī¸</emoji> <b>VelocitÃ  di risposta"
            " di Telegram:</b> <code>{}</code> <b>ms</b>\n<emoji"
            " document_id=5445284980978621387>đ</emoji> <b>Tempo trascorso dalla"
            " ultima riavvio: {}</b>"
        ),
        "ping_hint": (
            "<emoji document_id=5472146462362048818>đĄ</emoji> <i>La velocitÃ  di"
            " risposta di Telegram dipende maggiormente dalla carica dei server di"
            " Telegram e da altri fattori esterni e non Ã¨ in alcun modo correlata ai"
            " parametri del server su cui Ã¨ installato lo UserBot</i>"
        ),
        "confidential": (
            "â ī¸ <b>Il livello di log</b> <code>{}</code> <b>puÃ˛ contenere informazioni"
            " personali, fai attenzione</b>"
        ),
        "confidential_text": (
            "â ī¸ <b>Il livello di log</b> <code>{0}</code> <b>puÃ˛ contenere informazioni"
            " personali, fai attenzione</b>\n<b>Scrivi</b> <code>.logs {0}"
            " force_insecure</code><b>, per inviare i log ignorando l'avviso</b>"
        ),
        "choose_loglevel": "đââī¸ <b>Scegli il livello di log</b>",
        "_cmd_doc_dump": "Mostra le informazioni sul messaggio",
        "_cmd_doc_logs": (
            "<livello> - Invia il file di log. I livelli inferiori a WARNING possono"
            " contenere informazioni personali."
        ),
        "_cmd_doc_suspend": "<tempo> - Ferma lo UserBot per un certo tempo",
        "_cmd_doc_ping": "Controlla la velocitÃ  di risposta dello UserBot",
        "_cls_doc": "Operazioni relative alle prove di autotest",
        "send_anyway": "đ¤ Invia comunque",
        "cancel": "đĢ Annulla",
        "logs_cleared": "đ <b>Log cancellati</b>",
    }

    strings_de = {
        "set_loglevel": (
            "đĢ <b>Geben Sie die Protokollebene als Zahl oder Zeichenfolge an</b>"
        ),
        "no_logs": (
            "<emoji document_id=5363948200291998612>đ¤ˇââī¸</emoji> <b>Du hast kein"
            " Protokollnachrichten des</b> <code>{}</code> <b>Ebene.</b>"
        ),
        "logs_caption": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>Hikka-Level-Protokolle"
            "</b> <code>{}</code>\n\n<emoji document_id=6318902906900711458>âĒī¸</emoji>"
            " <b>Version: {}.{}.{}</b>{}"
        ),
        "suspend_invalid_time": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Falsche Zeit"
            "einfrieren</b>"
        ),
        "suspended": (
            "<emoji document_id=5452023368054216810>đĨļ</emoji> <b>Bot ist"
            " eingefroren</b> <code>{}</code> <b>Sekunden</b>"
        ),
        "results_ping": (
            "<emoji document_id=5431449001532594346>âĄī¸</emoji> <b>Reaktionszeit des"
            " Telegram:</b> <code>{}</code> <b>ms</b>\n<emoji"
            " document_id=5445284980978621387>đ</emoji> <b>Zeit seit dem letzten"
            " Neustart: {}</b>"
        ),
        "ping_hint": (
            "<emoji document_id=5472146462362048818>đĄ</emoji> <i>ReaktionsfÃ¤higkeit"
            " Telegram ist stÃ¤rker abhÃ¤ngig von der Auslastung der Telegram-Server und"
            " Andere externe Faktoren und steht in keinem Zusammenhang mit den"
            " Servereinstellungen welcher Userbot installiert ist</i>"
        ),
        "confidential": (
            "â ī¸ <b>Protokollebene</b> <code>{}</code> <b>kann privat enthalten"
            "Informationen, seien Sie vorsichtig</b>"
        ),
        "confidential_text": (
            "â ī¸ <b>Protokollebene</b> <code>{0}</code> <b>kann privat"
            " enthaltenInformationen, seien Sie vorsichtig</b>\n<b>Schreiben Sie"
            "</b> <code>.logs {0} force_insecure</code> <b>um Protokolle zu"
            " ignorierenWarnung</b>"
        ),
        "choose_loglevel": "đââī¸ <b>WÃ¤hle eine Protokollebene</b>",
        "_cmd_doc_dump": "Nachrichteninformationen anzeigen",
        "_cmd_doc_logs": (
            "<Ebene> - Sendet eine Protokolldatei. Ebenen unterhalb von WARNUNG kÃļnnen"
            " enthaltenpersÃļnliche Informationen."
        ),
        "_cmd_doc_suspend": "<Zeit> - Bot fÃŧr eine Weile einfrieren",
        "_cmd_doc_ping": "ÃberprÃŧft die Antwortgeschwindigkeit des Userbots",
        "_cls_doc": "Selbsttestbezogene Operationen",
        "send_anyway": "đ¤ Trotzdem senden",
        "cancel": "đĢ Abbrechen",
        "logs_cleared": "đ <b>Protokolle gelÃļscht</b>",
    }

    strings_uz = {
        "set_loglevel": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Log darajasini raqam"
            " yoki satr sifatida ko'rsating</b>"
        ),
        "no_logs": (
            "<emoji document_id=5363948200291998612>đ¤ˇââī¸</emoji> <b>Siz"
            "</b> <code>{}</code> <b>darajadagi hech qanday loglaringiz yo'q.</b>"
        ),
        "logs_caption": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>Hikka Loglari"
            "</b> <code>{}</code>\n\n<emoji document_id=6318902906900711458>âĒī¸</emoji>"
            " <b>Versiyasi: {}.{}.{}</b>{}"
        ),
        "suspend_invalid_time": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Noto'g'ri vaqt"
            "qo'ymoq</b>"
        ),
        "suspended": (
            "<emoji document_id=5452023368054216810>đĨļ</emoji> <b>Bot chiqarildi</b>"
            " <code>{}</code> <b>Soniyalar</b>"
        ),
        "results_ping": (
            "<emoji document_id=5431449001532594346>âĄī¸</emoji> <b>Telegram tezligi:</b>"
            " <code>{}</code> <b>ms</b>\n<emoji"
            " document_id=5445284980978621387>đ</emoji> <b>SoĘģngi marotaba qayta ishga"
            " tushirilgan vaqti:</b> {}"
        ),
        "ping_hint": (
            "<emoji document_id=5472146462362048818>đĄ</emoji> <i>Telegram"
            " tezligi Telegram serverlarining ishga tushishi va boshqa tashqi"
            " faktorlariga bog'liq va Userbot o'rnatilgan serverlarining sozlamalari"
            " bilan bog'liq emas</i>"
        ),
        "confidential": (
            "â ī¸ <b>Log darajasi</b> <code>{}</code> <b>shaxsiy ma'lumotlarga ega"
            " bo'lishi mumkinO'zingizni xavfsizligi uchun</b>"
        ),
        "confidential_text": (
            "â ī¸ <b>Log darajasi</b> <code>{0}</code> <b>shaxsiy ma'lumotlarga ega"
            " bo'lishi mumkinO'zingizni xavfsizligi uchun</b>\n<b>Yozing"
            "</b> <code>.logs {0} force_insecure</code> <b>loglarniOgohlantirish</b>"
        ),
        "choose_loglevel": "đââī¸ <b>Log darajasini tanlang</b>",
        "_cmd_doc_dump": "Xabar haqida ma'lumotlarni ko'rsatish",
        "_cmd_doc_logs": (
            "<Ebene> - Log faylini yuboradi. O'rin darajalari xavfsizlikma'lumotlar."
        ),
        "_cmd_doc_suspend": "<Vaqt> - Botni bir necha vaqtga o'chirish",
        "_cmd_doc_ping": "Userbotning javob berish tezligini tekshirish",
        "_cls_doc": "O'z testi bilan bog'liq operatsiyalar",
        "send_anyway": "đ¤ Baribir yuborish",
        "cancel": "đĢ Bekor qilish",
        "logs_cleared": "đ <b>GÃŧnlÃŧkler temizlendi</b>",
    }

    strings_tr = {
        "set_loglevel": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>LÃŧtfen kayÄąt"
            " seviyesini sayÄą veya metin olarak belirtin</b>"
        ),
        "no_logs": (
            "<emoji document_id=5363948200291998612>đ¤ˇââī¸</emoji> <code>{}</code>"
            " <b>seviyesinde hiÃ§bir kayÄąt bulunmuyor.</b>"
        ),
        "logs_caption": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>Hikka KayÄątlarÄą"
            "</b> <code>{}</code>\n\n<emoji document_id=6318902906900711458>âĒī¸</emoji>"
            " <b>VersiyasÄą: {}.{}.{}</b>{}"
        ),
        "suspend_invalid_time": (
            "<emoji document_id=5416024721705673488>đ</emoji> <b>Durdurma iÃ§in geÃ§ersiz"
            " zaman girdiniz</b>"
        ),
        "suspended": (
            "<emoji document_id=5452023368054216810>đĨļ</emoji> <b>KullanÄącÄą botu</b>"
            " <code>{}</code> <b>saniyeliÄine durduruldu</b>"
        ),
        "results_ping": (
            "<emoji document_id=5431449001532594346>âĄī¸</emoji> <b>Telegram ping:</b>"
            " <code>{}</code> <b>ms</b>\n<emoji"
            " document_id=5445284980978621387>đ</emoji> <b>ÃalÄąÅma SÃŧresi:</b> {}"
        ),
        "ping_hint": (
            "<emoji document_id=5472146462362048818>đĄ</emoji> <i>Telegram pingi"
            " Ã§oÄunlukla Telegram sunucularÄąnÄąn gecikmesine ve diÄer dÄąÅ etkenlere"
            " baÄlÄądÄąr ve userbot'un kurulu olduÄu sunucunun parametreleriyle hiÃ§bir"
            " ilgisi yoktur.</i>"
        ),
        "confidential": (
            "â ī¸ <b>KayÄąt seviyesi</b> <code>{}</code> <b>gizli bilgilere sahip"
            " olabilir, kendi gÃŧvenliÄiniz iÃ§in dikkatli olun</b>"
        ),
        "confidential_text": (
            "â ī¸ <b>KayÄąt seviyesi</b> <code>{0}</code> <b>gizli bilgilere sahip"
            " olabilir, dikkatli olun. \n<b>Bu mesajÄą gÃļrmezden gelmek iÃ§in"
            "</b> <code>.logs {0} force_insecure</code> <b>yazÄąnÄąz</b>"
        ),
        "choose_loglevel": "đââī¸ <b>LÃŧtfen KayÄąt seviyesini seÃ§in</b>",
        "_cmd_doc_dump": "Mesaj hakkÄąnda bilgi gÃļster",
        "_cmd_doc_logs": "<Ebene> - KayÄąt dosyasÄąnÄą gÃļnderir. Seviyeler gizlibilgiler.",
        "_cmd_doc_suspend": "<Zaman> - Botu bir sÃŧreliÄine durdurun",
        "_cmd_doc_ping": "KullanÄącÄą botunun yanÄąt verme hÄązÄąnÄą kontrol edin",
        "_cls_doc": "Ä°lgili testlerle ilgili iÅlemler",
        "send_anyway": "đ¤ GÃļnder",
        "cancel": "đĢ Ä°ptal",
    }

    strings_es = {
        "set_loglevel": (
            "đĢ <b>Por favor, indique el nivel de registro como nÃēmero o cadena</b>"
        ),
        "no_logs": (
            "<emoji document_id=5363948200291998612>đ¤ˇââī¸</emoji> <b>No hay registros"
            "</b> <code>{}</code> <b>nivel.</b>"
        ),
        "logs_caption": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>Registros de"
            "</b> <code>{}</code>\n\n<emoji document_id=6318902906900711458>âĒī¸</emoji>"
            " <b>VersiÃŗn: {}.{}.{}</b>{}"
        ),
        "suspend_invalid_time": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Has introducido un"
            " tiempo no vÃĄlido</b>"
        ),
        "suspended": (
            "<emoji document_id=5452023368054216810>đĨļ</emoji> <b>Bot suspendido</b>"
            " <code>{}</code> <b>segundos</b>"
        ),
        "results_ping": (
            "<emoji document_id=5431449001532594346>âĄī¸</emoji> <b>Retraso del"
            " Telegram:</b> <code>{}</code> <b>ms</b>\n<emoji"
            " document_id=5445284980978621387>đ</emoji> <b>Desde la Ãēltima"
            " actualizaciÃŗn:</b> {}"
        ),
        "ping_hint": (
            "<emoji document_id=5472146462362048818>đĄ</emoji> <i>La velocidad de"
            " Telegram depende de la inicializaciÃŗn de los servidores de Telegram y"
            " otros factores externosy no de la configuraciÃŗn de su servidor de"
            " Userbot</i>"
        ),
        "confidential": (
            "â ī¸ <b>Nivel de registro</b> <code>{}</code> <b>puede contener informaciÃŗn"
            " confidencial asegÃērate de proteger tu privacidad</b>"
        ),
        "confidential_text": (
            "â ī¸ <b>Nivel de registro</b> <code>{0}</code> <b>puede contener informaciÃŗn"
            " confidencial asegÃērate de proteger tu privacidad</b>\n<b>Escribe"
            "</b> <code>.logs {0} force_insecure</code> <b>para enviar los"
            " registros</b>"
        ),
        "choose_loglevel": "đââī¸ <b>Por favor, elige el nivel de registro</b>",
        "_cmd_doc_dump": "Muestra informaciÃŗn sobre el mensaje",
        "_cmd_doc_logs": (
            "<Nivel> - EnvÃ­a el archivo de registro. Los niveles confidenciales"
            "pueden contener informaciÃŗn confidencial"
        ),
        "_cmd_doc_suspend": "<Tiempo> - Suspende el bot durante un tiempo",
        "_cmd_doc_ping": "Comprueba la velocidad de respuesta de su Userbot",
        "_cls_doc": "Procesos relacionados con los tests",
        "send_anyway": "đ¤ Enviar de todos modos",
        "cancel": "đĢ Cancelar",
        "logs_cleared": "đ <b>Registros borrados</b>",
    }

    strings_kk = {
        "set_loglevel": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĐžĐŗ ŅŌ¯ŅŅĐŊ ŅĐ°ĐŊ ĐŊĐĩĐŧĐĩŅĐĩ"
            " ĐļĐžĐģĐŧĐĩĐŊ ĐĩĐŊĐŗŅĐˇŅŌŖŅĐˇ</b>"
        ),
        "no_logs": (
            "<emoji document_id=5363948200291998612>đ¤ˇââī¸</emoji> <b>ĐĄŅĐˇĐ´Đĩ"
            "</b> <code>{}</code> <b>Đ´ĐĩŌŖĐŗĐĩĐšŅĐŊĐ´ĐĩĐŗŅ ĐģĐžĐŗ ĐļĐžŌ.</b>"
        ),
        "logs_caption": (
            "<emoji document_id=5188377234380954537>đ</emoji> <b>Hikka ĐģĐžĐŗŅĐ°ŅŅĐŊŅŌŖ"
            " Đ´ĐĩŌŖĐŗĐĩĐšŅ</b> <code>{}</code>\n\n<emoji"
            " document_id=6318902906900711458>âĒī¸</emoji> <b>ĐŌąŅŌĐ°ŅŅ: {}.{}.{}</b>{}"
        ),
        "debugging_enabled": (
            "<emoji document_id=5332533929020761310>â</emoji> <b>ĐĐžĐ´ŅĐģŅ"
            "</b> <code>{0}</code> <b>Ō¯ŅŅĐŊ Đ´ĐĩĐąĐ°Đŗ ŅĐĩĐļĐ¸ĐŧŅ ŌĐžŅŅĐģĐ´Ņ</b>\n<i>`debug_modules`"
            " Đ´Đ¸ŅĐĩĐēŅĐžŅĐ¸ŅŅŅĐŊĐ° ĶŠŅŅŅŌŖŅĐˇ ĐēĐĩŅĐĩĐē, ŅĐ°ĐšĐģĐ´Ņ ĶŠĐˇĐŗĐĩŅŅŅŌŖŅĐˇ, ĶŅĐąŅŅ ĶŠĐˇĐŗĐĩŅŅŅŅŅ Đ°ĐģĐ´ŅĐŊ"
            " Đ°ĐģĐ° ŌĐ°ŅĐ°ŌŖŅĐˇ</i>"
        ),
        "debugging_disabled": (
            "<emoji document_id=5332533929020761310>â</emoji> <b>ĐĐĩĐąĐ°Đŗ ŅĐĩĐļĐ¸ĐŧŅ"
            " ĶŠŅŅŅŅĐģĐ´Ņ</b>"
        ),
        "suspend_invalid_time": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĐ°ŅĐ°ĐŧŅŅĐˇ ŅĐ°ŌŅŅ</b>"
        ),
        "suspended": (
            "<emoji document_id=5452023368054216810>đĨļ</emoji> <b>ĐĐžŅ"
            "</b> <code>{}</code> <b>ŅĐĩĐēŅĐŊĐ´ ŌŌąĐģŅĐŋŅĐ°ĐģĐ´Ņ</b>"
        ),
        "results_ping": (
            "<emoji document_id=5431449001532594346>âĄī¸</emoji> <b>Telegram ĐļĐ°ŅĐ°Đŋ ĐąĐĩŅŅ"
            " ŅĐ°ŌŅŅŅ:</b> <code>{}</code> <b>ĐŧŅ</b>\n<emoji"
            " document_id=5445284980978621387>đ</emoji> <b>ĐĄĐžŌŖŌŅ ŅĐĩŅŅĐ°ŅŅŅĐ°ĐŊ ĐąŌąŅŅĐŊ"
            " ŅĐ°ŌŅŅŅ: {}</b>"
        ),
        "ping_hint": (
            "<emoji document_id=5472146462362048818>đĄ</emoji> <i>Telegram ĐļĐ°ŅĐ°Đŋ"
            " ĐąĐĩŅŅ ŅĐ°ŌŅŅŅ ŅĐĩŅĐ˛ĐĩŅĐģĐĩŅĐ´ŅŌŖ ĐļŌ¯ĐšĐĩĐģŅĐŗŅ ĐŧĐĩĐŊ ĐąĐ°ŅŌĐ° ŅŅŅŅŌŅ ĶŅĐĩŅĐģĐĩŅĐŗĐĩ ŌĐ°ŅŅŅ"
            " ĶŠĐˇĐŗĐĩŅĐĩĐ´Ņ ĐļĶĐŊĐĩ ŅĐĩŅĐ˛ĐĩŅŅŌŖŅĐˇĐŗĐĩ ŌĐ°ĐŊŅĐ° ĐļĐ°ŌŅĐ°ŅŅŅĐģŌĐ°ĐŊŅĐŧĐĩĐŊ ŌĐ°ŅĐ°ŅŅĐŊ ĐąĐžĐģĐŧĐ°ĐšĐ´Ņ</i>"
        ),
        "confidential": (
            "â ī¸ <b>ĐĐžĐŗ ŅŌ¯ŅŅ</b> <code>{}</code> <b>ŅŅĐˇĐ´ŅŌŖ ĐļĐĩĐēĐĩ ĐŧĶĐģŅĐŧĐĩŅŅŌŖŅĐˇĐŗĐĩ ŌĐ°ŅŅŅŅŅ"
            " ĐąĐžĐģŅŅ ĐŧŌ¯ĐŧĐēŅĐŊ, ŅĐĩĐŊŅĐŧĐ´Ņ ĐąĐžĐģŅŌŖŅĐˇ</b>"
        ),
        "confidential_text": (
            "â ī¸ <b>ĐĐžĐŗ ŅŌ¯ŅŅ</b> <code>{0}</code> <b>ŅŅĐˇĐ´ŅŌŖ ĐļĐĩĐēĐĩ ĐŧĶĐģŅĐŧĐĩŅŅŌŖŅĐˇĐŗĐĩ ŌĐ°ŅŅŅŅŅ"
            " ĐąĐžĐģŅŅ ĐŧŌ¯ĐŧĐēŅĐŊ, ŅĐĩĐŊŅĐŧĐ´Ņ ĐąĐžĐģŅŌŖŅĐˇ</b>\n<b>ĐĐžĐģĐ´Đ°ĐŊ</b> <code>.logs {0}"
            " force_insecure</code><b>, ĐēĐĩĐģĐĩŅŅ ŅĐ¸ŅŌŅŅŌ ĐąĐžĐšŅĐŊŅĐ° ĐģĐžĐŗŅĐ°ŅĐ´Ņ ĐļŅĐąĐĩŅŅ"
            " Ō¯ŅŅĐŊ ŅĐĩĐŊŅĐŧĐ´Ņ ĐąĐžĐģŅŌŖŅĐˇ</b>"
        ),
        "choose_loglevel": "đââī¸ <b>ĐĐžĐŗ ŅŌ¯ŅŅĐŊ ŅĐ°ŌŖĐ´Đ°ŌŖŅĐˇ</b>",
        "_cmd_doc_dump": "ĐĨĐ°ĐąĐ°ŅĐģĐ°ĐŧĐ° ŅŅŅĐ°ĐģŅ Đ°ŌĐŋĐ°ŅĐ°ŅŅŅ ĐēĶŠŅŅĐĩŅŅ",
        "_cmd_doc_logs": (
            "<ŅŌ¯Ņ> - ĐĐžĐŗ ŅĐ°ĐšĐģŅĐŊ ĐļŅĐąĐĩŅŅ. WARNING ŅŌ¯ŅŅĐŊĐĩĐŊ ĐēĐĩĐšŅĐŊĐŗŅ ŅŌ¯ŅĐģĐĩŅ ŅŅĐˇĐ´ŅŌŖ"
            " ĐļĐĩĐēĐĩ ĐŧĶĐģŅĐŧĐĩŅŅŌŖŅĐˇĐŗĐĩ ŌĐ°ŅŅŅŅŅ ĐąĐžĐģŅŅ ĐŧŌ¯ĐŧĐēŅĐŊ."
        ),
        "_cmd_doc_suspend": "<ŅĐ°ŌŅŅ> - ĐĐžŅŅŅ ĐąŅŅĐŊĐĩŅĐĩ ŅĐ°ŌŅŅ ŌĐžĐšŅĐŋ ŌĐ°ĐģĐ´ŅŅŅ",
        "_cmd_doc_ping": "ĐŽĐˇĐĩŅĐąĐžŅŅŅŌŖ ĐļĐ°ŅĐ°Đŋ ĐąĐĩŅŅ ŅĐ°ŌŅŅŅĐŊ ŅĐĩĐēŅĐĩŅŅ",
        "_cls_doc": "Ķ¨ĐˇĐ´ŅĐēŅŅĐē ŅŅĐŊĐ°ŅŌĐ° ŌĐ°ŅŅŅŅŅ ĶŅĐĩĐēĐĩŅŅĐĩŅ",
        "send_anyway": "đ¤ ĐŅĐąĐĩŅŅ",
        "cancel": "đĢ ĐĐžĐģĐ´ŅŅĐŧĐ°Ņ",
        "logs_cleared": "đ <b>ĐĐžĐŗŅĐ°Ņ ŅĐ°ĐˇĐ°ŅŅŅĐģĐ´Ņ</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "force_send_all",
                False,
                "â ī¸ Do not touch, if you don't know what it does!\nBy default, Hikka"
                " will try to determine, which client caused logs. E.g. there is a"
                " module TestModule installed on Client1 and TestModule2 on Client2. By"
                " default, Client2 will get logs from TestModule2, and Client1 will get"
                " logs from TestModule. If this option is enabled, Hikka will send all"
                " logs to Client1 and Client2, even if it is not the one that caused"
                " the log.",
                validator=loader.validators.Boolean(),
                on_change=self._pass_config_to_logger,
            ),
            loader.ConfigValue(
                "tglog_level",
                "INFO",
                "â ī¸ Do not touch, if you don't know what it does!\n"
                "Minimal loglevel for records to be sent in Telegram.",
                validator=loader.validators.Choice(
                    ["INFO", "WARNING", "ERROR", "CRITICAL"]
                ),
                on_change=self._pass_config_to_logger,
            ),
        )

    def _pass_config_to_logger(self):
        logging.getLogger().handlers[0].force_send_all = self.config["force_send_all"]
        logging.getLogger().handlers[0].tg_level = {
            "INFO": 20,
            "WARNING": 30,
            "ERROR": 40,
            "CRITICAL": 50,
        }[self.config["tglog_level"]]

    @loader.command(
        ru_doc="ĐŅĐ˛ĐĩŅŅ ĐŊĐ° ŅĐžĐžĐąŅĐĩĐŊĐ¸Đĩ, ŅŅĐžĐąŅ ĐŋĐžĐēĐ°ĐˇĐ°ŅŅ ĐĩĐŗĐž Đ´Đ°ĐŧĐŋ",
        fr_doc="RÃŠpondre au message pour montrer sa dÃŠcharge",
        it_doc="Rispondi al messaggio per mostrare il suo dump",
        de_doc="Antworten Sie auf eine Nachricht, um ihren Dump anzuzeigen",
        tr_doc="DÃļkÃŧmÃŧnÃŧ gÃļstermek iÃ§in bir iletiyi yanÄątlayÄąn",
        uz_doc="Xabarning axlatini ko'rsatish uchun unga javob bering",
        es_doc="Responde a un mensaje para mostrar su volcado",
        kk_doc="ĐĐ°ĐŧĐŋŅĐŊ ĐēĶŠŅŅĐĩŅŅ Ō¯ŅŅĐŊ ŅĐ°ĐąĐ°ŅĐģĐ°ĐŧĐ°ŌĐ° ĐļĐ°ŅĐ°Đŋ ĐąĐĩŅŅŌŖŅĐˇ",
    )
    async def dump(self, message: Message):
        """Use in reply to get a dump of a message"""
        if not message.is_reply:
            return

        await utils.answer(
            message,
            "<code>"
            + utils.escape_html((await message.get_reply_message()).stringify())
            + "</code>",
        )

    @loader.command(
        ru_doc="ĐŅĐ¸ŅŅĐ¸ŅŅ ĐģĐžĐŗĐ¸",
        fr_doc="Effacer les journaux",
        it_doc="Cancella i log",
        de_doc="Logs lÃļschen",
        tr_doc="GÃŧnlÃŧkleri temizle",
        uz_doc="Jurnalni tozalash",
        es_doc="Limpiar registros",
        kk_doc="ĐĐžĐŗŅĐ°ŅĐ´Ņ ŅĐ°ĐˇĐ°ĐģĐ°Ņ",
    )
    async def clearlogs(self, message: Message):
        """Clear logs"""
        for handler in logging.getLogger().handlers:
            handler.buffer = []
            handler.handledbuffer = []
            handler.tg_buff = ""

        await utils.answer(message, self.strings("logs_cleared"))

    @loader.loop(interval=1, autostart=True)
    async def watchdog(self):
        if not os.path.isdir(DEBUG_MODS_DIR):
            return

        try:
            for module in os.scandir(DEBUG_MODS_DIR):
                last_modified = os.stat(module.path).st_mtime
                cls_ = module.path.split("/")[-1].split(".py")[0]

                if cls_ not in self._memory:
                    self._memory[cls_] = last_modified
                    continue

                if self._memory[cls_] == last_modified:
                    continue

                self._memory[cls_] = last_modified
                logger.debug("Reloading debug module %s", cls_)
                with open(module.path, "r") as f:
                    try:
                        await next(
                            module
                            for module in self.allmodules.modules
                            if module.__class__.__name__ == "LoaderMod"
                        ).load_module(
                            f.read(),
                            None,
                            save_fs=False,
                        )
                    except Exception:
                        logger.exception("Failed to reload module in watchdog")
        except Exception:
            logger.exception("Failed debugging watchdog")
            return

    @loader.command()
    async def debugmod(self, message: Message):
        """[module] - For developers: Open module for debugging
        You will be able to track changes in real-time"""
        args = utils.get_args_raw(message)
        instance = None
        for module in self.allmodules.modules:
            if (
                module.__class__.__name__.lower() == args.lower()
                or module.strings["name"].lower() == args.lower()
            ):
                if os.path.isfile(
                    os.path.join(
                        DEBUG_MODS_DIR,
                        f"{module.__class__.__name__}.py",
                    )
                ):
                    os.remove(
                        os.path.join(
                            DEBUG_MODS_DIR,
                            f"{module.__class__.__name__}.py",
                        )
                    )

                    try:
                        delattr(module, "hikka_debug")
                    except AttributeError:
                        pass

                    await utils.answer(message, self.strings("debugging_disabled"))
                    return

                module.hikka_debug = True
                instance = module
                break

        if not instance:
            await utils.answer(message, self.strings("bad_module"))
            return

        with open(
            os.path.join(
                DEBUG_MODS_DIR,
                f"{instance.__class__.__name__}.py",
            ),
            "wb",
        ) as f:
            f.write(inspect.getmodule(instance).__loader__.data)

        await utils.answer(
            message,
            self.strings("debugging_enabled").format(instance.__class__.__name__),
        )

    @loader.command(
        ru_doc="<ŅŅĐžĐ˛ĐĩĐŊŅ> - ĐĐžĐēĐ°ĐˇĐ°ŅŅ ĐģĐžĐŗĐ¸",
        fr_doc="<niveau> - Afficher les journaux",
        it_doc="<livello> - Mostra i log",
        de_doc="<Level> - Zeige Logs",
        uz_doc="<daraja> - Loglarni ko'rsatish",
        tr_doc="<seviye> - GÃŧnlÃŧkleri gÃļster",
        es_doc="<nivel> - Mostrar registros",
        kk_doc="<Đ´ĐĩŌŖĐŗĐĩĐš> - ĐĐžĐŗŅĐ°ŅĐ´Ņ ĐēĶŠŅŅĐĩŅŅ",
    )
    async def logs(
        self,
        message: typing.Union[Message, InlineCall],
        force: bool = False,
        lvl: typing.Union[int, None] = None,
    ):
        """<level> - Dump logs"""
        if not isinstance(lvl, int):
            args = utils.get_args_raw(message)
            try:
                try:
                    lvl = int(args.split()[0])
                except ValueError:
                    lvl = getattr(logging, args.split()[0].upper(), None)
            except IndexError:
                lvl = None

        if not isinstance(lvl, int):
            try:
                if not self.inline.init_complete or not await self.inline.form(
                    text=self.strings("choose_loglevel"),
                    reply_markup=utils.chunks(
                        [
                            {
                                "text": name,
                                "callback": self.logs,
                                "args": (False, level),
                            }
                            for name, level in [
                                ("đĢ Error", 40),
                                ("â ī¸ Warning", 30),
                                ("âšī¸ Info", 20),
                                ("đ§âđģ All", 0),
                            ]
                        ],
                        2,
                    )
                    + [[{"text": self.strings("cancel"), "action": "close"}]],
                    message=message,
                ):
                    raise
            except Exception:
                await utils.answer(message, self.strings("set_loglevel"))

            return

        logs = "\n\n".join(
            [
                "\n".join(
                    handler.dumps(lvl, client_id=self._client.tg_id)
                    if "client_id" in inspect.signature(handler.dumps).parameters
                    else handler.dumps(lvl)
                )
                for handler in logging.getLogger().handlers
            ]
        )

        named_lvl = (
            lvl
            if lvl not in logging._levelToName
            else logging._levelToName[lvl]  # skipcq: PYL-W0212
        )

        if (
            lvl < logging.WARNING
            and not force
            and (
                not isinstance(message, Message)
                or "force_insecure" not in message.raw_text.lower()
            )
        ):
            try:
                if not self.inline.init_complete:
                    raise

                cfg = {
                    "text": self.strings("confidential").format(named_lvl),
                    "reply_markup": [
                        {
                            "text": self.strings("send_anyway"),
                            "callback": self.logs,
                            "args": [True, lvl],
                        },
                        {"text": self.strings("cancel"), "action": "close"},
                    ],
                }
                if isinstance(message, Message):
                    if not await self.inline.form(**cfg, message=message):
                        raise
                else:
                    await message.edit(**cfg)
            except Exception:
                await utils.answer(
                    message,
                    self.strings("confidential_text").format(named_lvl),
                )

            return

        if len(logs) <= 2:
            if isinstance(message, Message):
                await utils.answer(message, self.strings("no_logs").format(named_lvl))
            else:
                await message.edit(self.strings("no_logs").format(named_lvl))
                await message.unload()

            return

        logs = self.lookup("python").censor(logs)

        logs = BytesIO(logs.encode("utf-16"))
        logs.name = "hikka-logs.txt"

        ghash = utils.get_git_hash()

        other = (
            *main.__version__,
            (
                " <a"
                f' href="https://github.com/hikariatama/Hikka/commit/{ghash}">@{ghash[:8]}</a>'
                if ghash
                else ""
            ),
        )

        if getattr(message, "out", True):
            await message.delete()

        if isinstance(message, Message):
            await utils.answer(
                message,
                logs,
                caption=self.strings("logs_caption").format(named_lvl, *other),
            )
        else:
            await self._client.send_file(
                message.form["chat"],
                logs,
                caption=self.strings("logs_caption").format(named_lvl, *other),
                reply_to=message.form["top_msg_id"],
            )

    @loader.owner
    @loader.command(
        ru_doc="<Đ˛ŅĐĩĐŧŅ> - ĐĐ°ĐŧĐžŅĐžĐˇĐ¸ŅŅ ĐąĐžŅĐ° ĐŊĐ° N ŅĐĩĐēŅĐŊĐ´",
        fr_doc="<temps> - Congeler le bot pendant N secondes",
        it_doc="<tempo> - Congela il bot per N secondi",
        de_doc="<Zeit> - Stoppe den Bot fÃŧr N Sekunden",
        tr_doc="<sÃŧre> - Botu N saniye boyunca durdur",
        uz_doc="<vaqt> - Botni N soniya davomida to'xtatish",
        es_doc="<tiempo> - Congela el bot durante N segundos",
        kk_doc="<ŅĐ°ŌŅŅ> - ĐĐžŅŅŅ N ŅĐĩĐēŅĐŊĐ´ ŌąĐˇĐ°ŌŅŅŌŅĐŊĐ´Đ° ŅŌąĐˇĐ°ŅŅĐŋ ŌĐžĐš",
    )
    async def suspend(self, message: Message):
        """<time> - Suspends the bot for N seconds"""
        try:
            time_sleep = float(utils.get_args_raw(message))
            await utils.answer(
                message,
                self.strings("suspended").format(time_sleep),
            )
            time.sleep(time_sleep)
        except ValueError:
            await utils.answer(message, self.strings("suspend_invalid_time"))

    @loader.command(
        ru_doc="ĐŅĐžĐ˛ĐĩŅĐ¸ŅŅ ŅĐēĐžŅĐžŅŅŅ ĐžŅĐēĐģĐ¸ĐēĐ° ŅĐˇĐĩŅĐąĐžŅĐ°",
        fr_doc="VÃŠrifiez la vitesse de rÃŠponse du bot utilisateur",
        it_doc="Controlla la velocitÃ  di risposta del userbot",
        de_doc="ÃberprÃŧfe die Antwortgeschwindigkeit des Userbots",
        tr_doc="KullanÄącÄą botunun yanÄąt hÄązÄąnÄą kontrol edin",
        uz_doc="Foydalanuvchi botining javob tezligini tekshiring",
        es_doc="Comprueba la velocidad de respuesta del bot de usuario",
        kk_doc="ŌĐžĐģĐ´Đ°ĐŊŅŅŅ ĐąĐžŅŅĐŊŅŌŖ ĐļĐ°ŅĐ°Đŋ ŅŅŌŅ ŅĐ°ŌŅŅŅĐŊ ŅĐĩĐēŅĐĩŅŅ",
    )
    async def ping(self, message: Message):
        """Test your userbot ping"""
        start = time.perf_counter_ns()
        message = await utils.answer(message, "đ")

        await utils.answer(
            message,
            self.strings("results_ping").format(
                round((time.perf_counter_ns() - start) / 10**6, 3),
                utils.formatted_uptime(),
            )
            + (
                ("\n\n" + self.strings("ping_hint"))
                if random.choice([0, 0, 1]) == 1
                else ""
            ),
        )

    async def client_ready(self):
        chat, _ = await utils.asset_channel(
            self._client,
            "hikka-logs",
            "đ Your Hikka logs will appear in this chat",
            silent=True,
            invite_bot=True,
            avatar="https://github.com/hikariatama/assets/raw/master/hikka-logs.png",
        )

        self._logchat = int(f"-100{chat.id}")

        logging.getLogger().handlers[0].install_tg_log(self)
        logger.debug("Bot logging installed for %s", self._logchat)

        self._pass_config_to_logger()
