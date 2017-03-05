import time
import sys
import spidev

spi = spidev.SpiDev()
spi.open(0,0)

def readAdc(channel):
    adc = spi.xfer2([(0x07 if(channel & 0x04) else 0x06), (channel & 0x03) << 6, 0])
    data = ((adc[1] & 0x0f) << 8) | adc[2]
    return data

def convertVolts(data):
    volts = (data * 3.3) / float(4095)
    volts = round(volts,4)
    return volts

'''
def convertTemp(volts):
    temp = (100 * volts) - 50.0
    temp = round(temp,4)
    return temp
'''

if __name__ == '__main__':
    try:
        while True:
            data = readAdc(0)
            print("adc  : {:8} ".format(data))
            volts = convertVolts(data)
            #temp = convertTemp(volts)
            print("volts: {:8.2f}".format(volts))
            #print("temp : {:8.2f}".format(temp))

            time.sleep(1)
    except KeyboardInterrupt:
        spi.close()
        sys.exit(0)