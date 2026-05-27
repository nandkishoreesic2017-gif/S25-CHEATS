# ========================= FIXED LOOP SECTION =========================

import asyncio
import threading

app = Flask(__name__)

loop = asyncio.new_event_loop()

def start_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()

threading.Thread(
    target=start_loop,
    daemon=True
).start()

# ========================= FIXED SEND PACKET =========================

async def SEndPacKeT(OnLinE, ChaT, TypE, PacKeT):
    global online_writer, whisper_writer

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

# ========================= FIXED PERFORM EMOTE =========================

async def perform_emote(team_code: str, uids: list, emote_id: int):
    global key, iv, region, online_writer, BOT_UID

    try:

        if online_writer is None:
            return {
                "status": "error",
                "message": "Bot offline"
            }

        print("🔥 Joining squad...")

        EM = await GenJoinSquadsPacket(team_code, key, iv)

        await SEndPacKeT(
            None,
            online_writer,
            'OnLine',
            EM
        )

        await asyncio.sleep(2)

        print("🔥 Sending emotes...")

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

                await asyncio.sleep(0.4)

            except Exception as e:
                print(f"UID emote error => {e}")

        print("🔥 Leaving squad...")

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

        import traceback

        traceback.print_exc()

        return {
            "status": "error",
            "message": str(e)
        }

# ========================= FIXED JOIN API =========================

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

        result = future.result(timeout=30)

        return jsonify(result)

    except Exception as e:

        import traceback

        traceback.print_exc()

        return jsonify({
            "status": "error",
            "message": str(e)
        })

# ========================= FIXED MAIN =========================

async def MaiiiinE():

    global key
    global iv
    global region
    global BOT_UID

    BOT_UID = int('4962573853')

    Uid = '4428929944'

    Pw = '0CF80D0C7AC19A7527BDECBE765A678D57817F89509BD259165F4CE2C3CCBA9B'

    open_id, access_token = await GeNeRaTeAccEss(Uid, Pw)

    if not open_id:

        print("❌ Invalid account")

        return

    PyL = await EncRypTMajoRLoGin(
        open_id,
        access_token
    )

    MajoRLoGinResPonsE = await MajorLogin(PyL)

    if not MajoRLoGinResPonsE:

        print("❌ Login failed")

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

    print("🔥 Bot connected")

    equie_emote(ToKen, UrL)

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

    await asyncio.gather(
        task1,
        task2
    )

# ========================= FIXED START =========================

async def StarTinG():

    while True:

        try:

            await asyncio.wait_for(
                MaiiiinE(),
                timeout=7 * 60 * 60
            )

        except asyncio.TimeoutError:

            print("🔥 Token expired restarting...")

        except Exception as e:

            import traceback

            traceback.print_exc()

            await asyncio.sleep(5)

# ========================= START =========================

if __name__ == '__main__':

    asyncio.run(
        StarTinG()
    )
