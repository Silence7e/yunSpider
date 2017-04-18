import os, json
import base64
# import requests
from scrapy import Request
import codecs
from scrapy import FormRequest
from scrapy.spiders import Spider
from scrapyspider.items import SongItem
from Crypto.Cipher import AES
# from prettytable import PrettyTable
# import warnings

class SongSpider(Spider):
    name = 'song_spider'
    headers = {'Cookie': 'appver=1.5.0.75771;', 'Referer': 'http://music.163.com/'}

    # 由于网易云音乐歌曲评论采取AJAX填充的方式所以在HTML上爬不到，需要调用评论API，而API进行了加密处理，下面是相关解决的方法
    def aesEncrypt(self, text, secKey):
        pad = 16 - len(text) % 16
        newPad = pad * chr(pad)
        text = text + newPad
        encryptor = AES.new(secKey, 2, '0102030405060708')
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext)
        ss = ciphertext.decode()
        return ss

    def rsaEncrypt(self, text, pubKey, modulus):
        text = text[::-1]
        ssss = str(codecs.encode(bytes(text, encoding="utf8"), 'hex_codec'), encoding="utf8")
        rs = int(ssss, 16) ** int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def createSecretKey(self, size):
        return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size).decode('iso-8859-15'))))[0:16]


    def start_requests(self):
        url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_185908/?csrf_token='
        text = {'username': '', 'password': '', 'rememberLogin': 'true'}
        modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        nonce = '0CoJUm6Qyw8W8jud'
        pubKey = '010001'
        text = json.dumps(text)
        secKey = self.createSecretKey(16)
        # secKey = '551e1d6d9864b016'
        encText = self.aesEncrypt(self.aesEncrypt(text, nonce), secKey)
        encSecKey = self.rsaEncrypt(secKey, pubKey, modulus)
        data = {'params': encText, 'encSecKey': encSecKey}
        # req = requests.post(url, headers=self.headers, data=data)
        yield FormRequest(url, formdata=data, headers=self.headers)

    def parse(self, response):
        item = SongItem()
        data = json.loads(str(response.body, encoding="utf-8"))
        item['name'] = data['total']
        print(data)
        print(item['name'])
