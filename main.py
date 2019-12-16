from m5stack import *
from m5ui import *
from uiflow import *
import wifiCfg
import socket
import network
import hat

lcd.setRotation(1)
setScreenColor(0x000000)
axp.setLcdBrightness(25)

wifiCfg.screenShow()
wifiCfg.autoConnect(lcdShow = True)

hat_env0 = hat.get(hat.ENV)
wlan = network.WLAN(network.STA_IF)
networkinfo = str(wlan.ifconfig()[0])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

lcd.clear()
lcd.print('Listening on...', 0, 0, 0xFFFFFF)
lcd.print('\n' + (networkinfo))

def getDatetimeISOFormat():
  year = str((rtc.now()[0]))
  month = str('%02d' % (rtc.now()[1]))
  date = str('%02d' % (rtc.now()[2]))
  hour = str('%02d' % (rtc.now()[3]))
  minute = str('%02d' % (rtc.now()[4]))
  second = str('%02d' % (rtc.now()[5]))
  isoformat = year + '-' + month + '-' + date + 'T' + hour + ':' + minute + ':' + second + '+09:00'
  return isoformat

def getJsonEnvData():
  temperature = ('%.1f' % (hat_env0.temperature))
  humidity = ('%.1f' % (hat_env0.humidity))
  pressure = ('%.1f' % (hat_env0.pressure))
  captureddatetime = getDatetimeISOFormat()
  ret = '{"temperature":{"value":%s,"type":"Float"},"humidity":{"value":%s,"type":"Float"},"pressure":{"value":%s,"type":"Float"},"captureddatetime":{"value":"%s","type":"Datetime"}}' % (temperature,humidity,pressure,captureddatetime)
  return ret

def buttonB_wasPressed():
  temperature = ('%.1f' % (hat_env0.temperature))
  humidity = ('%.1f' % (hat_env0.humidity))
  pressure = ('%.1f' % (hat_env0.pressure))
  captureddatetime = getDatetimeISOFormat()

  lcd.clear()
  lcd.print('Temperature: ' + temperature + '\n', 0, 0, 0xFFFFFF)
  lcd.print('Humidity: ' + humidity + '\n')
  lcd.print('Pressure: ' + pressure + '\n')
  lcd.print(captureddatetime)

btnB.wasPressed(buttonB_wasPressed)

try:
  while True:
    conn, addr = s.accept()
    response = (getJsonEnvData())
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: application/json\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()

    lcd.clear()
    lcd.print('Return Data:\n' + (getDatetimeISOFormat()), 0, 0, 0xFFFFFF)
    lcd.print('\nListening on...')
    lcd.print('\n' + (networkinfo))

except Exception as e:
    lcd.clear()
    lcd.print(str(e), 0, 0, 0xFFFFFF)
