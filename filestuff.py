import shutil
import glob
import os
import datetime

stats=shutil.disk_usage('c:')
print ('Drive space for c: drive in bytes-', stats)

list_of_files = glob.glob('C:/Users/lohme/Pictures/*.*') # * means all if need specific format then *.csv
print ('Number of files ', len(list_of_files))
latest_file = max(list_of_files, key=os.path.getctime)
print('Newest File in Pictures directory ',latest_file)
epochTime=os.path.getctime(latest_file)
print ('seconds since 1/1/1970 ?? ',epochTime)
fileDate=datetime.datetime.fromtimestamp(epochTime)
print ('latest file created ',fileDate)