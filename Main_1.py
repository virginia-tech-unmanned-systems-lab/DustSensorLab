
from machine import Pin, ADC
import utime

# Configuration constants
COV_RATIO = 0.2  # Conversion ratio: ug/mmm / mv
NO_DUST_VOLTAGE = 400  # No dust voltage level in mv
SYS_VOLTAGE = 3300  # System voltage

class Dust:
    def __init__(self):
        self.ADC_ConvertedValue = ADC(0)  # Initialize ADC for GPIO26
        self.DIN = Pin(22, Pin.OUT)  # Digital input pin
        self.conversion_factor = 3.3 / (65535)
        self.flag_first = 0
        self.buff = [0] * 10  # Initialize buffer
        self.sum1 = 0

    def Filter(self, ad_value):
        buff_max = 10
        if self.flag_first == 0:
            self.flag_first = 1
            for i in range(buff_max):
                self.buff[i] = ad_value
                self.sum1 += self.buff[i]
            return ad_value
        else:
            self.sum1 -= self.buff[0]
            for i in range(buff_max - 1):
                self.buff[i] = self.buff[i + 1]
            self.buff[9] = ad_value
            self.sum1 += self.buff[9]
            average_value = self.sum1 / 10.0
            return average_value

if __name__ == "__main__":
    dust_sensor = Dust()
    while True:
        dust_sensor.DIN.value(1)
        utime.sleep_us(280)
        AD_value = dust_sensor.ADC_ConvertedValue.read_u16()
        dust_sensor.DIN.value(0)
        AD_value = dust_sensor.Filter(AD_value)
        voltage = (SYS_VOLTAGE / 65536.0) * AD_value * 11
        if voltage >= NO_DUST_VOLTAGE:
            voltage -= NO_DUST_VOLTAGE
            density = voltage * COV_RATIO
        else:
            density = 0
        print(f"The current dust concentration is: {density:.2f} ug/m3")

        # Open the file in append mode and write the density value with description
        with open('dust_sensor_readings.txt', 'a') as file:
            timestamp = utime.time()
            file.write(f"Timestamp: {timestamp}, Dust concentration: {density:.2f} ug/m3\n")
        
        utime.sleep(1)

