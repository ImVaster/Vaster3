# ÂŠī¸ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# đ https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# đ https://www.gnu.org/licenses/agpl-3.0.html

import pyrogram
import telethon
from telethon.extensions.html import CUSTOM_EMOJIS
from telethon.tl.types import Message

from .. import loader, main, utils, version
from ..compat.dragon import DRAGON_EMOJI
from ..inline.types import InlineCall


@loader.tds
class CoreMod(loader.Module):
    """Control core userbot settings"""

    strings = {
        "name": "Settings",
        "too_many_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Too many args</b>"
        ),
        "blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Chat {} blacklisted"
            " from userbot</b>"
        ),
        "unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Chat {}"
            " unblacklisted from userbot</b>"
        ),
        "user_blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>User {} blacklisted"
            " from userbot</b>"
        ),
        "user_unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>User {}"
            " unblacklisted from userbot</b>"
        ),
        "what_prefix": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>What should the prefix"
            " be set to?</b>"
        ),
        "prefix_incorrect": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Prefix must be one"
            " symbol in length</b>"
        ),
        "prefix_set": (
            "{} <b>Command prefix"
            " updated. Type</b> <code>{newprefix}setprefix {oldprefix}</code> <b>to"
            " change it back</b>"
        ),
        "alias_created": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Alias created."
            " Access it with</b> <code>{}</code>"
        ),
        "aliases": "<b>đ Aliases:</b>\n",
        "no_command": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Command</b>"
            " <code>{}</code> <b>does not exist</b>"
        ),
        "alias_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>You must provide a"
            " command and the alias for it</b>"
        ),
        "delalias_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>You must provide the"
            " alias name</b>"
        ),
        "alias_removed": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Alias</b>"
            " <code>{}</code> <b>removed</b>."
        ),
        "no_alias": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Alias</b>"
            " <code>{}</code> <b>does not exist</b>"
        ),
        "db_cleared": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Database cleared</b>"
        ),
        "hikka": (
            "{} <b>{}.{}.{}</b> <i>{}</i>\n\n<b><emoji"
            " document_id=5377437404078546699>đ</emoji> <b>Hikka-TL:"
            "</b> <i>{}</i>\n{}"
            " <b>Hikka-Pyro:</b> <i>{}</i>\n\n<emoji"
            " document_id=5454182070156794055>â¨ī¸</emoji> <b>Developer:"
            " t.me/hikariatama</b>"
        ),
        "confirm_cleardb": "â ī¸ <b>Are you sure, that you want to clear database?</b>",
        "cleardb_confirm": "đ Clear database",
        "cancel": "đĢ Cancel",
        "who_to_blacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>Who to blacklist?</b>"
        ),
        "who_to_unblacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>Who to"
            " unblacklist?</b>"
        ),
        "unstable": (
            "\n\n<emoji document_id=5467370583282950466>đ</emoji> <b>You are using an"
            " unstable branch</b> <code>{}</code><b>!</b>"
        ),
        "prefix_collision": (
            "<emoji document_id=5469654973308476699>đŖ</emoji> <b>Your Dragon and Hikka"
            " prefixes must be different!</b>"
        ),
    }

    strings_ru = {
        "too_many_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĄĐģĐ¸ŅĐēĐžĐŧ ĐŧĐŊĐžĐŗĐž"
            " Đ°ŅĐŗŅĐŧĐĩĐŊŅĐžĐ˛</b>"
        ),
        "blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Đ§Đ°Ņ {} Đ´ĐžĐąĐ°Đ˛ĐģĐĩĐŊ Đ˛"
            " ŅĐĩŅĐŊŅĐš ŅĐŋĐ¸ŅĐžĐē ŅĐˇĐĩŅĐąĐžŅĐ°</b>"
        ),
        "unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Đ§Đ°Ņ {} ŅĐ´Đ°ĐģĐĩĐŊ Đ¸Đˇ"
            " ŅĐĩŅĐŊĐžĐŗĐž ŅĐŋĐ¸ŅĐēĐ° ŅĐˇĐĩŅĐąĐžŅĐ°</b>"
        ),
        "user_blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>ĐĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģŅ {}"
            " Đ´ĐžĐąĐ°Đ˛ĐģĐĩĐŊ Đ˛ ŅĐĩŅĐŊŅĐš ŅĐŋĐ¸ŅĐžĐē ŅĐˇĐĩŅĐąĐžŅĐ°</b>"
        ),
        "user_unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>ĐĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģŅ {}"
            " ŅĐ´Đ°ĐģĐĩĐŊ Đ¸Đˇ ŅĐĩŅĐŊĐžĐŗĐž ŅĐŋĐ¸ŅĐēĐ° ŅĐˇĐĩŅĐąĐžŅĐ°</b>"
        ),
        "what_prefix": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>Đ ĐēĐ°ĐēĐžĐš ĐŋŅĐĩŅĐ¸ĐēŅ"
            " ŅŅĐ°Đ˛Đ¸ŅŅ ŅĐž?</b>"
        ),
        "prefix_incorrect": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐŅĐĩŅĐ¸ĐēŅ Đ´ĐžĐģĐļĐĩĐŊ"
            " ŅĐžŅŅĐžŅŅŅ ŅĐžĐģŅĐēĐž Đ¸Đˇ ĐžĐ´ĐŊĐžĐŗĐž ŅĐ¸ĐŧĐ˛ĐžĐģĐ°</b>"
        ),
        "prefix_set": (
            "{} <b>ĐŅĐĩŅĐ¸ĐēŅ ĐžĐąĐŊĐžĐ˛ĐģĐĩĐŊ."
            " Đ§ŅĐžĐąŅ Đ˛ĐĩŅĐŊŅŅŅ ĐĩĐŗĐž, Đ¸ŅĐŋĐžĐģŅĐˇŅĐš</b> <code>{newprefix}setprefix"
            " {oldprefix}</code>"
        ),
        "alias_created": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>ĐĐģĐ¸Đ°Ņ ŅĐžĐˇĐ´Đ°ĐŊ."
            " ĐŅĐŋĐžĐģŅĐˇŅĐš ĐĩĐŗĐž ŅĐĩŅĐĩĐˇ</b> <code>{}</code>"
        ),
        "aliases": "<b>đ ĐĐģĐ¸Đ°ŅŅ:</b>\n",
        "no_command": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĐžĐŧĐ°ĐŊĐ´Đ°</b>"
            " <code>{}</code> <b>ĐŊĐĩ ŅŅŅĐĩŅŅĐ˛ŅĐĩŅ</b>"
        ),
        "alias_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĸŅĐĩĐąŅĐĩŅŅŅ Đ˛Đ˛ĐĩŅŅĐ¸"
            " ĐēĐžĐŧĐ°ĐŊĐ´Ņ Đ¸ Đ°ĐģĐ¸Đ°Ņ Đ´ĐģŅ ĐŊĐĩĐĩ</b>"
        ),
        "delalias_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĸŅĐĩĐąŅĐĩŅŅŅ Đ¸ĐŧŅ"
            " Đ°ĐģĐ¸Đ°ŅĐ°</b>"
        ),
        "alias_removed": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>ĐĐģĐ¸Đ°Ņ</b>"
            " <code>{}</code> <b>ŅĐ´Đ°ĐģĐĩĐŊ</b>."
        ),
        "no_alias": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĐģĐ¸Đ°Ņ</b>"
            " <code>{}</code> <b>ĐŊĐĩ ŅŅŅĐĩŅŅĐ˛ŅĐĩŅ</b>"
        ),
        "db_cleared": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>ĐĐ°ĐˇĐ° ĐžŅĐ¸ŅĐĩĐŊĐ°</b>"
        ),
        "hikka": (
            "{} <b>{}.{}.{}</b> <i>{}</i>\n\n<b><emoji"
            " document_id=5377437404078546699>đ</emoji> <b>Hikka-TL:"
            "</b> <i>{}</i>\n{}"
            " <b>Hikka-Pyro:</b> <i>{}</i>\n\n<emoji"
            " document_id=5454182070156794055>â¨ī¸</emoji> <b>Developer:"
            " t.me/hikariatama</b>"
        ),
        "_cls_doc": "ĐŖĐŋŅĐ°Đ˛ĐģĐĩĐŊĐ¸Đĩ ĐąĐ°ĐˇĐžĐ˛ŅĐŧĐ¸ ĐŊĐ°ŅŅŅĐžĐšĐēĐ°ĐŧĐ¸ ŅĐˇĐĩŅĐąĐžŅĐ°",
        "confirm_cleardb": "â ī¸ <b>ĐŅ ŅĐ˛ĐĩŅĐĩĐŊŅ, ŅŅĐž ŅĐžŅĐ¸ŅĐĩ ŅĐąŅĐžŅĐ¸ŅŅ ĐąĐ°ĐˇŅ Đ´Đ°ĐŊĐŊŅŅ?</b>",
        "cleardb_confirm": "đ ĐŅĐ¸ŅŅĐ¸ŅŅ ĐąĐ°ĐˇŅ",
        "cancel": "đĢ ĐŅĐŧĐĩĐŊĐ°",
        "who_to_blacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>ĐĐžĐŗĐž ĐˇĐ°ĐąĐģĐžĐēĐ¸ŅĐžĐ˛Đ°ŅŅ"
            " ŅĐž?</b>"
        ),
        "who_to_unblacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>ĐĐžĐŗĐž ŅĐ°ĐˇĐąĐģĐžĐēĐ¸ŅĐžĐ˛Đ°ŅŅ"
            " ŅĐž?</b>"
        ),
        "unstable": (
            "\n\n<emoji document_id=5467370583282950466>đ</emoji> <b>ĐĸŅ Đ¸ŅĐŋĐžĐģŅĐˇŅĐĩŅŅ"
            " ĐŊĐĩŅŅĐ°ĐąĐ¸ĐģŅĐŊŅŅ Đ˛ĐĩŅĐēŅ</b> <code>{}</code><b>!</b>"
        ),
        "prefix_collision": (
            "<emoji document_id=5469654973308476699>đŖ</emoji> <b>ĐŅĐĩŅĐ¸ĐēŅŅ Dragon Đ¸"
            " Hikka Đ´ĐžĐģĐļĐŊŅ ĐžŅĐģĐ¸ŅĐ°ŅŅŅŅ!</b>"
        ),
    }

    strings_fr = {
        "too_many_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Trop d'arguments </b>"
        ),
        "blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Le chat {} a ÃŠtÃŠ"
            " ajoutÃŠ Ã  la liste noire du robot utilisateur</b>"
        ),
        "unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Le chat {} a ÃŠtÃŠ"
            " supprimÃŠ de la liste noire du robot utilisateur</b>"
        ),
        "user_blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>L'utilisateur {}"
            " a ÃŠtÃŠ ajoutÃŠ Ã  la liste noire du robot utilisateur</b>"
        ),
        "user_unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>L'utilisateur {}"
            " a ÃŠtÃŠ supprimÃŠ de la liste noire du robot utilisateur</b>"
        ),
        "what_prefix": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>Et quel prÃŠfixe"
            " mettre alors ?</b>"
        ),
        "prefix_incorrect": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Le prÃŠfixe doit"
            " ÃĒtre composÃŠ d'un seul caractÃ¨re</b>"
        ),
        "prefix_set": (
            "{} <b>Le prÃŠfixe a ÃŠtÃŠ mis Ã  jour."
            " Pour le rÃŠtablir, utilisez</b> <code>{newprefix}setprefix"
            " {oldprefix}</code>"
        ),
        "alias_created": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>L'alias a ÃŠtÃŠ crÃŠÃŠ."
            " Utilisez-le avec</b> <code>{}</code>"
        ),
        "aliases": "<b>đ Alias:</b>\n",
        "no_command": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>La commande</b>"
            " <code>{}</code> <b>n'existe pas</b>"
        ),
        "alias_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Vous devez entrer"
            " une commande et un alias pour elle</b>"
        ),
        "delalias_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Vous devez entrer"
            " un alias</b>"
        ),
        "alias_removed": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Alias</b>"
            " <code>{}</code> <b>supprimÃŠ</b>."
        ),
        "no_alias": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Alias</b>"
            " <code>{}</code> <b>n'existe pas</b>"
        ),
        "db_cleared": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Base de donnÃŠes"
            " effacÃŠe</b>"
        ),
        "hikka": (
            "{} <b>{}.{}.{}</b> <i>{}</i>\n\n<b><emoji"
            " document_id=5377437404078546699>đ</emoji> <b>Hikka-TL:"
            "</b> <i>{}</i>\n{}"
            " <b>Hikka-Pyro:</b> <i>{}</i>\n\n<emoji"
            " document_id=5454182070156794055>â¨ī¸</emoji> <b>Developer:"
            " t.me/hikariatama</b>"
        ),
        "_cls_doc": "GÃŠrer les paramÃ¨tres de base du userbot",
        "confirm_cleardb": (
            "â ī¸ <b>Ãtes-vous sÃģr de vouloir rÃŠinitialiser la base de donnÃŠes?</b>"
        ),
        "cleardb_confirm": "đ Effacer la base de donnÃŠes",
        "cancel": "đĢ Annuler",
        "who_to_blacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>Qui bloquer?</b>"
        ),
        "who_to_unblacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>Qui dÃŠbloquer?</b>"
        ),
        "unstable": (
            "\n\n<emoji document_id=5467370583282950466>đ</emoji> <b>Vous utilisez"
            " une branche instable</b> <code>{}</code><b>!</b>"
        ),
        "prefix_collision": (
            "<emoji document_id=5469654973308476699>đŖ</emoji> <b>Les prÃŠfixes Dragon"
            " et Hikka doivent ÃĒtre diffÃŠrents!</b>"
        ),
    }

    strings_it = {
        "too_many_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Troppi argomenti</b>"
        ),
        "blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Il gruppo {} Ã¨ stato"
            " aggiunto alla lista nera del bot</b>"
        ),
        "unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Il gruppo {} Ã¨ stato"
            " rimosso dalla lista nera del bot</b>"
        ),
        "user_blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>L'utente {} Ã¨ stato"
            " aggiunto alla lista nera del bot</b>"
        ),
        "user_unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>L'utente {} Ã¨ stato"
            " rimosso dalla lista nera del bot</b>"
        ),
        "what_prefix": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>Che prefisso devo"
            " usare?</b>"
        ),
        "prefix_incorrect": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Il prefisso deve"
            " essere di un solo carattere</b>"
        ),
        "prefix_set": (
            "{} <b>Il prefisso Ã¨ stato aggiornato."
            " Per ripristinarlo, usa</b> <code>{newprefix}setprefix"
            " {oldprefix}</code>"
        ),
        "alias_created": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>L'alias Ã¨ stato"
            " creato. Usa il comando con</b> <code>{}</code>"
        ),
        "aliases": "<b>đ Alias:</b>\n",
        "no_command": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Il comando</b>"
            " <code>{}</code> <b>non esiste</b>"
        ),
        "alias_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Ã necessario"
            " specificare un comando e un alias per questo</b>"
        ),
        "delalias_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Nome alias"
            " richiesto</b>"
        ),
        "alias_removed": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Alias</b>"
            " <code>{}</code> <b>rimosso</b>."
        ),
        "no_alias": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Alias</b>"
            " <code>{}</code> <b>non esiste</b>"
        ),
        "db_cleared": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Database"
            " cancellato</b>"
        ),
        "hikka": (
            "{} <b>{}.{}.{}</b> <i>{}</i>\n\n<b><emoji"
            " document_id=5377437404078546699>đ</emoji> <b>Hikka-TL:"
            "</b> <i>{}</i>\n{}"
            " <b>Hikka-Pyro:</b> <i>{}</i>\n\n<emoji"
            " document_id=5454182070156794055>â¨ī¸</emoji> <b>Developer:"
            " t.me/hikariatama</b>"
        ),
        "_cls_doc": "Gestisci le impostazioni base del bot utente",
        "confirm_cleardb": "â ī¸ <b>Sei sicuro di voler cancellare il database?</b>",
        "cleardb_confirm": "đ Cancella il database",
        "cancel": "đĢ Annulla",
        "who_to_blacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>Chi vuoi bloccare?"
            " </b>"
        ),
        "who_to_unblacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>Chi vuoi sbloccare?"
            " </b>"
        ),
        "unstable": (
            "\n\n<emoji document_id=5467370583282950466>đ</emoji> <b>Stai usando una"
            " versione instabile</b> <code>{}</code><b>!</b>"
        ),
        "prefix_collision": (
            "<emoji document_id=5469654973308476699>đŖ</emoji> <b>I prefissi Dragon e"
            " Hikka devono essere diversi!</b>"
        ),
    }

    strings_de = {
        "too_many_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Zu vieleArgumente</b>"
        ),
        "blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Chat {} hinzugefÃŧgt"
            " zuUserbot-Blacklist</b>"
        ),
        "unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Chat {} entfernt aus"
            "Blacklist fÃŧr Userbots</b>"
        ),
        "user_blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Benutzer {}"
            "Von Userbot auf die schwarze Liste gesetzt</b>"
        ),
        "user_unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Benutzer {}"
            " von Userbot-Blacklist entfernt</b>"
        ),
        "what_prefix": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>Welches PrÃ¤fix soll"
            " ich setzen?</b>"
        ),
        "prefix_incorrect": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>PrÃ¤fix muss"
            "bestehen nur aus einem Zeichen</b>"
        ),
        "prefix_set": (
            "{} <b>PrÃ¤fix aktualisiert."
            " Um es zurÃŧckzugeben, verwenden Sie</b> <code>{newprefix}setprefix"
            "{oldprefix}</code>"
        ),
        "alias_created": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Alias ââerstellt."
            " Verwenden Sie es Ãŧber</b> <code>{}</code>"
        ),
        "aliases": "<b>đ Aliasse:</b>\n",
        "no_command": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Befehl</b>"
            " <code>{}</code> <b>existiert nicht</b>"
        ),
        "alias_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Eingabe erforderlich"
            "Befehl und Alias ââdafÃŧr</b>"
        ),
        "delalias_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Name erforderlich"
            "alias</b>"
        ),
        "alias_removed": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Alias</b>"
            " <code>{}</code> <b>gelÃļscht</b>."
        ),
        "no_alias": (
            "<emoji document_id=5312526098750252863>đĢ</emoji><b>Alias</b>"
            " <code>{}</code> <b>existiert nicht</b>"
        ),
        "db_cleared": (
            "<emoji document_id=5197474765387864959>đ</emoji><b>Basis gelÃļscht</b>"
        ),
        "hikka": (
            "{} <b>{}.{}.{}</b> <i>{}</i>\n\n<b><emoji"
            " document_id=5377437404078546699>đ</emoji> <b>Hikka-TL:"
            "</b> <i>{}</i>\n{}"
            " <b>Hikka-Pyro:"
            "</b> <i>{}</i>\n\n<emoji document_id=5454182070156794055>â¨ī¸</emoji>"
            " <b>Entwickler: t.me/hikariatama</b>"
        ),
        "_cls_doc": "Verwaltung der Grundeinstellungen des Userbots",
        "confirm_cleardb": (
            "â ī¸ <b>Sind Sie sicher, dass Sie die Datenbank zurÃŧcksetzen mÃļchten?</b>"
        ),
        "cleardb_confirm": "đ Basis lÃļschen",
        "cancel": "đĢ Stornieren",
        "who_to_blacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>Zu blockierende"
            " Personendann?"
        ),
        "who_to_unblacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>Wen entsperrendann?"
        ),
        "unstable": (
            "\n\n<emoji document_id=5467370583282950466>đ</emoji> <b>Sie verwenden"
            "instabiler Zweig</b> <code>{}</code><b>!</b>"
        ),
        "prefix_collision": (
            "<emoji document_id=5469654973308476699>đŖ</emoji> <b>PrÃ¤fixe"
            "Dragon und Hikka mÃŧssen sich unterscheiden!</b>"
        ),
    }

    strings_tr = {
        "too_many_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Ãok fazla"
            " argÃŧman var</b>"
        ),
        "blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>{} adlÄą sohbet,"
            " kullanÄącÄą botu kara listesine eklendi</b>"
        ),
        "unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>{} adlÄą sohbet,"
            " kullanÄącÄą botu kara listesinden Ã§ÄąkartÄąldÄą</b>"
        ),
        "user_blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>{} adlÄą kiÅi,"
            " kullanÄącÄą botu kara listesine eklendi</b>"
        ),
        "user_unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>{} adlÄą kiÅi,"
            " kullanÄącÄą botu kara listesine eklendi</b>"
        ),
        "what_prefix": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>Hangi Ãļneki"
            " ayarlamalÄąyÄąm?</b>"
        ),
        "prefix_incorrect": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Ãnek sadece"
            " bir karakterden oluÅabilir</b>"
        ),
        "prefix_set": (
            "{} <b>Komut Ãļneki gÃŧncellendi. Yeniden deÄiÅtirmek iÃ§in"
            " iÃ§in,</b> <code>{newprefix}setprefix {oldprefix}</code> <b>komutunu"
            " kullanÄąn</b>"
        ),
        "alias_created": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Komut iÃ§in takma ad"
            " oluÅturuldu.</b> <code>{}</code> <b>komutuyla kullanabilirsiniz</b>"
        ),
        "aliases": "<b>đ Takma adlar:</b>\n",
        "no_command": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Komut</b>"
            " <code>{}</code> <b>mevcut deÄil</b>"
        ),
        "alias_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Bunun iÃ§in bir komut"
            " ve takma ad girmeniz gerekmektedir</b>"
        ),
        "delalias_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Bunun iÃ§in bir takma "
            " ad girmeniz gerekmektedir</b>"
        ),
        "alias_removed": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Takma ad</b>"
            " <code>{}</code> <b>kaldÄąrÄąldÄą</b>."
        ),
        "no_alias": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Takma Ad</b>"
            " <code>{}</code> <b>mevcut deÄil</b>"
        ),
        "db_cleared": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Veri TabanÄą"
            " sÄąfÄąrlandÄą</b>"
        ),
        "hikka": (
            "{} <b>{}.{}.{}</b> <i>{}</i>\n\n<b><emoji"
            " document_id=5377437404078546699>đ</emoji> <b>Hikka-TL:"
            "</b> <i>{}</i>\n{}"
            " <b>Hikka-Pyro:"
            "</b> <i>{}</i>\n\n<emoji document_id=5454182070156794055>â¨ī¸</emoji>"
            " <b>GeliÅtirici: t.me/hikariatama</b>"
        ),
        "_cls_doc": "Userbot temel ayar yÃļnetimi",
        "confirm_cleardb": (
            "â ī¸ <b>VeritabanÄąnÄą sÄąfÄąrlamak istediÄinizden emin misiniz?</b>"
        ),
        "cleardb_confirm": "đ Veri TabanÄąnÄą sÄąfÄąrla",
        "cancel": "đĢ Ä°ptal",
        "who_to_blacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>Kimler engellenir"
            "sonra?</b>"
        ),
        "who_to_unblacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>Kimin engellemesi"
            " kaldÄąrÄąlsÄąn?</b>"
        ),
        "unstable": (
            "\n\n<emoji document_id=5467370583282950466>đ</emoji> <b>Hikka'nÄąn kararsÄąz"
            " bir sÃŧrÃŧmÃŧ olan <code>{}</code></b>  sÃŧrÃŧmÃŧnÃŧ kullanÄąyorsunuz!</b>"
        ),
        "prefix_collision": (
            "<emoji document_id=5469654973308476699>đŖ</emoji> <b>Ãnekler Ã§akÄąÅÄąyor!</b>"
        ),
    }

    strings_uz = {
        "too_many_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Juda ko'p"
            " argumentlar</b>"
        ),
        "blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Chat {} qo'shildi"
            " userbot qora ro' yxati</b>"
        ),
        "unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Chat {} o'chirildi"
            "Userbot qora ro'yxati</b>"
        ),
        "user_blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Foydalanuvchi {}"
            " userbot tomonidan qora ro'yxatga kiritilgan</b>"
        ),
        "user_unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Foydalanuvchi {}"
            " userbot qora ro'yxatidan olib tashlandi</b>"
        ),
        "what_prefix": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>Qaysi prefiksni"
            " o'rnatishim kerak?</b>"
        ),
        "prefix_incorrect": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Prefiks kerak"
            "faqat bitta belgidan iborat</b>"
        ),
        "prefix_set": (
            "{} <b>Prefiks yangilandi."
            " Uni qaytarish uchun</b> <code>{newprefix}setprefix dan foydalaning."
            "{oldprefix}</code>"
        ),
        "alias_created": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Taxallus yaratildi."
            "</b> <code>{}</code> <b>orqali foydalaning</b>"
        ),
        "aliases": "<b>đ Taxalluslar:</b>\n",
        "no_command": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Buyruq</b>"
            " <code>{}</code> <b>mavjud</b>"
        ),
        "alias_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Kirish kerak"
            "buyruq va uning taxallusi</b>"
        ),
        "delalias_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Ism keraktaxallus</b>"
        ),
        "alias_removed": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Taxallus</b>"
            " <code>{}</code> <b>o'chirildi</b>."
        ),
        "no_alias": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Taxallus</b>"
            " <code>{}</code> <b>mavjud</b>"
        ),
        "db_cleared": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Baza tozalandi</b>"
        ),
        "hikka": (
            "{} <b>{}.{}.{}</b> <i>{}</i>\n\n<b><emoji"
            " document_id=5377437404078546699>đ</emoji> <b>Hikka-TL:"
            "</b> <i>{}</i>\n{}"
            " <b>Hikka-Pyro:</b> <i>{}</i>\n\n<emoji"
            " document_id=5454182070156794055>â¨ī¸</emoji> <b>Ishlab chiquvchi:"
            " t.me/hikariatama</b>"
        ),
        "_cls_doc": "Userbot asosiy sozlamalarini boshqarish",
        "confirm_cleardb": (
            "â ī¸ <b>Siz maĘŧlumotlar bazasini qayta o'rnatmoqchimisiz?</b>"
        ),
        "cleardb_confirm": "đ Bazani tozalash",
        "cancel": "đĢ Bekor qilish",
        "who_to_blacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>Kimni bloklash kerak"
            "keyin?</b>"
        ),
        "who_to_unblacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>Kimni blokdan"
            " chiqarish kerakkeyin?</b>"
        ),
        "unstable": (
            "\n\n<emoji document_id=5467370583282950466>đ</emoji> <b>Siz"
            " foydalanayotgan versiya</b> <code>{}</code><b>!</b>"
        ),
        "prefix_collision": (
            "<emoji document_id=5469654973308476699>đŖ</emoji> <b>Dragon va Hikka"
            " prefikslari boshqacha bo'lishi kerak!</b>"
        ),
    }

    strings_es = {
        "chat_blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>El chat {} ha sido"
            " aÃąadido a la lista negra</b>"
        ),
        "chat_unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>El chat {} ha sido"
            " removido de la lista negra</b>"
        ),
        "user_blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>El usuario {} ha sido"
            " aÃąadido a la lista negra</b>"
        ),
        "user_unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>El usuario {} ha sido"
            " removido de la lista negra</b>"
        ),
        "what_prefix": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>ÂŋCuÃĄl es el prefijo"
            " que quieres establecer?</b>"
        ),
        "prefix_incorrect": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>El prefijo debe ser"
            " un solo carÃĄcter</b>"
        ),
        "prefix_set": (
            "{} <b>El prefijo ha sido"
            " establecido. El nuevo prefijo es</b> <code>{newprefix}setprefix"
            " {oldprefix}</code> <b>para restablecerlo</b>"
        ),
        "alias_created": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>El alias</b>"
            " <code>{}</code> <b>ha sido creado</b>"
        ),
        "alias_deleted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>El alias</b>"
            " <code>{}</code> <b>ha sido eliminado</b>"
        ),
        "no_alias": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>Alias</b>"
            " <code>{}</code> <b>no existe</b>"
        ),
        "db_cleared": (
            "<emoji document_id=5197474765387864959>đ</emoji><b>Base de datos"
            " borrada</b>"
        ),
        "hikka": (
            "{} <b>{}.{}.{}</b> <i>{}</i>\n\n<b><emoji"
            " document_id=5377437404078546699>đ</emoji> <b>Hikka-TL:"
            "</b> <i>{}</i>\n{}"
            " <b>Hikka-Pyro:</b> <i>{}</i>\n\n<emoji"
            " document_id=5454182070156794055>â¨ī¸</emoji> <b>Desarrollador:"
            " t.me/hikariatama</b>"
        ),
        "_cls_doc": "Los ajustes bÃĄsicos del usuario del bot",
        "confirm_cleardb": "â ī¸ <b>ÂŋQuieres borrar la base de datos?</b>",
        "cleardb_confirm": "đ Borrar base de datos",
        "cancel": "đĢ Cancelar",
        "who_to_blacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>ÂŋQuiÃŠn quieres"
            " aÃąadir a la lista negra?</b>"
        ),
        "who_to_unblacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>ÂŋQuiÃŠn quieres"
            " eliminar de la lista negra?</b>"
        ),
        "unstable": (
            "\n\n<emoji document_id=5467370583282950466>đ</emoji> <b>EstÃĄs usando la"
            " rama inestable</b> <code>{}</code><b>!</b>"
        ),
        "prefix_collision": (
            "<emoji document_id=5469654973308476699>đŖ</emoji> <b>ÂĄDragon y Hikka deben"
            " tener prefijos diferentes!</b>"
        ),
    }

    strings_kk = {
        "too_many_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĸŅĐŧ ĐēĶŠĐŋ"
            " Đ°ŅĐŗŅĐŧĐĩĐŊŅŅĐĩŅ</b>"
        ),
        "blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Đ§Đ°Ņ {} ŅĐ°ŅŅĐ°Ņ"
            "Đ´ŅŌŖ ĐēĶŠŅŅĐĩŅĐēŅŅŅĐŊŅŌŖ ĐēŌ¯ĐšŅĐŊĐĩ ŌĐžŅŅĐģĐ´Ņ</b>"
        ),
        "unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>Đ§Đ°Ņ {} ŅĐ°ŅŅĐ°Ņ"
            "Đ´ŅŌŖ ĐēĶŠŅŅĐĩŅĐēŅŅŅĐŊŅŌŖ ĐēŌ¯ĐšŅĐŊĐĩĐŊ Đ°ĐģŅĐŊĐ´Ņ</b>"
        ),
        "user_blacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>ĐĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŅŅ {}"
            " ĐŋĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŅŅĐģĐ°ŅĐ´ŅŌŖ ĐēĶŠŅŅĐĩŅĐēŅŅŅĐŊŅŌŖ ĐēŌ¯ĐšŅĐŊĐĩ ŌĐžŅŅĐģĐ´Ņ</b>"
        ),
        "user_unblacklisted": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>ĐĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŅŅ {}"
            " ĐŋĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŅŅĐģĐ°ŅĐ´ŅŌŖ ĐēĶŠŅŅĐĩŅĐēŅŅŅĐŊŅŌŖ ĐēŌ¯ĐšŅĐŊĐĩĐŊ Đ°ĐģŅĐŊĐ´Ņ</b>"
        ),
        "what_prefix": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>ĐŅŅĐ°Ō"
            " ŌĐ°ĐŊĐ´Đ°Đš ĶĐģŅĐŋĐąĐ¸ ĐąĐĩŅĐĩĐŧŅĐŊ?</b>"
        ),
        "prefix_incorrect": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĶĐģŅĐŋĐąĐ¸ ŅĐĩĐē"
            " ĐąŅŅ ŅĐ°ŌŖĐąĐ°Đ´Đ°ĐŊ ŅŌąŅŅŅ ĐēĐĩŅĐĩĐē</b>"
        ),
        "prefix_set": (
            "{} <b>ĶĐģŅĐŋĐąĐ¸ ĐļĐ°ŌŖĐ°ŅŅŅĐģĐ´Ņ."
            " ŌĐ°ĐšŅĐ°ŅŅ Ō¯ŅŅĐŊ</b> <code>{newprefix}setprefix {oldprefix}</code>"
            " <b>ĐŋĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŌŖŅĐˇ</b>"
        ),
        "alias_created": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>ĐĐģĐ¸Đ°Ņ ĐļĐ°ŅĐ°ĐģĐ´Ņ."
            " ĐĐŊŅ</b> <code>{}</code> <b>ĐŋĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŌŖŅĐˇ</b>"
        ),
        "aliases": "<b>đ ĐĐģĐ¸Đ°ŅŅĐ°Ņ:</b>\n",
        "no_command": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĐžĐŧĐ°ĐŊĐ´Đ°</b>"
            " <code>{}</code> <b>ĐļĐžŌ</b>"
        ),
        "alias_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĐžĐŧĐ°ĐŊĐ´Đ° ĐŧĐĩĐŊ"
            " ĐžĐŊŅŌŖ Đ°ĐģĐ¸Đ°ŅŅĐŊ ĐĩĐŊĐŗŅĐˇŅŅŌŖŅĐˇ ĐēĐĩŅĐĩĐē</b>"
        ),
        "delalias_args": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĐģĐ¸Đ°Ņ Đ°ŅĐ°ŅŅ"
            " ĐĩĐŊĐŗŅĐˇŅŅŌŖŅĐˇ ĐēĐĩŅĐĩĐē</b>"
        ),
        "alias_removed": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>ĐĐģĐ¸Đ°Ņ</b>"
            " <code>{}</code> <b>ĐļĐžĐšŅĐģĐ´Ņ</b>."
        ),
        "no_alias": (
            "<emoji document_id=5312526098750252863>đĢ</emoji> <b>ĐĐģĐ¸Đ°Ņ</b>"
            " <code>{}</code> <b>ĐļĐžŌ</b>"
        ),
        "db_cleared": (
            "<emoji document_id=5197474765387864959>đ</emoji> <b>ĐĐ°ĐˇĐ° ŅĐ°ĐˇĐ°ĐģĐ°ĐŊĐ´Ņ</b>"
        ),
        "hikka": (
            "{} <b>{}.{}.{}</b> <i>{}</i>\n\n<b><emoji"
            " document_id=5377437404078546699>đ</emoji> <b>Hikka-TL:"
            "</b> <i>{}</i>\n{}"
            " <b>Hikka-Pyro:</b> <i>{}</i>\n\n<emoji"
            " document_id=5454182070156794055>â¨ī¸</emoji> <b>ĶĐˇŅŅĐģĐĩŅŅŅ:"
            " t.me/hikariatama</b>"
        ),
        "_cls_doc": "ĐŌ¯ĐšĐĩ ĐąĐ°ŅŅĐ°ĐŋŌŅ ĐŋĐ°ŅĐ°ĐŧĐĩŅŅĐģĐĩŅŅĐŊ ĐąĐ°ŅŌĐ°ŅŅ",
        "confirm_cleardb": (
            "â ī¸ <b>ĐĄŅĐˇ Đ´ĐĩĐšŅĐŊĐŗŅ ĐąĐ°ĐˇĐ° Đ´ĐĩŅĐĩĐēŅĐĩŅŅĐŊ ŅĐ°ĐˇĐ°ĐģĐ°ŅŌĐ° ŅĐĩĐŊŅĐŧĐ´ŅŅŅĐˇ ĐąĐĩ?</b>"
        ),
        "cleardb_confirm": "đ ĐĐ°ĐˇĐ° Đ´ĐĩŅĐĩĐēŅĐĩŅŅĐŊ ŅĐ°ĐˇĐ°ĐģĐ°Ņ",
        "cancel": "đĢ ĐĐžĐģĐ´ŅŅĐŧĐ°Ņ",
        "who_to_blacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>ĐŅĐŧĐ´Ņ ĐąĐģĐžĐŗĐ° ŌĐžŅ"
            " ĐēĐĩŅĐĩĐē?</b>"
        ),
        "who_to_unblacklist": (
            "<emoji document_id=5382187118216879236>â</emoji> <b>ĐŅĐŧĐ´Ņ ĐąĐģĐžĐŗĐ° ŌĐžŅĐ´Ņ"
            " ĐąĐžĐģĐ´ŅŅĐŧĐ°Ņ ĐēĐĩŅĐĩĐē?</b>"
        ),
        "unstable": (
            "\n\n<emoji document_id=5467370583282950466>đ</emoji> <b>ĐĄŅĐˇ ŌĐžĐģĐ´Đ°ĐŊĐąĐ°ŌĐ°ĐŊ"
            " ĐąĐĩĐģĐŗŅŅŅĐˇ ŌĐžŅŅĐŧŅĐ°</b> <code>{}</code><b>!</b>"
        ),
        "prefix_collision": (
            "<emoji document_id=5469654973308476699>đŖ</emoji> <b>Dragon ĐļĶĐŊĐĩ"
            " Hikka ĐŋŅĐĩŅĐ¸ĐēŅŅĐĩŅŅ Đ°ĐšŅŅĐŧĐ°ŅŅ ĐēĐĩŅĐĩĐē!</b>"
        ),
    }

    async def blacklistcommon(self, message: Message):
        args = utils.get_args(message)

        if len(args) > 2:
            await utils.answer(message, self.strings("too_many_args"))
            return

        chatid = None
        module = None

        if args:
            try:
                chatid = int(args[0])
            except ValueError:
                module = args[0]

        if len(args) == 2:
            module = args[1]

        if chatid is None:
            chatid = utils.get_chat_id(message)

        module = self.allmodules.get_classname(module)
        return f"{str(chatid)}.{module}" if module else chatid

    @loader.command(
        ru_doc="ĐĐžĐēĐ°ĐˇĐ°ŅŅ Đ˛ĐĩŅŅĐ¸Ņ Hikka",
        fr_doc="Afficher la version de Hikka",
        it_doc="Mostra la versione di Hikka",
        de_doc="Zeige die Hikka-Version an",
        tr_doc="Hikka sÃŧrÃŧmÃŧnÃŧ gÃļsterir",
        uz_doc="Hikka versiyasini ko'rsatish",
        es_doc="Mostrar la versiÃŗn de Hikka",
        kk_doc="Hikka ĐŊŌąŅŌĐ°ŅŅĐŊ ĐēĶŠŅŅĐĩŅŅ",
    )
    async def hikkacmd(self, message: Message):
        """Get Hikka version"""
        await utils.answer_file(
            message,
            "https://github.com/hikariatama/assets/raw/master/hikka_cat_banner.mp4",
            self.strings("hikka").format(
                (
                    utils.get_platform_emoji()
                    if self._client.hikka_me.premium and CUSTOM_EMOJIS
                    else "đ <b>Hikka userbot</b>"
                ),
                *version.__version__,
                utils.get_commit_url(),
                f"{telethon.__version__} #{telethon.tl.alltlobjects.LAYER}",
                (
                    "<emoji document_id=5377399247589088543>đĨ</emoji>"
                    if self._client.pyro_proxy
                    else "<emoji document_id=5418308381586759720>đ´</emoji>"
                ),
                f"{pyrogram.__version__} #{pyrogram.raw.all.layer}",
            )
            + (
                ""
                if version.branch == "master"
                else self.strings("unstable").format(version.branch)
            ),
        )

    @loader.command(
        ru_doc="[ŅĐ°Ņ] [ĐŧĐžĐ´ŅĐģŅ] - ĐŅĐēĐģŅŅĐ¸ŅŅ ĐąĐžŅĐ° ĐŗĐ´Đĩ-ĐģĐ¸ĐąĐž",
        fr_doc="[chat] [module] - DÃŠsactiver le bot n'importe oÃš",
        it_doc="[chat] [module] - Disattiva il bot ovunque",
        de_doc="[chat] [Modul] - Deaktiviere den Bot irgendwo",
        tr_doc="[sohbet] [modÃŧl] - Botu herhangi bir yerde devre dÄąÅÄą bÄąrakÄąn",
        uz_doc="[chat] [modul] - Botni hozircha o'chirish",
        es_doc="[chat] [mÃŗdulo] - Desactivar el bot en cualquier lugar",
        kk_doc="[ŅĶŠĐšĐģĐĩŅŅ] [ĐŧĐžĐ´ŅĐģŅ] - ĐĐžŅŅŅ ŌĐ°ĐšĐ´Đ° ĐąĐžĐģŅĐ° ĐąĐžĐģŅŅĐŊ ĶŠŅŅŅŅ",
    )
    async def blacklist(self, message: Message):
        """[chat_id] [module] - Blacklist the bot from operating somewhere"""
        chatid = await self.blacklistcommon(message)

        self._db.set(
            main.__name__,
            "blacklist_chats",
            self._db.get(main.__name__, "blacklist_chats", []) + [chatid],
        )

        await utils.answer(message, self.strings("blacklisted").format(chatid))

    @loader.command(
        ru_doc="[ŅĐ°Ņ] - ĐĐēĐģŅŅĐ¸ŅŅ ĐąĐžŅĐ° ĐŗĐ´Đĩ-ĐģĐ¸ĐąĐž",
        fr_doc="[chat] - Activer le bot n'importe oÃš",
        it_doc="[chat] - Attiva il bot ovunque",
        de_doc="[chat] - Aktiviere den Bot irgendwo",
        tr_doc="[sohbet] - Botu herhangi bir yerde etkinleÅtirin",
        uz_doc="[chat] - Botni hozircha yoqish",
        es_doc="[chat] - Activar el bot en cualquier lugar",
        kk_doc="[ŅĶŠĐšĐģĐĩŅŅ] - ĐĐžŅŅŅ ŌĐ°ĐšĐ´Đ° ĐąĐžĐģŅĐ° ĐąĐžĐģŅŅĐŊ ŌĐžŅŅ",
    )
    async def unblacklist(self, message: Message):
        """<chat_id> - Unblacklist the bot from operating somewhere"""
        chatid = await self.blacklistcommon(message)

        self._db.set(
            main.__name__,
            "blacklist_chats",
            list(set(self._db.get(main.__name__, "blacklist_chats", [])) - {chatid}),
        )

        await utils.answer(message, self.strings("unblacklisted").format(chatid))

    async def getuser(self, message: Message):
        try:
            return int(utils.get_args(message)[0])
        except (ValueError, IndexError):
            reply = await message.get_reply_message()

            if reply:
                return reply.sender_id

            return message.to_id.user_id if message.is_private else False

    @loader.command(
        ru_doc="[ĐŋĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģŅ] - ĐĐ°ĐŋŅĐĩŅĐ¸ŅŅ ĐŋĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģŅ Đ˛ŅĐŋĐžĐģĐŊŅŅŅ ĐēĐžĐŧĐ°ĐŊĐ´Ņ",
        fr_doc="[utilisateur] - Interdire Ã  l'utilisateur d'exÃŠcuter des commandes",
        it_doc="[utente] - Impedisci all'utente di eseguire comandi",
        de_doc="[Benutzer] - Verbiete dem Benutzer, Befehle auszufÃŧhren",
        tr_doc="[kullanÄącÄą] - KullanÄącÄąya komutlarÄą yÃŧrÃŧtmeyi yasakla",
        uz_doc="[foydalanuvchi] - Foydalanuvchiga buyruqlarni bajarishni taqiqlash",
        es_doc="[usuario] - Prohibir al usuario ejecutar comandos",
        kk_doc="[ĐŋĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŅŅ] - ĐĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŅŅŌĐ° ĐēĐžĐŧĐ°ĐŊĐ´Đ°ĐģĐ°ŅĐ´Ņ ĐžŅŅĐŊĐ´Đ°ŅŌĐ° ŅŌąŌŅĐ°Ņ ĐąĐĩŅĐŧĐĩŅ",
    )
    async def blacklistuser(self, message: Message):
        """[user_id] - Prevent this user from running any commands"""
        user = await self.getuser(message)

        if not user:
            await utils.answer(message, self.strings("who_to_blacklist"))
            return

        self._db.set(
            main.__name__,
            "blacklist_users",
            self._db.get(main.__name__, "blacklist_users", []) + [user],
        )

        await utils.answer(message, self.strings("user_blacklisted").format(user))

    @loader.command(
        ru_doc="[ĐŋĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģŅ] - Đ Đ°ĐˇŅĐĩŅĐ¸ŅŅ ĐŋĐžĐģŅĐˇĐžĐ˛Đ°ŅĐĩĐģŅ Đ˛ŅĐŋĐžĐģĐŊŅŅŅ ĐēĐžĐŧĐ°ĐŊĐ´Ņ",
        fr_doc="[utilisateur] - Autoriser l'utilisateur Ã  exÃŠcuter des commandes",
        it_doc="[utente] - Consenti all'utente di eseguire comandi",
        de_doc="[Benutzer] - Erlaube dem Benutzer, Befehle auszufÃŧhren",
        tr_doc="[kullanÄącÄą] - KullanÄącÄąya komutlarÄą yÃŧrÃŧtmeyi yasakla",
        uz_doc="[foydalanuvchi] - Foydalanuvchiga buyruqlarni bajarishni taqiqlash",
        es_doc="[usuario] - Prohibir al usuario ejecutar comandos",
        kk_doc="[ĐŋĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŅŅ] - ĐĐ°ĐšĐ´Đ°ĐģĐ°ĐŊŅŅŅŌĐ° ĐēĐžĐŧĐ°ĐŊĐ´Đ°ĐģĐ°ŅĐ´Ņ ĐžŅŅĐŊĐ´Đ°ŅŌĐ° ŅŌąŌŅĐ°Ņ ĐąĐĩŅĐŧĐĩŅ",
    )
    async def unblacklistuser(self, message: Message):
        """[user_id] - Allow this user to run permitted commands"""
        user = await self.getuser(message)

        if not user:
            await utils.answer(message, self.strings("who_to_unblacklist"))
            return

        self._db.set(
            main.__name__,
            "blacklist_users",
            list(set(self._db.get(main.__name__, "blacklist_users", [])) - {user}),
        )

        await utils.answer(
            message,
            self.strings("user_unblacklisted").format(user),
        )

    @loader.owner
    @loader.command(
        ru_doc="[dragon] <ĐŋŅĐĩŅĐ¸ĐēŅ> - ĐŖŅŅĐ°ĐŊĐžĐ˛Đ¸ŅŅ ĐŋŅĐĩŅĐ¸ĐēŅ ĐēĐžĐŧĐ°ĐŊĐ´",
        fr_doc="[dragon] <prÃŠfixe> - DÃŠfinir le prÃŠfixe des commandes",
        it_doc="[dragon] <prefisso> - Imposta il prefisso dei comandi",
        de_doc="[dragon] <PrÃ¤fix> - Setze das BefehlsprÃ¤fix",
        tr_doc="[dragon] <Ãļnek> - Komut Ãļneki ayarla",
        uz_doc="[dragon] <avvalgi> - Buyruqlar uchun avvalgi belgilash",
        es_doc="[dragon] <prefijo> - Establecer el prefijo de comandos",
        kk_doc="[dragon] <ĐąĐ°ŅŅĐ°ŅŅŅ> - ĐĐžĐŧĐ°ĐŊĐ´Đ°ĐģĐ°ŅĐ´ŅŌŖ ĐąĐ°ŅŅĐ°ŅŅŅŅĐŊ ĐžŅĐŊĐ°ŅŅ",
    )
    async def setprefix(self, message: Message):
        """[dragon] <prefix> - Sets command prefix"""
        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(message, self.strings("what_prefix"))
            return

        if len(args.split()) == 2 and args.split()[0] == "dragon":
            args = args.split()[1]
            is_dragon = True
        else:
            is_dragon = False

        if len(args) != 1:
            await utils.answer(message, self.strings("prefix_incorrect"))
            return

        if (
            not is_dragon
            and args[0] == self._db.get("dragon.prefix", "command_prefix", ",")
            or is_dragon
            and args[0] == self._db.get(main.__name__, "command_prefix", ".")
        ):
            await utils.answer(message, self.strings("prefix_collision"))
            return

        oldprefix = (
            f"dragon {self.get_prefix('dragon')}" if is_dragon else self.get_prefix()
        )
        self._db.set(
            "dragon.prefix" if is_dragon else main.__name__,
            "command_prefix",
            args,
        )
        await utils.answer(
            message,
            self.strings("prefix_set").format(
                (
                    DRAGON_EMOJI
                    if is_dragon
                    else "<emoji document_id=5197474765387864959>đ</emoji>"
                ),
                newprefix=utils.escape_html(
                    self.get_prefix() if is_dragon else args[0]
                ),
                oldprefix=utils.escape_html(oldprefix),
            ),
        )

    @loader.owner
    @loader.command(
        ru_doc="ĐĐžĐēĐ°ĐˇĐ°ŅŅ ŅĐŋĐ¸ŅĐžĐē Đ°ĐģĐ¸Đ°ŅĐžĐ˛",
        fr_doc="Afficher la liste des alias",
        it_doc="Mostra la lista degli alias",
        de_doc="Zeige Aliase",
        tr_doc="Takma adlarÄą gÃļster",
        uz_doc="Aliaslarni ko'rsatish",
        es_doc="Mostrar lista de alias",
        kk_doc="ĐĐšĐģĐ°ĐŊŅŅŅĐ°ŅĐ´Ņ ĐēĶŠŅŅĐĩŅŅ",
    )
    async def aliases(self, message: Message):
        """Print all your aliases"""
        aliases = self.allmodules.aliases
        string = self.strings("aliases")

        string += "\n".join(
            [f"âĢī¸ <code>{i}</code> &lt;- {y}" for i, y in aliases.items()]
        )

        await utils.answer(message, string)

    @loader.owner
    @loader.command(
        ru_doc="ĐŖŅŅĐ°ĐŊĐžĐ˛Đ¸ŅŅ Đ°ĐģĐ¸Đ°Ņ Đ´ĐģŅ ĐēĐžĐŧĐ°ĐŊĐ´Ņ",
        fr_doc="DÃŠfinir un alias pour la commande",
        it_doc="Imposta un alias per il comando",
        de_doc="Setze einen Alias fÃŧr einen Befehl",
        tr_doc="Bir komut iÃ§in takma ad ayarla",
        uz_doc="Buyrug' uchun alias belgilash",
        es_doc="Establecer alias para el comando",
        kk_doc="ĐĐžĐŧĐ°ĐŊĐ´Đ° Ō¯ŅŅĐŊ Đ°ĐšĐģĐ°ĐŊŅŅ ĐžŅĐŊĐ°ŅŅ",
    )
    async def addalias(self, message: Message):
        """Set an alias for a command"""
        args = utils.get_args(message)

        if len(args) != 2:
            await utils.answer(message, self.strings("alias_args"))
            return

        alias, cmd = args
        if self.allmodules.add_alias(alias, cmd):
            self.set(
                "aliases",
                {
                    **self.get("aliases", {}),
                    alias: cmd,
                },
            )
            await utils.answer(
                message,
                self.strings("alias_created").format(utils.escape_html(alias)),
            )
        else:
            await utils.answer(
                message,
                self.strings("no_command").format(utils.escape_html(cmd)),
            )

    @loader.owner
    @loader.command(
        ru_doc="ĐŖĐ´Đ°ĐģĐ¸ŅŅ Đ°ĐģĐ¸Đ°Ņ Đ´ĐģŅ ĐēĐžĐŧĐ°ĐŊĐ´Ņ",
        fr_doc="Supprimer un alias pour la commande",
        it_doc="Rimuovi un alias per il comando",
        de_doc="Entferne einen Alias fÃŧr einen Befehl",
        tr_doc="Bir komut iÃ§in takma ad kaldÄąr",
        uz_doc="Buyrug' uchun aliasni o'chirish",
        es_doc="Eliminar alias para el comando",
        kk_doc="ĐĐžĐŧĐ°ĐŊĐ´Đ° Ō¯ŅŅĐŊ Đ°ĐšĐģĐ°ĐŊŅŅŅŅ ĐļĐžŅ",
    )
    async def delalias(self, message: Message):
        """Remove an alias for a command"""
        args = utils.get_args(message)

        if len(args) != 1:
            await utils.answer(message, self.strings("delalias_args"))
            return

        alias = args[0]
        removed = self.allmodules.remove_alias(alias)

        if not removed:
            await utils.answer(
                message,
                self.strings("no_alias").format(utils.escape_html(alias)),
            )
            return

        current = self.get("aliases", {})
        del current[alias]
        self.set("aliases", current)
        await utils.answer(
            message,
            self.strings("alias_removed").format(utils.escape_html(alias)),
        )

    @loader.owner
    @loader.command(
        ru_doc="ĐŅĐ¸ŅŅĐ¸ŅŅ ĐąĐ°ĐˇŅ Đ´Đ°ĐŊĐŊŅŅ",
        fr_doc="Vider la base de donnÃŠes",
        it_doc="Cancella il database",
        de_doc="Datenbank leeren",
        tr_doc="VeritabanÄąnÄą temizle",
        uz_doc="Ma'lumotlar bazasini tozalash",
        es_doc="Limpiar la base de datos",
        kk_doc="ĐĐĩŅĐĩĐēŅĐĩŅ ĐąĐ°ĐˇĐ°ŅŅĐŊ ŅĐ°ĐˇĐ°ĐģĐ°Ņ",
    )
    async def cleardb(self, message: Message):
        """Clear the entire database, effectively performing a factory reset"""
        await self.inline.form(
            self.strings("confirm_cleardb"),
            message,
            reply_markup=[
                {
                    "text": self.strings("cleardb_confirm"),
                    "callback": self._inline__cleardb,
                },
                {
                    "text": self.strings("cancel"),
                    "action": "close",
                },
            ],
        )

    async def _inline__cleardb(self, call: InlineCall):
        self._db.clear()
        self._db.save()
        await utils.answer(call, self.strings("db_cleared"))
