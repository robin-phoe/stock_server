from redis import Redis
import time
rc = Redis(host='127.0.0.1', port=6379, db=0)
ps = rc.pubsub()
ps.subscribe(['res'])
i = 0
for item in ps.listen():
   print(item)
   i += 1
   time.sleep(10)
print('2')