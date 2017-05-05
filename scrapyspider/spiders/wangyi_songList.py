import os
import json
import base64
from scrapy import Request
import codecs
from scrapy import FormRequest
from scrapy.spiders import Spider
from scrapyspider.items import SongItem, CommentItem, CommentListItem, ProxyItem
from Crypto.Cipher import AES
from scrapyspider.settings import PROXIES

class SongSpider(Spider):
    name = 'song_list'
    headers = {'Cookie': 'appver=1.5.0.75771;', 'Referer': 'http://music.163.com/'}
    proxy_list = []
    songList = []
    playList = []
    playListUrl = 'http://music.163.com/playlist'
    commentsUrl = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_185908/?csrf_token='

    @staticmethod
    def aes_encrypt(text, sec_key):
        pad = 16 - len(text) % 16
        new_pad = pad * chr(pad)
        text += new_pad
        encryptor = AES.new(sec_key, 2, '0102030405060708')
        cipher_text = encryptor.encrypt(text)
        cipher_text = base64.b64encode(cipher_text)
        ss = cipher_text.decode()
        return ss

    @staticmethod
    def rsa_encrypt(text, pub_key, modulus):
        text = text[::-1]
        ssss = str(codecs.encode(bytes(text, encoding="utf8"), 'hex_codec'), encoding="utf8")
        rs = int(ssss, 16) ** int(pub_key, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    @staticmethod
    def create_secret_key(size):
        return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size).decode('iso-8859-15'))))[0:16]

    def start_requests(self):
        proxy_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        }
        url = 'http://www.xicidaili.com/nn/'
        yield Request(url, headers=proxy_headers)

    def parse(self, response):
        tr_list = response.css("#ip_list tr")[2: 50]
        for i in tr_list:
            item = ProxyItem()
            item['ip_port'] = i.css("td::text").extract()[0] + ':' + i.css("td::text").extract()[1]
            item['user_pass'] = ''
            self.proxy_list.append(item)
            PROXIES.append(item)
        page_max = 0
        for i in range(0, page_max + 1):
            url = 'http://music.163.com/discover/playlist/?cat=%E5%85%A8%E9%83%A8&limit=35&offset=' + str(i * 35)
            yield Request(url, headers=self.headers, callback=self.get_playlist)

    def get_playlist(self, response):
        a_list = response.xpath('.//ul[@id="m-pl-container"]/li/p[@class="dec"]/a')
        # for a in a_list:
        #     play_list_id = a.xpath('@href').extract()[0].split('=')[1]
        #     self.playList.append(play_list_id)
        #     yield Request(self.playListUrl + '?id=' + str(play_list_id), headers=self.headers,
        #                   callback=lambda list_response: self.parse_list(list_response, play_list_id))
        a = a_list[0]
        play_list_id = a.xpath('@href').extract()[0].split('=')[1]
        self.playList.append(play_list_id)
        yield Request(self.playListUrl + '?id=' + str(play_list_id), headers=self.headers,
                      callback=lambda list_response: self.parse_list(list_response, play_list_id))

    @staticmethod
    def generator_url(song_id):
        return 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(song_id) + '/?csrf_token='

    def parse_list(self, response, play_list_id):

        """另一种获取方式"""
        # a_list = response.xpath('.//ul[@class="f-hide"]/li//a')
        # for a in a_list:
        #     song_id = a.xpath('@href').extract()[0].split('=')[1]
        #     song_name = a.xpath('text()').extract()[0]
        #     song_item = SongItem()
        #     song_item['id'] = song_id
        #     song_item['name'] = song_name

        b_list = json.loads(response.css('ul.f-hide + textarea::text').extract()[0])
        b = b_list[0]
        # for b in b_list:
        #     song_id = b['id']
        #     song_name = b['name']
        #     song_item = SongItem()
        #     song_item['id'] = song_id
        #     song_item['name'] = song_name
        #     song_item['singer'] = b['artists'][0]['name']
        #     song_item['singer_id'] = b['artists'][0]['id']
        #     self.songList.append(song_id)
        #     text = {'username': '', 'password': '', 'rememberLogin': 'true'}
        #     modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        #     nonce = '0CoJUm6Qyw8W8jud'
        #     pub_key = '010001'
        #     text = json.dumps(text)
        #     sec_key = self.create_secret_key(16)
        #     enc_text = self.aes_encrypt(self.aes_encrypt(text, nonce), sec_key)
        #     enc_sec_key = self.rsa_encrypt(sec_key, pub_key, modulus)
        #     data = {'params': enc_text, 'encSecKey': enc_sec_key}
        #     yield FormRequest(self.generator_url(song_id),
        #                       formdata=data,
        #                       headers=self.headers,
        #                       callback=lambda comment_response: self.get_all_comments(comment_response, song_item))
        song_id = b['id']
        song_name = b['name']
        song_item = SongItem()
        song_item['id'] = song_id
        song_item['name'] = song_name
        song_item['singer'] = b['artists'][0]['name']
        song_item['singer_id'] = b['artists'][0]['id']
        self.songList.append(song_id)
        text = {'username': '', 'password': '', 'rememberLogin': 'true'}
        modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        nonce = '0CoJUm6Qyw8W8jud'
        pub_key = '010001'
        text = json.dumps(text)
        sec_key = self.create_secret_key(16)
        enc_text = self.aes_encrypt(self.aes_encrypt(text, nonce), sec_key)
        enc_sec_key = self.rsa_encrypt(sec_key, pub_key, modulus)
        data = {'params': enc_text, 'encSecKey': enc_sec_key}
        yield FormRequest(self.generator_url(song_id),
                          formdata=data,
                          headers=self.headers,
                          callback=lambda comment_response: self.get_all_comments(comment_response, song_item))

    def parse_comments(self, response, song_item):
        data = json.loads(str(response.body, encoding="utf-8"))
        comments = data['comments']
        total = data['total']
        comment_list = CommentListItem()
        comment_list['song_id'] = song_item['id']
        comment_list['list'] = []
        for c in comments:
            item = CommentItem()
            item['id'] = c['commentId']
            item['time'] = c['time']
            item['content'] = c['content']
            item['user_name'] = c['user']['nickname']
            item['user_id'] = c['user']['userId']
            comment_list['list'].append(item)
        return comment_list


    def get_all_comments(self, response, song_item):
        song_id = song_item['id']
        data = json.loads(str(response.body, encoding="utf-8"))
        comments_num = data['total']
        if (comments_num % 20 == 0):
            page = comments_num / 20
        else:
            page = int(comments_num / 20) + 1
        modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        nonce = '0CoJUm6Qyw8W8jud'
        pub_key = '010001'
        text = {'username': '', 'password': '', 'rememberLogin': 'true', 'limit': "20"}
        for i in range(page):
            text['offset'] = str(i)
            text = json.dumps(text)
            sec_key = self.create_secret_key(16)
            enc_text = self.aes_encrypt(self.aes_encrypt(text, nonce), sec_key)
            enc_sec_key = self.rsa_encrypt(sec_key, pub_key, modulus)
            data = {'params': enc_text, 'encSecKey': enc_sec_key}
            yield FormRequest(self.generator_url(song_id),
                              formdata=data,
                              headers=self.headers,
                              callback=lambda comment_response: self.parse_comments(comment_response, song_item))

    @staticmethod
    def comment_log(song_item, comment_item):
        print(song_item['name'] + '-' + song_item['singer'] + ' : '
              + comment_item['content'] + '  by: ' + comment_item['user_name'])
