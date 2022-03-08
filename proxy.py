import asyncio
from proxybroker import Broker

proxy_list=[]
async def show(proxies):
    global proxy_list
    while True:
        proxy = await proxies.get()
        if proxy is None: break
        proto = 'https' if 'HTTPS' in proxy.types else 'http'
        row = '%s://%s:%d' % (proto, proxy.host, proxy.port)
        proxy_list.append(row)
        #print('Found proxy: %s' % proxy)

def get_proxy():
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(
        broker.find(types=['HTTP', 'HTTPS'], limit=10),
        show(proxies))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)
    return proxy_list

get_proxy()
print('Proxy list=',proxy_list)