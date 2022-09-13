import shutil
import glob
import os
import datetime
from RPLCD.i2c import CharLCD

stats=shutil.disk_usage('/')
print ('Drive space for root drive in bytes-', stats)

fileList = glob.glob('/home/pi/Pictures/*.*') # * means all if need specific format then *.csv
print ('Number of files ', len(fileList))
latestFile = max(fileList, key=os.path.getctime)
print('Newest File in Pictures directory ',latestFile)
epochTime=os.path.getctime(latestFile)
print ('seconds since 1/1/1970 ?? ',epochTime)
fileDate=datetime.datetime.fromtimestamp(epochTime)
print ('latest file created ',fileDate)

freeSpace='Free Space '+str(round((stats.free/10e9),2))+' GB'
newestFileName=latestFile.rsplit('/',1)[1]
numFiles='# Files- '+str(len(fileList))
shortDT=fileDate.strftime('%m/%d/%y %H:%M:%S')

lcd = CharLCD('PCF8574', 0x27)
lcd.cursor_pos=(0,0)
lcd.write_string(freeSpace)
lcd.cursor_pos=(1,0)
lcd.write_string(newestFileName)
lcd.cursor_pos=(2,0)
lcd.write_string(numFiles)
lcd.cursor_pos=(3,0)
lcd.write_string(shortDT)

# https://docs.python.org/3/library/shutil.html#shutil.disk_usage 
# https://docs.python.org/3/library/glob.html
# https://docs.python.org/3/library/os.path.html
# https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
# https://rplcd.readthedocs.io/en/stable/index.html