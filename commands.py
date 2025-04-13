from serials import cat_ser
import serial

# 假设 cat_ser 是已经初始化的串口对象
cat_serial = cat_ser
sat_data_rx = "0000000000"
sat_data_tx = "0000000000"
real_data = "0000000000"
# x_freq, tx_freq, rx_mode, tx_mode = "0", "0", "0", "0"

# 在模块顶部定义模式映射字典
MODE_MAP = {
    "00": "USB",
    "01": "LSB",
    "02": "CW",
    "03": "CWR",
    "04": "AM",
    "08": "FM",
    "88": "FMN",
    "0A": "DIG",
    "0C": "SPEC"
}

# 状态命令字典映射
_STATUS_CMD_MAP = {
    "lock": {True: "00 00 00 00 00", False: "00 00 00 00 08"},
    "split": {True: "00 00 00 00 02", False: "00 00 00 00 08"},
    "clar": {True: "00 00 00 00 05", False: "00 00 00 00 85"},
    "ptt": {True: "00 00 00 00 08", False: "00 00 00 00 88"},
    "ctcss_status": {True: "0A 00 00 00 2A", False: "0A 00 00 00 8A"},
    "dcs_status": {True: "0A 00 00 00 0A", False: "0A 00 00 00 8A"}
}

# 模式命令字典映射
_MODE_CMD_MAP = {
    "LSB": "00 00 00 00 07",
    "USB": "01 00 00 00 07",
    "CW": "02 00 00 00 07",
    "CWR": "03 00 00 00 07",
    "AM": "04 00 00 00 07",
    "FM": "08 00 00 00 07",
    "FMN": "88 00 00 00 07",
    "DIG": "0A 00 00 00 07",
    "SPEC": "0C 00 00 00 07"
}

# 编解码器字典映射
_CODER_CMD_MAP = {
    "ctcss": {"dec": "3A", "enc": "4A"},
    "dcs": {"dec": "0B", "enc": "0C"}
}

def set_model(model):
    global spe_format
    if model == "FT-847":
        spe_format = True
    elif model == "others":
        spe_format = False

def _set_status(cmd_type, status):
    """统一处理布尔状态命令"""
    cmd = _STATUS_CMD_MAP[cmd_type][status]
    cat_serial.write(bytes.fromhex(cmd))

def set_lock(lock_status):
    # Type:bool
    # FT_847 do not support this action
    _set_status("lock", lock_status)

def set_ptt(status):
    # Type:bool
    _set_status("ptt", status)

def set_split(status):
    # Type:bool
    # opera code = 02, 08
    _set_status("split", status)

def set_clar(status):
    # Type:bool
    # opera code = 05
    _set_status("clar", status)

def set_ctcss_status(status):
    # Type:bool
    # opera code = 0A
    _set_status("ctcss_status", status)

def set_dcs_status(status):
    # Type:bool
    # opera code = 0A
    _set_status("dcs_status", status)

def set_mode(mode):
    # mode e.g.:USB(Type:String)
    # opera code = 07
    if cmd := _MODE_CMD_MAP.get(mode):
        cat_serial.write(bytes.fromhex(cmd))

# 符号化频率处理
def _handle_signed_freq(freq, pos_prefix, neg_prefix, cmd_suffix):
    """统一处理带符号的频率命令"""
    sign = freq[0]
    str_freq = freq[1:]
    prefix = pos_prefix if sign == "+" else neg_prefix
    cmd = f"{prefix}{str_freq}{cmd_suffix}"
    cat_serial.write(bytes.fromhex(cmd))
    cat_serial.write(bytes.fromhex(freq))

def set_clar_freq(freq):
    # e.g.:-12.34KHz = "-12 34"
    # e.g.:+12.34KHz = "+12 34"
    # Type:String
    # opera code = F5
    _handle_signed_freq(freq, "00 00", "01 00", "F5")

def set_repeater_offset(freq):
    # e.g.:+5.432100MHz = "+05432100"
    # e.g.:-5.432100MHz = "-05432100"
    # e.g.:OFF = "0"
    # Freq max = +-99 99 99 99 99(99.99999999MHz)
    # Type:String
    # opera code = 09, 49, 89
    if freq == "0":
        cat_serial.write(bytes.fromhex("00 00 00 00 89"))
    else:
        _handle_signed_freq(freq, "00 00 00 00 09", "00 00 00 00 49", "")

def _set_coder(coder_type, action):
    """统一处理编解码器命令"""
    if cmd := _CODER_CMD_MAP[coder_type].get(action):
        cat_serial.write(bytes.fromhex(f"0A 00 00 00 {cmd}"))

def set_ctcss_coder(coder):
    # Type:String
    # opera code:0A
    # e.g.:Decoder on = dec
    # e.g.:Encoder on = enc
    # If want to turn it off,please see set_ctcss_status.
    _set_coder("ctcss", coder)

def set_dcs_coder(coder):
    # Type:String
    # opera code:0A
    # e.g.:Decoder on = dec
    # e.g.:Encoder on = enc
    # If want to turn it off,please see set_dcs_status.
    _set_coder("dcs", coder)

