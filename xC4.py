# ========================= FULL FIXED xC4.py =========================

# By AbdeeLkarim BesTo - FIXED VERSION

import requests
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
import os
import asyncio

from protobuf_decoder.protobuf_decoder import Parser
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)

Key = bytes([
    89, 103, 38, 116,
    99, 37, 68, 69,
    117, 104, 54, 37,
    90, 99, 94, 56
])

Iv = bytes([
    54, 111, 121, 90,
    68, 114, 50, 50,
    69, 51, 121, 99,
    104, 106, 77, 37
])

# ========================= AES =========================

async def EnC_AEs(HeX):

    cipher = AES.new(
        Key,
        AES.MODE_CBC,
        Iv
    )

    return cipher.encrypt(
        pad(bytes.fromhex(HeX), AES.block_size)
    ).hex()

async def DEc_AEs(HeX):

    cipher = AES.new(
        Key,
        AES.MODE_CBC,
        Iv
    )

    return unpad(
        cipher.decrypt(bytes.fromhex(HeX)),
        AES.block_size
    ).hex()

async def EnC_PacKeT(HeX, K, V):

    return AES.new(
        K,
        AES.MODE_CBC,
        V
    ).encrypt(
        pad(bytes.fromhex(HeX), 16)
    ).hex()

async def DEc_PacKeT(HeX, K, V):

    return unpad(
        AES.new(
            K,
            AES.MODE_CBC,
            V
        ).decrypt(bytes.fromhex(HeX)),
        16
    ).hex()

# ========================= VARIANT =========================

async def EnC_Uid(H, Tp):

    e = []

    H = int(H)

    while H:

        e.append(
            (H & 0x7F) |
            (0x80 if H > 0x7F else 0)
        )

        H >>= 7

    if Tp == 'Uid':
        return bytes(e).hex()

    return None

async def EnC_Vr(N):

    if N < 0:
        return b''

    H = []

    while True:

        BesTo = N & 0x7F

        N >>= 7

        if N:
            BesTo |= 0x80

        H.append(BesTo)

        if not N:
            break

    return bytes(H)

def DEc_Uid(H):

    n = 0
    s = 0

    for b in bytes.fromhex(H):

        n |= (b & 0x7F) << s

        if not b & 0x80:
            break

        s += 7

    return n

# ========================= PROTO =========================

async def CrEaTe_VarianT(field_number, value):

    field_header = (field_number << 3) | 0

    return (
        await EnC_Vr(field_header)
        +
        await EnC_Vr(value)
    )

async def CrEaTe_LenGTh(field_number, value):

    field_header = (field_number << 3) | 2

    encoded_value = (
        value.encode()
        if isinstance(value, str)
        else value
    )

    return (
        await EnC_Vr(field_header)
        +
        await EnC_Vr(len(encoded_value))
        +
        encoded_value
    )

async def CrEaTe_ProTo(fields):

    packet = bytearray()

    for field, value in fields.items():

        if isinstance(value, dict):

            nested_packet = await CrEaTe_ProTo(value)

            packet.extend(
                await CrEaTe_LenGTh(
                    field,
                    nested_packet
                )
            )

        elif isinstance(value, int):

            packet.extend(
                await CrEaTe_VarianT(
                    field,
                    value
                )
            )

        elif isinstance(value, str) or isinstance(value, bytes):

            packet.extend(
                await CrEaTe_LenGTh(
                    field,
                    value
                )
            )

    return packet

# ========================= PACKET =========================

async def DecodE_HeX(H):

    R = hex(H)

    F = str(R)[2:]

    if len(F) == 1:
        F = "0" + F

    return F

