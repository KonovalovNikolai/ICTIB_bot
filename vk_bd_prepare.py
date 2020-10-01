from redis import Redis
from Misc import B

ID_G = {B.VK1: 48632629, B.VK2: 47535294, B.VK3: 177747188}

k = 1
vk = "vk"
with Redis(db=3, password='QzEcTb123789') as db:
    for i in ID_G.keys():
        db.hset(vk + str(k), "Name", i)
        db.hset(vk + str(k), "ID", ID_G[i])
        db.hset(vk + str(k), "Post", 0)  # db.get(k))
        k += 1
