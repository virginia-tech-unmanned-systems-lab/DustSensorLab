'''
******************************************************************************
  * @file    Dust Sensor.py
  * @author  Waveshare Team
  * @version 
  * @date    2021-09-07
  * @brief   Dust Sensor
  ******************************************************************************
  * @attention
  *
  * THE PRESENT FIRMWARE WHICH IS FOR GUIDANCE ONLY AIMS AT PROVIDING CUSTOMERS
  * WITH CODING INFORMATION REGARDING THEIR PRODUCTS IN ORDER FOR THEM TO SAVE
  * TIME. AS A RESULT, WAVESHARE SHALL NOT BE HELD LIABLE FOR ANY
  * DIRECT, INDIRECT OR CONSEQUENTIAL DAMAGES WITH RESPECT TO ANY CLAIMS ARISING
  * FROM THE CONTENT OF SUCH FIRMWARE AND/OR THE USE MADE BY CUSTOMERS OF THE
  * CODING INFORMATION CONTAINED HEREIN IN CONNECTION WITH THEIR PRODUCTS.
  *
  ******************************************************************************
'''


from machine import Pin,ADC
import utime

#Select ADC input 0 (GPIO26)
COV_RATIO     =  0.2 #ug/mmm / mv
NO_DUST_VOLTAGE = 400  #mv
SYS_VOLTAGE = 3300


class Dust:
    def __init__(self):
         #Select ADC input 0 (GPIO26)
        self.ADC_ConvertedValue = machine.ADC(0)
        self.DIN = Pin(22,Pin.OUT)
        self.conversion_factor = 3.3 / (65535)
        self.flag_first = 0
        self.buff = [0,0,0,0,0,0,0,0,0,0]
        self.sum1 = 0
    def Filter(self,ad_value):      
        buff_max = 10
        if self.flag_first == 0:
            self.flag_first = 1
            for i in range (buff_max):
                self.buff[i] = ad_value
                self.sum1 = self.sum1+self.buff[i]
            return ad_value
        else:
            self.sum1 = self.sum1-self.buff[0]
            for i in range (buff_max-1):
                self.buff[i] = self.buff[i+1]
            self.buff[9] = ad_value
            self.sum1 = self.sum1 + self.buff[9]
            i = self.sum1 / 10.0
            return i
        
if __name__ == "__main__":
    Dust=Dust()
    while True :
        Dust.DIN.value(1 )
        utime.sleep_us(280)
        AD_value = Dust.ADC_ConvertedValue.read_u16()
        Dust.DIN.value(0)
        AD_value = Dust.Filter(AD_value)
        voltage = (SYS_VOLTAGE / 65536.0) * AD_value * 11
        if voltage >= NO_DUST_VOLTAGE:
            voltage = voltage - NO_DUST_VOLTAGE
            density = voltage * COV_RATIO
        else:
            density = 0
        print("The current dust concentration is:",density,"ug/m3\n")      
        utime.sleep(1)
