from datetime import datetime
from pytz import timezone
tm = timezone('Moscow')
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
