from pyftdi.ftdi import Ftdi


device = "DLOP-IO20"
ftdi = Ftdi()
ftdi.open_by_name(device)
ftdi.set_bitmode(0x0000, Ftdi.Bitmode.RESET)
ftdi.set_bitmode(0x0000, Ftdi.Bitmode.RESET)

### Check output status
status = ftdi.read_data(1)
print(status)