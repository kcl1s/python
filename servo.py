from machine import Pin, PWM
from time import sleep

class Servo:
    
    def __init__(self, s_pin, us_min=500, us_max=2500, min_pos=0, max_pos=180):
        self.pwm = PWM(Pin(s_pin))
        self.pwm.freq(50)
        self.pw_min = us_min * 65535 / 20000
        self.pw_max = us_max * 65535 / 20000
        self.min_pos = min_pos
        self.max_pos = max_pos
        self.slope = (self.pw_max - self.pw_min) / (self.max_pos - self.min_pos)
        
    def set_pos(self, pos):
        pos = min(self.max_pos, max(self.min_pos, pos))
        self.pw_des = int((pos - self.min_pos) * self.slope + self.pw_min)
        self.pwm.duty_u16(self.pw_des)
        
# end class--------------
if __name__ == '__main__':
    servo1 = Servo(16)
    try:
        while True:
            servo1.set_pos(180)
            sleep(2)
            servo1.set_pos(90)
            sleep(2)
            servo1.set_pos(0)
            sleep(2)
    except KeyboardInterrupt:
        machine.reset()
        