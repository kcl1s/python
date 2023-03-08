from machine import Timer, Pin, PWM
from time import sleep

def s_update(t):
    for i in Slow_Servo.instancelist:
        i._move()

class Slow_Servo:
    instancelist = [] 
        
    def __init__(self,s_pin, pw_min=1600, pw_max=8200, pw_cur=4900):
        self.pwm = PWM(Pin(s_pin))
        self.pwm.freq(50)
        self.pw_min = pw_min
        self.pw_max = pw_max
        self.pw_cur = min(self.pw_max, max(self.pw_min, int(pw_cur)))
        self.pw_des = self.pw_cur
        self.tics_togo = 0
        Slow_Servo.instancelist.append(self)
        if len(Slow_Servo.instancelist) == 1:
            t = Timer(period=10, mode=Timer.PERIODIC,
                    callback=s_update)
    
    def _move(self):
        if self.tics_togo > 0:
            diff = self.pw_des - self.pw_cur
            self.pw_cur += int(diff / self.tics_togo)
            print(self.pw_cur)
            self.tics_togo -= 1
            self.pwm.duty_u16(self.pw_cur)
        
    def set_angle(self, angle, move_ms=0):
        angle = min(180, max(0, int(angle)))
        self.pw_des = int((angle - 0) * (self.pw_max - self.pw_min) / (180 - 0) + self.pw_min)
        print(self.pw_des)
        if move_ms < 0: move_ms = 0
        if move_ms == 0:
            self.tics_togo = 1
        else:
            self.tics_togo = int(move_ms / 10)
# end class--------------

servo1 = Slow_Servo(1)
servo2 = Slow_Servo(0)
try:
    while True:
        servo1.set_angle(170,2000)
        servo2.set_angle(20,2000)
        sleep(2.5)
        servo1.set_angle(1,2000)
        servo2.set_angle(50,2000)
        sleep(2.5)
except KeyboardInterrupt:
    machine.reset()