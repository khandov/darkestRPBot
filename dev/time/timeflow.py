import time
from datetime import timedelta
import main
def update_date(start_time, multiplier):
    main.rpTime = start_time.strftime("%Y-%m-%d")
    while True:
        time.sleep(60) #1m upadate
        simulated_time = start_time + timedelta(seconds=60 * multiplier)
        main.rpTime = simulated_time.strftime("%Y-%m-%d")
        print(main.rpTime)