import json

import requests
from lxml import etree
import re


def ip_proxy():
    url = 'http://api.ip.data5u.com/dynamic/get.html?order=78cefa327faa6e95ff2a1005f1bd3d4e&random=1&sep=3'
    resp = requests.get(url)
    proxies = {
        'https': 'https://' + resp.text.replace('/n', ''),
        'http': 'http://' + resp.text.replace('/n', ''),
    }
    return proxies



def data_proces(shopdata, typedata):
    shopimation = {}
    shopimation['商户名称'] = shopdata['name']
    shopimation['商户地址'] = shopdata['address']
    shopimation['商户联系方式'] = shopdata['phone']
    shopimation['商户营业时间'] = shopdata['openTime']

    shopimation['详细商户分类'] = ''
    for data in typedata:
        shopimation['详细商户分类'] = shopimation['详细商户分类'] + ' > ' + data['title']
    return shopimation



def pagings(link, type_name, whole_type):
    print(link, type_name, whole_type)
    for i in range(12, 100):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        }
        if 'https' not in link:
            link = link.replace('http', 'https')
        try:
            response = requests.session().get(link + f"pn{i}/", headers=headers, proxies=ip_proxy())
        except:
            continue
        html = response.content.decode('utf8')
        poiids = re.findall('"poiId":(.*?),', html)
        print(poiids)
        for i in poiids:
            headers = {
                'Referer': 'https://sz.meituan.com/meishi/c393/pn1/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
            }
            url = f'https://www.meituan.com/meishi/{i}/'
            try:
                response = requests.session().get(url, headers=headers, proxies=ip_proxy())
            except:
                continue
            # print(url)
            html = response.text
            shopdata = re.findall('"detailInfo":(.*),"photos":', html)
            typedata = re.findall('"crumbNav":(.*),"prefer', html)
            try:
                shopdata = json.loads(shopdata[0])
                typedata = json.loads(typedata[0])
            except Exception as e:
                with open('log.log', 'a', encoding='utf-8') as file:

                    file.write(url + '\t' + link + f"pn{i}/" + '\t' +type_name + '\t'+whole_type + '\n')
                continue


            shopimation = data_proces(shopdata, typedata)
            print(shopimation)
            with open('meituan.js', 'a', encoding='utf-8') as file:
                json.dump(shopimation, file, ensure_ascii=False)
                file.write('\n')



    #




url = 'https://sz.meituan.com/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
}
meituan_resp = requests.get(url, headers=headers, proxies=ip_proxy())
print(meituan_resp.text)
meituan_html = etree.HTML(meituan_resp.text)
meituan_type = meituan_html.xpath('//li[@class="nav-li"]/span/span/a/@href')
meituan_type_name = meituan_html.xpath('//li[@class="nav-li"]/span/span/a/text()')
print(meituan_type)
print(meituan_type_name)
for type_link, type_name in zip(meituan_type, meituan_type_name):

    try:
        type_detail_resp = requests.get(type_link, headers=headers, proxies=ip_proxy())
    except:
        continue
    type_detail_html = etree.HTML(type_detail_resp.text)
    try:
        type_detail_comm = type_detail_html.xpath('//div[@class="condition"]/div[1]/ul[@class="more clear"]/li/a/@href')
        type_detail_name = type_detail_html.xpath('//div[@class="condition"]/div[1]/ul[@class="more clear"]/li/a/text()')
    except Exception as e:
        continue
    for whole_link, whole_name in zip(type_detail_comm, type_detail_name):
        pagings(whole_link, type_name, whole_name)


"""
# 获取token
import base64
import random
import time
import zlib
import requests

# https://sz.meituan.com/meishi/api/poi/getPoiList?cityName=%E6%B7%B1%E5%9C%B3&cateId=393&areaId=0&sort=&dinnerCountAttrId=&page=1&userId=&uuid=58711e5e-0bc0-4c2e-b045-41158b1e2c67&platform=1&partner=126&originUrl=https%3A%2F%2Fsz.meituan.com%2Fmeishi%2Fc393%2Fpn1%2F&riskLevel=1&optimusCode=10&_token=eJyNj01vskAUhf%2FLbCHO4PBp0oUiBURqinwITRcIKNAKwgxQbd7%2F%2Fk6TdtFdk5ucZ849ObnzCXo7BwsBIQ0hHoxFDxZAmKGZDHhACdtIGsJzTcKyJmIeZL88BSGJB8c%2BXIPFi6CIEj9X5Ncvx2PGi6DNES8gFb3yPywynotsvlI2C4GS0itZQEjus0tR0SFtZll7gYxJWcEMaxheGwGyc%2F6UlCUIWPfFZ91M3741%2FVb683bZP1knqc4No2Iz5XUgDFO9fC4LqE89Pe9u3tLB7x5JO2MYyMoyM6dVY2i2nCfqN81zI91QDo3sVL3GNVeYTur5wOVNaK3cqSRNHXf2Izydlj7mYM1xx643Q1ffDfuIs6Nk44S3OL5Ra7Tde9mFesDF%2BPL%2BkXDJvlGigeLAkHZHn%2BXbsiBJnqykQ7INu7Hyn4zITvIxOXWjI45vdfCxPxJLLMRnZ5u52PD7wIFqQcXibsJMSk3HuAf3dW5Yfbupdy6O1nTYqEQzTSWCaOXjp%2B3j%2BeEB%2FPsPB5af%2BA%3D%3D

def get_token(areaId, cateId, page, cityName, originUrl):
    uuid = ''.join([random.choice('0123456789abcdef') for _ in range(20)]) + '.' + str(int(time.time())) + '.1.0.0'
    sign = base64.b64encode(zlib.compress(
                    (
                       f"areaId={areaId}&cateId={cateId}&cityName={cityName}&dinnerCountAttrId=&"
                       f"optimusCode=10&originUrl={originUrl}&page={page}&partner=126&platform=1&"
                       f"riskLevel=1&sort=&userId=&uuid={uuid}"
                    ).encode()
                )
            ).decode()
    ts = int(time.time() * 1000)
    token = {
        "rId":100900,
        "ver":"1.0.6",
        "ts":ts,
        "cts":ts + random.randint(100, 150),
        "brVD":[1853, 921],
        "brR":[[1920, 1080], [1853, 1053], 24, 24],
        "bI":[originUrl, ""],
        "mT":[],
        "kT":[],
        "aT":[],
        "tT":[],
        "aM":"",
        "sign": sign
    }
    _token = base64.b64encode(zlib.compress(str(token).encode())).decode()
    return _token




token = get_token('0', '393', '2', '深圳', 'https://sz.meituan.com/meishi/c393/pn2/&riskLevel=1')
# print(token)


"""



