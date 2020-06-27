"""
Read file into texts and calls.
It's ok if you don't understand how to read files
"""
import csv
with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)

"""
TASK 2: Which telephone number spent the longest time on the phone
during the period? Don't forget that time spent answering a call is
also time spent on the phone.
Print a message:
"<telephone number> spent the longest time, <total time> seconds, on the phone during 
September 2016.".
"""

from collections import defaultdict
from datetime import datetime

selected_calls = defaultdict(int)


for caller, reciever, timestamp, duration in calls:
    date = datetime.strptime(timestamp, "%d-%m-%Y %H:%M:%S")
    if date.year == 2016 and date.month == 9:
        selected_calls[caller] += int(duration)
        selected_calls[reciever] += int(duration)
		
max_duration = max(selected_calls.items(), key=lambda x: x[1])
print(f"{max_duration[0]} spent the longest time, {max_duration[1]} seconds, on the phone during September 2016.")