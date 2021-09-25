from redis import Redis
rc = Redis(host='127.0.0.1', port=6379, db=0)
rc.pubsub()
res = {}
rc.publish('res', res)