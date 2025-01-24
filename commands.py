from serials import cat_ser
import serial

# 假设 cat_ser 是已经初始化的串口对象
cat_serial = cat_ser

def set_lock(lock_status):
    # Type:bool
    # FT_847 do not support this action
    global cat_serial
    if lock_status:
        cat_serial.write(bytes.fromhex("00 00 00 00 00"))
    elif not lock_status:
        cat_serial.write(bytes.fromhex("00 00 00 00 08"))

def set_ptt(status):
    # Type:bool
    global cat_serial
    if status:
        cat_serial.write(bytes.fromhex("00 00 00 00 08"))
    elif not status:
        cat_serial.write(bytes.fromhex("00 00 00 00 88"))

def set_freq(freq):
    # 144/430 freq e.g.:435.12345MHz = "43512345"
    # HF/50MHz freq e.g.:50.31300MHz = "05031300"
    # Type:String
    global cat_serial
    cat_serial.write(bytes.fromhex(freq))

def set_mode(mode):
    # mode e.g.:USB(Type:String)
    # opera code = 07
    global cat_serial
    mode_code = ""
    if mode == "USB":
        mode_code = "01 00 00 00 07"
    elif mode == "LSB":
        mode_code = "00 00 00 00 07"
    elif mode == "CW":
        mode_code = "02 00 00 00 07"
    elif mode == "CWR":
        mode_code = "03 00 00 00 07"
    elif mode == "AM":
        mode_code = "04 00 00 00 07"
    elif mode == "FM":
        mode_code = "08 00 00 00 07"
    elif mode == "FMN":
        mode_code = "88 00 00 00 07"
    elif mode == "DIG":
        mode_code = "0A 00 00 00 07"
    elif mode == "SPEC":
        mode_code = "0C 00 00 00 07"
    cat_serial.write(bytes.fromhex(mode_code))

def set_clar(status):
    # Type:bool
    # opera code = 05
    global cat_serial
    if status:
        cat_serial.write(bytes.fromhex("00 00 00 00 05"))
    elif not status:
        cat_serial.write(bytes.fromhex("00 00 00 00 85"))

def set_clar_freq(freq):
    #e.g.:-12.34KHz = "-12 34"
    # e.g.:+12.34KHz = "+12 34"
    # Type:String
    # opera code = F5
    global cat_serial
    if freq[1] == "+":
        str_freq = freq[1:]
        cat_serial.write(bytes.fromhex("00 00"+str_freq+"F5"))
        cat_serial.write(bytes.fromhex(freq))
    elif freq[1] == "-":
        str_freq = freq[1:]
        cat_serial.write(bytes.fromhex("01 00"+str_freq+"F5"))
        cat_serial.write(bytes.fromhex(freq))

def set_vfo():
    # opera code = 81
    # use it to change vfo
    global cat_serial
    cat_serial.write(bytes.fromhex("00 00 00 00 81"))

def set_split(status):
    # Type:bool
    # opera code = 02, 08
    global cat_serial
    if status:
        cat_serial.write(bytes.fromhex("00 00 00 00 02"))
    elif not status:
        cat_serial.write(bytes.fromhex("00 00 00 00 08"))

def set_repeater_offset(freq):
    # e.g.:+5.432100MHz = "+05432100"
    # e.g.:-5.432100MHz = "-05432100"
    # e.g.:OFF = "0"
    # Freq max = +-99 99 99 99 99(99.99999999MHz)
    # Type:String
    # opera code = 09, 49, 89
    global cat_serial
    if freq[1] == "+":
        str_freq = freq[1:]
        cat_serial.write(bytes.fromhex("00 00 00 00 09"))
        cat_serial.write(bytes.fromhex(str_freq))
    elif freq[1] == "-":
        str_freq = freq[1:]
        cat_serial.write(bytes.fromhex("00 00 00 00 49"))
        cat_serial.write(bytes.fromhex(str_freq))
    elif freq == "0":
        cat_serial.write(bytes.fromhex("00 00 00 00 89"))
        
def set_ctcss_status(status):
    # Type:bool
    # opera code = 0A
    global cat_serial
    if status:
        cat_serial.write(bytes.fromhex("0A 00 00 00 2A"))
    elif not status:
        cat_serial.write(bytes.fromhex("0A 00 00 00 8A"))

def set_dcs_status(status):
    # Type:bool
    # opera code = 0A
    global cat_serial
    if status:
        cat_serial.write(bytes.fromhex("0A 00 00 00 0A"))
    elif not status:
        cat_serial.write(bytes.fromhex("0A 00 00 00 8A"))

def set_ctcss_coder(coder):
    # Type:String
    # opera code:0A
    # e.g.:Decoder on = dec
    # e.g.:Encoder on = enc
    # If want to turn it off,please see set_ctcss_status.
    global cat_serial
    if coder == "dec":
        cat_serial.write(bytes.fromhex("0A 00 00 00 3A"))
    elif coder == "enc":
        cat_serial.write(bytes.fromhex("0A 00 00 00 4A"))

def set_dcs_coder(coder):
    # Type:String
    # opera code:0A
    # e.g.:Decoder on = dec
    # e.g.:Encoder on = enc
    # If want to turn it off,please see set_dcs_status.
    global cat_serial
    if coder == "dec":
        cat_serial.write(bytes.fromhex("0A 00 00 00 0B"))
    elif coder == "enc":
        cat_serial.write(bytes.fromhex("0A 00 00 00 0C"))

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



# Read status will be finished in the future.