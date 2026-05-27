# ========================= FULL FIXED xHeaders.py =========================

import requests
import os
import psutil
import sys
import jwt
import pickle
import json
import binascii
import time
import urllib3
import base64
import datetime
import re
import socket
import threading
import random
import traceback

from protobuf_decoder.protobuf_decoder import Parser
from xC4 import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)

# ========================= TOKEN =========================

def GeTToK():

    try:

        with open("token.txt") as f:

            return f.read().strip()

    except Exception as e:

        print(f"❌ Token read error => {e}")

        return ""

# ========================= EMOTE EQUIP =========================

def equie_emote(JWT, url):

    try:

        url = f"{url}/ChooseEmote"

        headers = {
            "Accept-Encoding": "gzip",
            "Authorization": f"Bearer {JWT}",
            "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Expect": "100-continue",
            "ReleaseVersion": "OB52",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)",
            "X-GA": "v1 1",
            "X-Unity-Version": "2018.4.11f1",
        }

        data = bytes.fromhex(
            "CAF683222A25C7BEFEB51F59544DB313"
        )

        response = requests.post(
            url,
            headers=headers,
            data=data,
            timeout=15,
            verify=False
        )

        print(
            f"🔥 Equip emote => {response.status_code}"
        )

        return response.status_code == 200

    except Exception as e:

        print(f"❌ Equip emote error => {e}")

        traceback.print_exc()

        return False

# ========================= LIKES =========================

def Likes(id):

    try:

        response = requests.get(
            f"https://tokens-asfufvfshnfkhvbb.francecentral-01.azurewebsites.net/ReQuesT?id={id}&type=likes",
            timeout=15
        )

        text = response.text

        get = lambda p: re.search(p, text)

        name, lvl, exp, lb, la, lg = (
            get(r).group(1) if get(r) else None
            for r in
            [
                r"PLayer NamE\s*:\s*(.+)",
                r"PLayer SerVer\s*:\s*(.+)",
                r"Exp\s*:\s*(\d+)",
                r"LiKes BeFore\s*:\s*(\d+)",
                r"LiKes After\s*:\s*(\d+)",
                r"LiKes GiVen\s*:\s*(\d+)"
            ]
        )

        return (
            name,
            f"{lvl}" if lvl else None,
            int(lb) if lb else None,
            int(la) if la else None,
            int(lg) if lg else None
        )

    except Exception as e:

        print(f"❌ Likes error => {e}")

        return None, None, None, None, None

# ========================= SPAM =========================

def Requests_SPam(id):

    try:

        Api = requests.get(
            f'https://tokens-asfufvfshnfkhvbb.francecentral-01.azurewebsites.net/ReQuesT?id={id}&type=spam',
            timeout=15
        )

        if (
            Api.status_code in [200, 201]
            and
            '[SuccessFuLy] -> SenDinG Spam ReQuesTs !'
            in Api.text
        ):

            return True

        return False

    except Exception as e:

        print(f"❌ Spam error => {e}")

        return False

# ========================= PLAYER NAME =========================

def GeT_Name(uid, Token):

    try:

        data = bytes.fromhex(
            asyncio.run(
                EnC_AEs(
                    f"08{asyncio.run(EnC_Uid(uid , Tp='Uid'))}1007"
                )
            )
        )

        url = (
            "https://clientbp.common.ggbluefox.com/"
            "GetPlayerPersonalShow"
        )

        headers = {
            'X-Unity-Version': '2018.4.11f1',
            'ReleaseVersion': 'OB52',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-GA': 'v1 1',
            'Authorization': f'Bearer {GeTToK()}',
            'Content-Length': '16',
            'User-Agent': 'Dalvik/2.1.0',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }

        response = requests.post(
            url,
            headers=headers,
            data=data,
            timeout=15,
            verify=False
        )

        if response.status_code not in [200, 201]:

            return ''

        packet = binascii.hexlify(
            response.content
        ).decode('utf-8')

        BesTo_data = json.loads(
            asyncio.run(
                DeCode_PackEt(packet)
            )
        )

        try:

            return BesTo_data["1"]["data"]["3"]["data"]

        except:

            return ''

    except Exception as e:

        print(f"❌ Get name error => {e}")

        return ''

