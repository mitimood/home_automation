import asyncio    
import requests
import json
from datetime import datetime

import time

from extra.aula import rodar
indice=0
tempo=None

def get_status():
  
  while True:
    global led,     led_2,    led_3,    led_4,    led_5,    led_6
    # Get the current time
    current_time = datetime.now()

    # Calculate the total minutes
    total_minutes = current_time.hour * 60 + current_time.minute

    url = "http://129.151.38.143:8000/predict"
    data = json.dumps({'room': 'sala', 'time': total_minutes})  # example data
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=data, headers=headers)

    response = response.json()

    status = True if response['prediction'] == 'on' else False

    if status:
      led.on()
      led_2.on()
      led_3.on()
      led_4.on()
      led_5.on()
      led_6.on()

    elif status:
      led.off()
      led_2.off()
      led_3.off()
      led_4.off()
      led_5.off()
      led_6.off()
    
    print(status)
    time.sleep(2)


@rodar
def main():
  global led, led_2, led_3, led_4, led_5, led_6

  from gpiozero import LED, Button, LightSensor, MotionSensor, Buzzer
  from Adafruit_CharLCD import Adafruit_CharLCD

  print('AAA')

  led = LED(21)
  led_2 = LED(22)
  led_3 = LED(23)
  led_4 = LED(24)
  led_5 = LED(25)
  led_6 = LED(26)

  botao1 = Button(5)
  
  alerta = Buzzer(16)
  alerta_2 = Buzzer(17)
  alerta_3 = Buzzer(19)
  alerta_4 = Buzzer(20)
  lcd = Adafruit_CharLCD(2,3,4,5,6,7,16,2)
  lcd_2 = Adafruit_CharLCD(2,3,4,5,6,8,16,2)
  light_sensor = LightSensor(8)
  movi_sensor = MotionSensor(27)

  lcd.message("      Bem \n     vindo!")
  lcd_2.message("      Bem \n     vindo!")

  # loop = asyncio.new_event_loop()

  # task = loop.create_task(get_status())


  def Ativar_Sensor():
    # intensidade_de_luz = light_sensor.value # valor entre 0 e 1
    movimento = movi_sensor.motion_detected # True ou False
    
    if movimento == True:
      lcd.clear()
      lcd.message("    Abriu a \n     Porta!")
      led.blink(n=1, on_time=0.3, off_time=0.5)
      led_3.blink(n=1, on_time=0.3, off_time=0.5)
      alerta.beep(n=1, on_time=0.3, off_time=0.3)
      alerta_2.beep(n=1, on_time=0.3, off_time=0.3)
      
  movi_sensor.when_motion = Ativar_Sensor

  def Desativou_Sensor():
    movimento = movi_sensor.motion_detected # True ou False
    if movimento == False:
      lcd.clear()
      lcd.message("    Fechou a \n     Porta!")
      led.blink(n=1, on_time=0.3, off_time=0.5)
      led_3.blink(n=1, on_time=0.3, off_time=0.5)
      alerta.beep(n=1, on_time=0.3, off_time=0.3)
      alerta_2.beep(n=1, on_time=0.3, off_time=0.3)
    
  movi_sensor.when_no_motion = Desativou_Sensor

  def ficou_claro():
    light_sensor.threshold = 0.5
    led_2.off()
    led_4.off()
    led_5.off()
    led_6.off()
    lcd_2.clear()
    lcd_2.message("   Amanheceu! \n   Bom Dia!")
    alerta_3.beep(n=1, on_time=0.3, off_time=0.3)

  light_sensor.when_light = ficou_claro

  def anoiteceu(x):
      print(led, x,)
      light_sensor.threshold = 0.5
      led_2.on()
      led_4.on()
      led_5.on()
      led_6.on()
      lcd_2.clear()
      lcd_2.message("   Anoiteceu!")
      alerta_4.beep(n=1, on_time=0.3, off_time=0.3)
      def dormir():
        led_2.off()
        led_4.off()
        led_5.off()
        led_6.off() 
        lcd_2.clear()
        lcd_2.message("   Boa Noite!")
      botao1.when_released = dormir

  light_sensor.when_dark = anoiteceu

  # loop.run_until_complete(task)
  # loop.close()

  get_status()

