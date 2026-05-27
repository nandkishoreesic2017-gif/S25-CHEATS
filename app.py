# ========================= FIXED LOOP SECTION =========================

import asyncio
import threading
import traceback
import os

from flask import Flask, request, jsonify

from xC4 import *
from xHeaders import *

app = Flask(__name__)

loop = asyncio.new_event_loop()

def start_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()

threading.Thread(
    target=start_loop,
    daemon=True
).start()

# ========================= GLOBALS =========================

online_writer = None
whisper_writer = None
BOT_UID = 4962573853

# ========================= SAFE SEND PACKET =========================

async def SEndPacKeT(OnLinE, ChaT, TypE, PacKeT):

    global online_writer
    global whisper_writer

    try:

        if TypE == 'ChaT':

            if whisper_writer is None:
                print("❌ whisper_writer disconnected")
                return

            whisper_writer.write(PacKeT)
            await whisper_writer.drain()

        elif TypE == 'OnLine':

            if online_writer is None:
                print("❌ online_writer disconnected")
                return

            online_writer.write(PacKeT)
            await online_writer.drain()

        else:
            print("❌ Unsupported packet type")

    except Exception as e:
        print(f"❌ Packet send error => {e}")
        traceback.print_exc()

# ========================= ONLINE TCP =========================

async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=2):

    global online_writer

    while True:

        try:

            print(f"🔥 Connecting Online TCP {ip}:{port}")

            reader, writer = await asyncio.open_connection(
                ip,
                int(port)
            )

            online_writer = writer

            bytes_payload = bytes.fromhex(AutHToKen)

            online_writer.write(bytes_payload)

            await online_writer.drain()

            print("✅ Online socket connected")

            while True:

                data = await reader.read(9999)

                if not data:
                    break

            print("⚠️ Online socket disconnected")

            try:
                online_writer.close()
                await online_writer.wait_closed()
            except:
                pass

            online_writer = None

        except Exception as e:

            print(f"❌ Online socket error => {e}")

            traceback.print_exc()

            online_writer = None

        await asyncio.sleep(reconnect_delay)

# ========================= CHAT TCP =========================

async def TcPChaT(
    ip,
    port,
    AutHToKen,
    key,
    iv,
    LoGinDaTaUncRypTinG,
    ready_event,
    region,
    reconnect_delay=2
):

    global whisper_writer

    while True:

        try:

            print(f"🔥 Connecting Chat TCP {ip}:{port}")

            reader, writer = await asyncio.open_connection(
                ip,
                int(port)
            )

            whisper_writer = writer

            bytes_payload = bytes.fromhex(AutHToKen)

            whisper_writer.write(bytes_payload)

            await whisper_writer.drain()

            print("✅ Chat socket connected")

            ready_event.set()

            while True:

                data = await reader.read(9999)

                if not data:
                    break

            print("⚠️ Chat socket disconnected")

            try:
                whisper_writer.close()
                await whisper_writer.wait_closed()
            except:
                pass

            whisper_writer = None

        except Exception as e:

            print(f"❌ Chat socket error => {e}")

            traceback.print_exc()

            whisper_writer = None

        await asyncio.sleep(reconnect_delay)

# ========================= EMOTE SYSTEM =========================

async def perform_emote(team_code: str, uids: list, emote_id: int):

    global key
    global iv
    global region
    global BOT_UID

    try:

        if online_writer is None:

            return {
                "status": "error",
                "message": "Bot offline"
            }

        print("🔥 Joining squad")

        EM = await GenJoinSquadsPacket(
            team_code,
            key,
            iv
        )

        await SEndPacKeT(
            None,
            online_writer,
            'OnLine',
            EM
        )

        await asyncio.sleep(2)

        print("🔥 Sending emotes")

        for uid_str in uids:

            try:

                uid = int(uid_str)

                H = await Emote_k(
                    uid,
                    emote_id,
                    key,
                    iv,
                    region
                )

                await SEndPacKeT(
                    None,
                    online_writer,
                    'OnLine',
                    H
                )

                await asyncio.sleep(0.5)

            except Exception as e:

                print(f"❌ Emote UID error => {e}")

        print("🔥 Leaving squad")

        LV = await ExiT(
            BOT_UID,
            key,
            iv
        )

        await SEndPacKeT(
            None,
            online_writer,
            'OnLine',
            LV
        )

        await asyncio.sleep(1)

        return {
            "status": "success",
            "message": "Emote success"
        }

    except Exception as e:

        traceback.print_exc()

        return {
            "status": "error",
            "message": str(e)
        }

# ========================= FLASK =========================

@app.route("/")
def home():

    return "Bot Running 🚀"

