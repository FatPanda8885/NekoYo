from commands import *
from serials import *

# cat_ser.timeout = 1
set_port("COM5")
set_baudrate(4800)
set_model("FT-847")
data = read_rx_status()
print(data)