import requests, os, sys, time, urllib3, asyncio, aiohttp, ssl
from xC4 import *
from xHeaders import *
from datetime import datetime
from Pb2 import DEcwHisPErMsG_pb2, MajoRLoGinrEs_pb2, PorTs_pb2, MajoRLoGinrEq_pb2
from cfonts import render

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
ADMIN_UID = "8431487083"
BYPASS_TOKEN = "godpapa"

# Global Variables
online_writer = None
whisper_writer = None
connection_pool = None
bot_start_time = time.time()
join_loop_active = False
current_team_code = None

# Headers
Hr = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': 'v1 1',
    'ReleaseVersion': "OB51"
}

def is_admin(uid):
    return str(uid) == ADMIN_UID

# Crypto Functions
async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload

async def GeNeRaTeAccEss(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": (await Ua()),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    try:
        async with connection_pool.post(url, headers=Hr, data=data) as response:
            if response.status != 200:
                return None, None
            data = await response.json()
            open_id = data.get("open_id")
            access_token = data.get("access_token")
            return (open_id, access_token) if open_id and access_token else (None, None)
    except:
        return (None, None)

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = "1.118.1"
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return await encrypted_proto(string)

async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    try:
        async with connection_pool.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200:
                return await response.read()
            return None
    except:
        return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization'] = f"Bearer {token}"
    try:
        async with connection_pool.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200:
                return await response.read()
            return None
    except:
        return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto

async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9:
        headers = '0000000'
    elif uid_length == 8:
        headers = '00000000'
    elif uid_length == 10:
        headers = '000000'
    elif uid_length == 7:
        headers = '000000000'
    else:
        headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"

async def cHTypE(H):
    if not H:
        return 'Squid'
    elif H == 1:
        return 'CLan'
    elif H == 2:
        return 'PrivaTe'

async def SEndMsG(H, message, Uid, chat_id, key, iv):
    TypE = await cHTypE(H)
    if TypE == 'Squid':
        msg_packet = await xSEndMsgsQ(message, chat_id, key, iv)
    elif TypE == 'CLan':
        msg_packet = await xSEndMsg(message, 1, chat_id, chat_id, key, iv)
    elif TypE == 'PrivaTe':
        msg_packet = await xSEndMsg(message, 2, Uid, Uid, key, iv)
    return msg_packet

async def SEndPacKeT(OnLinE, ChaT, TypE, PacKeT):
    if TypE == 'ChaT' and ChaT:
        whisper_writer.write(PacKeT)
        await whisper_writer.drain()
    elif TypE == 'OnLine':
        online_writer.write(PacKeT)
        await online_writer.drain()
    else:
        return 'UnsoPorTed TypE ! >> ErrrroR (:():)'

async def join_leave_loop(team_code, key, iv, region, uid, chat_id, chat_type):
    """24/7 loop: join -> wait 35s -> leave -> join again -> repeat forever"""
    global join_loop_active
    
    loop_count = 0
    
    try:
        while join_loop_active:
            loop_count += 1
            
            # JOIN
            try:
                join_msg = f"[00FF00][B]🔄 Loop {loop_count}: Joining {team_code}"
                P = await SEndMsG(chat_type, join_msg, uid, chat_id, key, iv)
                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                
                print(f"\n{'='*60}")
                print(f"🔵 LOOP {loop_count} - JOINING TEAM: {team_code}")
                print(f"⏰ Time: {time.strftime('%H:%M:%S')}")
                print(f"{'='*60}")
                
                join_packet = await GenJoinSquadsPacket(team_code, key, iv)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
                
                # Wait 35 seconds in group with live countdown
                status_msg = f"[FFD700][B]⏳ In Group: {team_code} (35s)"
                P = await SEndMsG(chat_type, status_msg, uid, chat_id, key, iv)
                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                
                print(f"✅ JOINED SUCCESSFULLY!")
                print(f"⏳ Waiting in group for 35 seconds...")
                
                # Live countdown in console
                for remaining in range(35, 0, -1):
                    if not join_loop_active:
                        break
                    print(f"⏱️  Time Remaining: {remaining}s", end='\r', flush=True)
                    await asyncio.sleep(1)
                
                print(f"\n✅ 35 seconds completed!")
                
            except Exception as e:
                print(f"❌ JOIN ERROR: {e}")
            
            if not join_loop_active:
                break
            
            # LEAVE
            try:
                leave_msg = f"[FF6347][B]🚪 Leaving {team_code} (Loop {loop_count})"
                P = await SEndMsG(chat_type, leave_msg, uid, chat_id, key, iv)
                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                
                print(f"\n🔴 LEAVING TEAM: {team_code}")
                print(f"⏰ Time: {time.strftime('%H:%M:%S')}")
                
                leave_packet = await ExiT(None, key, iv)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
                
                print(f"✅ LEFT SUCCESSFULLY!")
                print(f"⏳ Waiting 2s before rejoining...")
                
                await asyncio.sleep(2)  # Small delay before rejoining
                
            except Exception as e:
                print(f"❌ LEAVE ERROR: {e}")
            
            if not join_loop_active:
                break
        
        # Final message when stopped
        final_msg = f"[FF0000][B]⛔ Stopped! Total Loops: {loop_count}"
        P = await SEndMsG(chat_type, final_msg, uid, chat_id, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
        
        print(f"\n{'='*60}")
        print(f"🛑 LOOP STOPPED!")
        print(f"📊 Total Loops Completed: {loop_count}")
        print(f"⏰ Stopped At: {time.strftime('%H:%M:%S')}")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"❌ LOOP ERROR: {e}")
    finally:
        join_loop_active = False

async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=0.5):
    global online_writer
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            online_writer.write(bytes_payload)
            await online_writer.drain()
            
            while True:
                data2 = await reader.read(9999)
                if not data2:
                    break
                
                if data2.hex().startswith('0500') and len(data2.hex()) > 1000:
                    try:
                        packet = await DeCode_PackEt(data2.hex()[10:])
                        packet = json.loads(packet)
                        OwNer_UiD, CHaT_CoDe, SQuAD_CoDe = await GeTSQDaTa(packet)
                        
                        JoinCHaT = await AutH_Chat(3, OwNer_UiD, CHaT_CoDe, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', JoinCHaT)
                        
                        message = f'[B][C][00FF00]\n🎯 LEVEL UP BOT Online!\n[00FF00]Use: /help for commands\n[FFFFFF]━━━━━━━━━━━━━\n[808080]TELEGRAM: @GODJEXARYT'
                        P = await SEndMsG(0, message, OwNer_UiD, OwNer_UiD, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                    except:
                        pass
            
            online_writer.close()
            await online_writer.wait_closed()
            online_writer = None
            
        except Exception as e:
            print(f"OnLine Error {ip}:{port} - {e}")
            online_writer = None
        await asyncio.sleep(reconnect_delay)

async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region, reconnect_delay=0.5):
    global whisper_writer, join_loop_active, current_team_code
    
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            whisper_writer.write(bytes_payload)
            await whisper_writer.drain()
            ready_event.set()
            
            if LoGinDaTaUncRypTinG.Clan_ID:
                clan_id = LoGinDaTaUncRypTinG.Clan_ID
                clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                print(f'\n - Bot in Clan: {clan_id}')
                pK = await AuthClan(clan_id, clan_compiled_data, key, iv)
                if whisper_writer:
                    whisper_writer.write(pK)
                    await whisper_writer.drain()
            
            while True:
                data = await reader.read(9999)
                if not data:
                    break
                
                if data.hex().startswith("120000"):
                    try:
                        response = await DecodeWhisperMessage(data.hex()[10:])
                        uid = response.Data.uid
                        chat_id = response.Data.Chat_ID
                        chat_type = response.Data.chat_type
                        inPuTMsG = response.Data.msg.lower().strip()
                    except:
                        response = None
                    
                    if response and is_admin(uid):
                        # /help COMMAND - Shows all commands
                        if inPuTMsG.startswith('/help'):
                            help_msg = (
                                f"[FFD700][B]━━━━━━━━━━━━━━━━━━━\n"
                                f"[FFFFFF][B]LEVEL UP BOT BY GOD JEXAR\n"
                                f"[FFD700]━━━━━━━━━━━━━━━━━━━\n\n"
                                f"[00FF00][B]Available Commands:\n\n"
                                f"[FFFFFF]/join [TEAM_CODE]\n"
                                f"[808080]Start auto join/leave loop\n"
                                f"[808080]Joins team every 35 seconds\n\n"
                                f"[FFFFFF]/stop\n"
                                f"[808080]Stop the active loop\n\n"
                                f"[FFFFFF]/help\n"
                                f"[808080]Show this help menu\n\n"
                                f"[FFD700]━━━━━━━━━━━━━━━━━━━\n"
                                f"[808080]TELEGRAM: @GODJEXARYT\n"
                                f"[FFD700]━━━━━━━━━━━━━━━━━━━"
                            )
                            P = await SEndMsG(chat_type, help_msg, uid, chat_id, key, iv)
                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                        
                        # /join COMMAND - Works in personal/clan/squad chat
                        elif inPuTMsG.startswith('/join '):
                            try:
                                parts = inPuTMsG.split()
                                if len(parts) >= 2:
                                    team_code = parts[1].upper()
                                    current_team_code = team_code
                                    
                                    # Start the join/leave loop
                                    join_loop_active = True
                                    
                                    start_msg = (
                                        f"[FFD700][B]━━━━━━━━━━━━━━━━━━━\n"
                                        f"[00FF00][B]🚀 LEVEL UP BOT ACTIVE\n"
                                        f"[FFD700]━━━━━━━━━━━━━━━━━━━\n\n"
                                        f"[FFFFFF]📋 Team Code: [00FF00]{team_code}\n"
                                        f"[FFFFFF]⏱️  Loop Time: [00FF00]35 Seconds\n"
                                        f"[FFFFFF]🔄 Mode: [00FF00]Auto Join/Leave\n\n"
                                        f"[FF6347][B]⚠️ IMPORTANT:\n"
                                        f"[FFFFFF]Make sure you selected\n"
                                        f"[00FF00]LONE WOLF DUEL[FFFFFF] mode!\n\n"
                                        f"[FFD700]━━━━━━━━━━━━━━━━━━━\n"
                                        f"[808080]TELEGRAM: @GODJEXARYT\n"
                                        f"[FFD700]━━━━━━━━━━━━━━━━━━━"
                                    )
                                    P = await SEndMsG(chat_type, start_msg, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                    
                                    # Create background task for join/leave loop
                                    asyncio.create_task(join_leave_loop(team_code, key, iv, region, uid, chat_id, chat_type))
                                else:
                                    error_msg = f"[FF0000][B]❌ Usage: /join [TEAM_CODE]\n[FFFFFF]Example: /join ABC123"
                                    P = await SEndMsG(chat_type, error_msg, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            except Exception as e:
                                error_msg = f"[FF0000][B]❌ Join command error!"
                                P = await SEndMsG(chat_type, error_msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                        
                        # /stop COMMAND - Stops the join/leave loop
                        elif inPuTMsG.startswith('/stop'):
                            if join_loop_active:
                                join_loop_active = False
                                stop_msg = (
                                    f"[FF0000][B]━━━━━━━━━━━━━━━━━━━\n"
                                    f"[FF0000][B]⛔ BOT STOPPED!\n"
                                    f"[FF0000]━━━━━━━━━━━━━━━━━━━\n\n"
                                    f"[FFFFFF]Loop stopped for: [FFD700]{current_team_code}\n\n"
                                    f"[808080]TELEGRAM: @GODJEXARYT\n"
                                    f"[FF0000]━━━━━━━━━━━━━━━━━━━"
                                )
                                P = await SEndMsG(chat_type, stop_msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            else:
                                stop_msg = f"[FFB300][B]⚠️ No active loop to stop!\n[FFFFFF]Use /join first"
                                P = await SEndMsG(chat_type, stop_msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
            
            whisper_writer.close()
            await whisper_writer.wait_closed()
            whisper_writer = None
            
        except Exception as e:
            print(f"Chat Error {ip}:{port} - {e}")
            whisper_writer = None
        await asyncio.sleep(reconnect_delay)

async def MaiiiinE():
    global connection_pool
    
    connection_pool = aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=20),
        connector=aiohttp.TCPConnector(limit=20, limit_per_host=10)
    )
    
    Uid, Pw = '4326340563', 'GODJEXAR_RGS82PGBV'
    
    open_id, access_token = await GeNeRaTeAccEss(Uid, Pw)
    if not open_id or not access_token:
        print("Error - Invalid Account")
        return None
    
    PyL = await EncRypTMajoRLoGin(open_id, access_token)
    MajoRLoGinResPonsE = await MajorLogin(PyL)
    if not MajoRLoGinResPonsE:
        print("Account Banned / Not Registered!")
        return None
    
    MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
    UrL = MajoRLoGinauTh.url
    region = MajoRLoGinauTh.region
    ToKen = MajoRLoGinauTh.token
    TarGeT = MajoRLoGinauTh.account_uid
    key = MajoRLoGinauTh.key
    iv = MajoRLoGinauTh.iv
    timestamp = MajoRLoGinauTh.timestamp
    
    LoGinDaTa = await GetLoginData(UrL, PyL, ToKen)
    if not LoGinDaTa:
        print("Error - Getting Ports From Login Data!")
        return None
    
    LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
    OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
    ChaTPorTs = LoGinDaTaUncRypTinG.AccountIP_Port
    OnLineiP, OnLineporT = OnLinePorTs.split(":")
    ChaTiP, ChaTporT = ChaTPorTs.split(":")
    acc_name = LoGinDaTaUncRypTinG.AccountName
    
    equie_emote(ToKen, UrL)
    AutHToKen = await xAuThSTarTuP(int(TarGeT), ToKen, int(timestamp), key, iv)
    ready_event = asyncio.Event()
    
    task1 = asyncio.create_task(TcPChaT(ChaTiP, ChaTporT, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region))
    
    await ready_event.wait()
    await asyncio.sleep(1)
    
    task2 = asyncio.create_task(TcPOnLine(OnLineiP, OnLineporT, key, iv, AutHToKen))
    
    os.system('clear')
    print(render('LEVEL UP', colors=['white', 'green'], align='center'))
    print(f"\n - LEVEL UP BOT BY GOD JEXAR Online: {TarGeT} | {acc_name}")
    print(f" - Status: ONLINE | Ready for commands")
    print(f" - Admin UID: {ADMIN_UID}")
    print(f" - Use /help to see all commands")
    print(f" - TELEGRAM: @GODJEXARYT")
    
    await asyncio.gather(task1, task2)

async def StarTinG():
    while True:
        try:
            await asyncio.wait_for(MaiiiinE(), timeout=7 * 60 * 60)
        except asyncio.TimeoutError:
            print("Token Expired! Restarting...")
        except Exception as e:
            print(f"TCP Error - {e} => Restarting...")

if __name__ == '__main__':
    asyncio.run(StarTinG())