@app.route('/join')
def join_team():

    global loop

    try:

        team_code = request.args.get("tc")

        uid1 = request.args.get("uid1")
        uid2 = request.args.get("uid2")
        uid3 = request.args.get("uid3")
        uid4 = request.args.get("uid4")
        uid5 = request.args.get("uid5")
        uid6 = request.args.get("uid6")

        emote_id_str = request.args.get("emote_id")

        if not team_code:

            return jsonify({
                "status": "error",
                "message": "Missing team code"
            })

        try:
            emote_id = int(emote_id_str)

        except:

            return jsonify({
                "status": "error",
                "message": "Invalid emote id"
            })

        uids = [
            uid for uid in
            [uid1, uid2, uid3, uid4, uid5, uid6]
            if uid
        ]

        if len(uids) == 0:

            return jsonify({
                "status": "error",
                "message": "No UIDs provided"
            })

        future = asyncio.run_coroutine_threadsafe(
            perform_emote(
                team_code,
                uids,
                emote_id
            ),
            loop
        )

        try:
    result = future.result(timeout=120)
        except Exception as e:
        return jsonify({
        "status": "error",
        "message": str(e)
    })

return jsonify(result)

        return jsonify(result)

    except Exception as e:

        traceback.print_exc()

        return jsonify({
            "status": "error",
            "message": str(e)
        })

# ========================= FLASK RUN =========================

def run_flask():

    port = int(
        os.environ.get("PORT", 10000)
    )

    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        use_reloader=False
    )

# ========================= MAIN =========================

async def MaiiiinE():

    global key
    global iv
    global region

    Uid = '4428929944'

    Pw = '0CF80D0C7AC19A7527BDECBE765A678D57817F89509BD259165F4CE2C3CCBA9B'

    print("🔥 Generating access token")

    open_id, access_token = await GeNeRaTeAccEss(
        Uid,
        Pw
    )

    if not open_id:

        print("❌ Invalid account")

        return

    PyL = await EncRypTMajoRLoGin(
        open_id,
        access_token
    )

    print("🔥 Major login")

    MajoRLoGinResPonsE = await MajorLogin(PyL)

    if not MajoRLoGinResPonsE:

        print("❌ Major login failed")

        return

    MajoRLoGinauTh = await DecRypTMajoRLoGin(
        MajoRLoGinResPonsE
    )

    UrL = MajoRLoGinauTh.url

    region = str(
        MajoRLoGinauTh.region
    ).lower().strip()

    ToKen = MajoRLoGinauTh.token

    TarGeT = MajoRLoGinauTh.account_uid

    key = MajoRLoGinauTh.key

    iv = MajoRLoGinauTh.iv

    timestamp = MajoRLoGinauTh.timestamp

    print("🔥 Getting login data")

    LoGinDaTa = await GetLoginData(
        UrL,
        PyL,
        ToKen
    )

    if not LoGinDaTa:

        print("❌ Login data failed")

        return

    LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(
        LoGinDaTa
    )

    OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port

    ChaTPorTs = LoGinDaTaUncRypTinG.AccountIP_Port

    OnLineiP, OnLineporT = OnLinePorTs.split(":")

    ChaTiP, ChaTporT = ChaTPorTs.split(":")

    print("🔥 Equipping emote")

    try:
        equie_emote(ToKen, UrL)
    except Exception as e:
        print(e)

    print("🔥 Generating auth token")

    AutHToKen = await xAuThSTarTuP(
        int(TarGeT),
        ToKen,
        int(timestamp),
        key,
        iv
    )

    ready_event = asyncio.Event()

    task1 = asyncio.create_task(
        TcPChaT(
            ChaTiP,
            ChaTporT,
            AutHToKen,
            key,
            iv,
            LoGinDaTaUncRypTinG,
            ready_event,
            region
        )
    )

    await ready_event.wait()

    await asyncio.sleep(1)

    task2 = asyncio.create_task(
        TcPOnLine(
            OnLineiP,
            OnLineporT,
            key,
            iv,
            AutHToKen
        )
    )

    flask_thread = threading.Thread(
        target=run_flask,
        daemon=True
    )

    flask_thread.start()

    print("✅ BOT ONLINE")

    await asyncio.gather(
        task1,
        task2
    )

# ========================= AUTO RESTART =========================

async def StarTinG():

    while True:

        try:

            await asyncio.wait_for(
                MaiiiinE(),
                timeout=7 * 60 * 60
            )

        except asyncio.TimeoutError:

            print("🔥 Token expired restarting")

        except Exception as e:

            print(f"❌ Main crash => {e}")

            traceback.print_exc()

        await asyncio.sleep(5)

# ========================= START =========================

if __name__ == '__main__':

    asyncio.run(
        StarTinG()
    )