async def GeneRaTePk(Pk, N, K, V):

    PkEnc = await EnC_PacKeT(
        Pk,
        K,
        V
    )

    _ = await DecodE_HeX(
        int(len(PkEnc) // 2)
    )

    if len(_) == 2:
        HeadEr = N + "000000"

    elif len(_) == 3:
        HeadEr = N + "00000"

    elif len(_) == 4:
        HeadEr = N + "0000"

    elif len(_) == 5:
        HeadEr = N + "000"

    else:
        raise Exception(
            "Packet generation failed"
        )

    return bytes.fromhex(
        HeadEr + _ + PkEnc
    )

# ========================= JOIN =========================

async def GenJoinSquadsPacket(code, K, V):

    fields = {
        1: 4,
        2: {
            4: bytes.fromhex(
                "01090a0b121920"
            ),
            5: str(code),
            6: 6,
            8: 1,
            9: {
                2: 800,
                6: 11,
                8: "1.111.1",
                9: 5,
                10: 1
            }
        }
    }

    return await GeneRaTePk(
        (await CrEaTe_ProTo(fields)).hex(),
        '0515',
        K,
        V
    )

# ========================= FIXED EMOTE =========================

async def Emote_k(
    TarGeT,
    idT,
    K,
    V,
    region
):

    try:

        region = str(
            region
        ).strip().lower()

        fields = {
            1: 21,
            2: {

                # FIXED sender uid
                1: int(TarGeT),

                # FIXED dynamic emote
                2: int(idT),

                5: {

                    1: int(TarGeT),

                    # FIXED emote id
                    3: int(idT),
                }
            }
        }

        if region in ["ind", "in"]:

            packet = '0514'

        elif region in ["bd", "ban"]:

            packet = "0519"

        else:

            packet = "0515"

        return await GeneRaTePk(
            (await CrEaTe_ProTo(fields)).hex(),
            packet,
            K,
            V
        )

    except Exception as e:

        print(f"❌ Emote error => {e}")

        return b''

# ========================= OPEN SQUAD =========================

async def OpEnSq(K, V, region):

    try:

        region = str(region).strip().lower()

        fields = {
            1: 1,
            2: {
                2: "\u0001",
                3: 1,
                4: 1,
                5: "en",
                9: 1,
                11: 1,
                13: 1,
                14: {
                    2: 5756,
                    6: 11,
                    8: "1.111.5",
                    9: 2,
                    10: 4
                }
            }
        }

        if region in ["ind", "in"]:

            packet = '0514'

        elif region in ["bd", "ban"]:

            packet = "0519"

        else:

            packet = "0515"

        return await GeneRaTePk(
            (await CrEaTe_ProTo(fields)).hex(),
            packet,
            K,
            V
        )

    except Exception as e:

        print(f"❌ Open squad error => {e}")

        return b''

# ========================= SEND INVITE =========================

async def SEnd_InV(
    Nu,
    Uid,
    K,
    V,
    region
):

    try:

        region = str(
            region
        ).strip().lower()

        fields = {
            1: 2,
            2: {
                1: int(Uid),
                2: region,
                4: int(Nu)
            }
        }

        if region in ["ind", "in"]:

            packet = '0514'

        elif region in ["bd", "ban"]:

            packet = "0519"

        else:

            packet = "0515"

        return await GeneRaTePk(
            (await CrEaTe_ProTo(fields)).hex(),
            packet,
            K,
            V
        )

    except Exception as e:

        print(f"❌ Invite error => {e}")

        return b''

# ========================= CHANGE SLOT =========================

async def cHSq(
    Nu,
    Uid,
    K,
    V,
    region
):

    try:

        region = str(
            region
        ).strip().lower()

        fields = {
            1: 17,
            2: {
                1: int(Uid),
                2: 1,
                3: int(Nu - 1),
                4: 62,
                5: "\u001a",
                8: 5,
                13: 329
            }
        }

        if region in ["ind", "in"]:

            packet = '0514'

        elif region in ["bd", "ban"]:

            packet = "0519"

        else:

            packet = "0515"

        return await GeneRaTePk(
            (await CrEaTe_ProTo(fields)).hex(),
            packet,
            K,
            V
        )

    except Exception as e:

        print(f"❌ Change slot error => {e}")

        return b''

# ========================= EXIT =========================

async def ExiT(idT, K, V):

    fields = {
        1: 7,
        2: {
            1: idT,
        }
    }

    return await GeneRaTePk(
        (await CrEaTe_ProTo(fields)).hex(),
        '0515',
        K,
        V
    )

# ========================= STATUS =========================

async def GeT_Status(
    PLayer_Uid,
    K,
    V
):

    PLayer_Uid = await EnC_Uid(
        PLayer_Uid,
        Tp='Uid'
    )

    if len(PLayer_Uid) == 8:

        Pk = (
            f'080112080a04'
            f'{PLayer_Uid}1005'
        )

    else:

        Pk = (
            f'080112090a05'
            f'{PLayer_Uid}1005'
        )

    return await GeneRaTePk(
        Pk,
        '0f15',
        K,
        V
    )