# ========================= PLAYER INFO =========================

def GeT_PLayer_InFo(uid, Token):

    try:

        data = bytes.fromhex(
            asyncio.run(
                EnC_AEs(
                    f"08{asyncio.run(EnC_Uid(uid , Tp='Uid'))}1007"
                )
            )
        )

        url = (
            "https://clientbp.common.ggbluefox.com/"
            "GetPlayerPersonalShow"
        )

        headers = {
            'X-Unity-Version': '2018.4.11f1',
            'ReleaseVersion': 'OB52',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-GA': 'v1 1',
            'Authorization': f'Bearer {GeTToK()}',
            'Content-Length': '16',
            'User-Agent': 'Dalvik/2.1.0',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }

        response = requests.post(
            url,
            headers=headers,
            data=data,
            timeout=15,
            verify=False
        )

        if response.status_code not in [200, 201]:

            return "❌ Failed getting player info"

        packet = binascii.hexlify(
            response.content
        ).decode('utf-8')

        BesTo_data = json.loads(
            asyncio.run(
                DeCode_PackEt(packet)
            )
        )

        try:

            player_uid = str(
                BesTo_data["1"]["data"]["1"]["data"]
            )

            player_likes = (
                BesTo_data["1"]["data"]["21"]["data"]
            )

            player_name = (
                BesTo_data["1"]["data"]["3"]["data"]
            )

            player_server = (
                BesTo_data["1"]["data"]["5"]["data"]
            )

            player_level = (
                BesTo_data["1"]["data"]["6"]["data"]
            )

            return f'''

🔥 PLAYER INFO

Name : {player_name}
UID : {xMsGFixinG(player_uid)}
Likes : {xMsGFixinG(player_likes)}
Level : {player_level}
Server : {player_server}

'''

        except Exception as e:

            print(e)

            return "❌ Parsing failed"

    except Exception as e:

        print(f"❌ Player info error => {e}")

        traceback.print_exc()

        return "❌ Failed"

# ========================= DELETE FRIEND =========================

def DeLet_Uid(id, Tok):

    try:

        print(f'🔥 Removing => {id}')

        url = (
            'https://clientbp.common.ggbluefox.com/'
            'RemoveFriend'
        )

        headers = {
            'X-Unity-Version': '2018.4.11f1',
            'ReleaseVersion': 'OB52',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-GA': 'v1 1',
            'Authorization': f'Bearer {Tok}',
            'User-Agent': 'Dalvik/2.1.0',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }

        data = bytes.fromhex(
            asyncio.run(
                EnC_AEs(
                    f"08a7c4839f1e10{asyncio.run(EnC_Uid(id , Tp='Uid'))}"
                )
            )
        )

        ResPonse = requests.post(
            url,
            headers=headers,
            data=data,
            verify=False,
            timeout=15
        )

        if (
            ResPonse.status_code == 400
            and
            'BR_FRIEND_NOT_SAME_REGION'
            in ResPonse.text
        ):

            return (
                f'UID {xMsGFixinG(id)} '
                f'not same region'
            )

        elif ResPonse.status_code == 200:

            return (
                f'Success delete '
                f'{xMsGFixinG(id)}'
            )

        return 'Delete failed'

    except Exception as e:

        print(f"❌ Delete uid error => {e}")

        return "Delete error"

# ========================= UID CHECK =========================

def ChEck_The_Uid(id):

    try:

        Api = requests.get(
            "https://panel-g2ccathtf6gdcmdw.polandcentral-01.azurewebsites.net/Uids",
            timeout=15
        )

        if Api.status_code not in [200, 201]:

            return False

        lines = Api.text.splitlines()

        for i, line in enumerate(lines):

            if f' - Uid : {id}' in line:

                expire = None
                status = None

                for sub_line in lines[i:]:

                    if "Expire In" in sub_line:

                        expire = re.search(
                            r"Expire In\s*:\s*(.*)",
                            sub_line
                        ).group(1).strip()

                    if "Status" in sub_line:

                        status = re.search(
                            r"Status\s*:\s*(\w+)",
                            sub_line
                        ).group(1)

                    if expire and status:

                        return status, expire

        return False

    except Exception as e:

        print(f"❌ UID check error => {e}")

        return False