def set_freq(freq):
    # 144/430 freq e.g.:435.12345MHz = "43512345"
    # HF/50MHz freq e.g.:50.31300MHz = "05031300"
    # Type:String
    global cat_serial
    cat_serial.write(bytes.fromhex(freq))

def set_vfo():
    # opera code = 81
    # use it to change vfo
    global cat_serial
    cat_serial.write(bytes.fromhex("00 00 00 00 81"))

def set_ctcss_freq(tx, rx):
    # Type:int
    # opera code:0B
    # e.g.:tx = 0885(88.5Hz), rx = 1000(100.0Hz)
    global cat_serial
    cat_serial.write(bytes.fromhex(str(tx)+str(rx)+"0B"))

def set_dcs_freq(tx, rx):
    # Type:int
    # opera code:0C
    # e.g.:tx = 0023(023), rx = 0371(371)
    global cat_serial
    cat_serial.write(bytes.fromhex(str(tx)+str(rx)+"0C"))

def _parse_binary_status(data_bin, status_map):
    """通用二进制状态解析工具"""
    status = {}
    for key, (start, end, converter) in status_map.items():
        bits = data_bin[start:end] if end else data_bin[start]
        status[key] = converter(bits)
    return status

def read_freq():
    # operaq code:P1
    global cat_serial, sat_data_rx, sat_data_tx, real_data  # , rx_freq, tx_freq, rx_mode, tx_mode
    cat_serial.write(bytes.fromhex("00 00 00 00 03"))
    data_byte = cat_serial.read(5)
    data = data_byte.hex()

    # 统一处理数据为空的情况
    if not data:
        cat_serial.write(bytes.fromhex("00 00 00 00 03"))
        real_data_byte = cat_serial.read(5)
        real_data = real_data_byte.hex()
        data_source, sat = (real_data, False)
    else:
        cat_serial.write(bytes.fromhex("00 00 00 00 13"))
        sat_data_rx = cat_serial.read(5).hex()
        cat_serial.write(bytes.fromhex("00 00 00 00 23"))
        sat_data_tx = cat_serial.read(5).hex()
        data_source, sat = (sat_data_rx, True), (sat_data_tx, True)

    # 统一解析频率和模式
    def _parse_freq_mode(source):
        freq = source[0:6]
        mode_code = source[7:9]
        return freq, MODE_MAP.get(mode_code, "unknown")

    rx_freq, rx_mode = _parse_freq_mode(sat_data_rx if sat else real_data)
    tx_freq, tx_mode = _parse_freq_mode(sat_data_tx if sat else real_data)
    return rx_freq, tx_freq, rx_mode, tx_mode, sat

def read_rx_status():
    global cat_serial, spe_format
    cat_serial.write(bytes.fromhex("00 00 00 00 E7"))
    data_byte = cat_serial.read(1)
    data_bin = '{:08b}'.format(int(data_byte.hex(), 16))

    # 定义状态位映射规则
    _RX_STATUS_MAP = {
        "spe_format": {
            "ptt_status": (0, 1, lambda b: b == "1"),
            "po_alc_data": (2, 7, lambda b: b)
        },
        "default": {
            "sql_status": (0, 1, lambda b: b == "1"),
            "tone_status": (1, 2, lambda b: b == "0"),
            "disc_status": (2, 3, lambda b: b == "0"),
            "s_metre": (4, 7, lambda b: b)
        }
    }

    # 动态选择映射表
    status_map = _RX_STATUS_MAP["spe_format"] if spe_format else _RX_STATUS_MAP["default"]
    parsed = _parse_binary_status(data_bin, status_map)

    # 返回结果（保留原有返回结构）
    if spe_format:
        return parsed["ptt_status"], parsed["po_alc_data"], None  # dummy_data 需根据实际需求补充
    else:
        return parsed["sql_status"], parsed["tone_status"], parsed["disc_status"], None, parsed["s_metre"]

def read_tx_status():
    global cat_serial, spe_format
    cat_serial.write(bytes.fromhex("00 00 00 00 F7"))
    data_byte = cat_serial.read(1)
    data_bin = '{:08b}'.format(int(data_byte.hex(), 16))

    # 定义状态位映射规则
    _TX_STATUS_MAP = {
        "spe_format": {
            "sql_status": (0, 1, lambda b: b == "1"),
            "tone_status": (1, 2, lambda b: b == "0"),
            "disc_status": (2, 3, lambda b: b == "0"),
            "s_meter_data": (3, 7, lambda b: b)
        },
        "default": {
            "ptt_status": (0, 1, lambda b: b == "1"),
            "hi_swr": (1, 2, lambda b: b == "1"),
            "split_status": (2, 3, lambda b: b == "0"),
            "po_alc_data": (4, 7, lambda b: b)
        }
    }

    # 动态选择映射表
    status_map = _TX_STATUS_MAP["spe_format"] if spe_format else _TX_STATUS_MAP["default"]
    parsed = _parse_binary_status(data_bin, status_map)

    # 返回结果（保留原有返回结构）
    if spe_format:
        return parsed["sql_status"], parsed["tone_status"], parsed["disc_status"], parsed["s_meter_data"]
    else:
        return parsed["ptt_status"], parsed["hi_swr"], parsed["split_status"], None, parsed["po_alc_data"]