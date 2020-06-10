import json
import time
import requests


# 121724111,39039388,121772027,39011888


def get_mmsi(degrees):
    while 1:
        hsd_url = f'http://www.shipxy.com/ship/getareaships?scode=1365289&level=15&area={",".join([str(i) for i in degrees])}&enc=1'
        headers = {
            'Host': 'www.shipxy.com',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://www.shipxy.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        hsd_resp = requests.get(hsd_url, headers=headers)
        x = 0
        mmsi_list = []
        try:
            if len(json.loads(hsd_resp.text)['data']) == 0:
                continue
        except:
            print('参数错误')
            continue
        break
    name_dict = {}
    for i in json.loads(hsd_resp.text)['data']:
        lon = i['lon']
        lat = i['lat']
        # 121724111,39039388,121772027,39011888
        if int(lon) > degrees[0] and int(lon) < degrees[2]:
            mmsi_list.append(i['mmsi'])
            name_dict[i['mmsi']] = i['name']
        x += 1
    print(name_dict)
    print(mmsi_list)
    return mmsi_list, name_dict


def degree_reversal(num_degree):
    degree = num_degree.split('º')[0]
    minute = num_degree.split(' ')[1].split('.')[0]
    second = num_degree.split(' ')[1].split('.')[-1]
    degrees = int((int(degree) + (int(minute) + int(second) / 10 / 60) / 60) * 1000000)
    return degrees


def get_data(mmsi_id):
    url = 'http://www.shipxy.com/ship/GetShip'
    data = {
        'shipIDs': str(mmsi_id),
        'mmsi': str(mmsi_id)
    }

    headers = {
        'Host': 'www.shipxy.com',
        'Origin': 'http://www.shipxy.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://www.shipxy.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Length': '15',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '_elane_maptype=MT_SEA; _filter_flag=-1; _elane_shipfilter_one=2; tc_QX=; _9755xjdesxxd_=32; YD00803672648830%3AWM_TID=ABz2i4zhyXdFFVQEVUc%2BSR87N7UJ%2B15t; gdxidpyhxdE=pSSaJTs2rszvuzM2S91LoIAD7YfPHa7nI6enoxjrs2mCRr08jo4EWSTnV3%2B69Dm6KK3ou5xs5772Ti%2FAsvfiurKN%2BydnrYwlsfA%2Fx5Weo1W%2B6ccZVNc7XfTrU9WimuNob2kNxvIU1JJD9SGSkxEZGv8IVzbnNuRtUbX4kPMKXL1Kuo2y%3A1590150045417; YD00803672648830%3AWM_NI=0OhnoCUrHpwR%2FrsB%2BQzftHpkgOJ0tkygmEcqla5PIei6dHginNXdCvLV6C6YYQsjxFqDvvLAGRwI2eHFLi69Gnce4UYZD1pHj93uWrEU%2BBowDrrkraWWiMbmgAG3Z17jTFg%3D; YD00803672648830%3AWM_NIKE=9ca17ae2e6ffcda170e2e6ee95cc4195ed9fd9b667818a8fa6c44a929a8aabae4997aa00bbd73cf89482abb12af0fea7c3b92af491a88fee4997ae8891f65aedaebda3aa5bbababca9f361a59186d1f761bbb9a3a6e27bb0bffbb1cc6fabeaaca9e663ae929885c27e908afaa4b5539b8fbd8bfb4eb39cba97cf4b858eb9aab16f8c9a848ab53385b2ad86b75f9b868cd2f344aae7fd96d67a878be5a3ee7d88aebe8cf16b9589a7aee167a59f89d4d93bf5b69ca7e637e2a3; ASP.NET_SessionId=cit1z2ac4luirhgbcr2vsyea; Hm_lvt_adc1d4b64be85a31d37dd5e88526cc47=1590190750,1590193917,1590194706,1590227972; _elane_rastar=; _elane_shipfilter_olength=0; _elane_shipfilter_sog=0; _elane_shipfilter_length=0%2C40%2C41%2C80%2C81%2C120%2C121%2C160%2C161%2C240%2C241%2C320%2C321%2C9999; _elane_shipfilter_country=0%2C1%2C2; tc_TC=; .UserAuth2=78C88ABEE00C9A94C68FD8064868763C03AA9477A25D93D85CC3C14381DCCE639CFAD233B0005CADFA98051D43354F161C4FB0413587626ED2140AE4663A8173703AA5796C01613E8C1DAECFA0316C8A8124B43B02733CAB6613D6607B1DF028DC0601EC2B5D196D06FFF80634592E007A16C58A; _elane_shipfilter_type=%u8D27%u8239%2C%u96C6%u88C5%u7BB1%u8239%2C%u6CB9%u8F6E%2C%u5F15%u822A%u8239%2C%u62D6%u8F6E%2C%u62D6%u5F15%2C%u6E14%u8239%2C%u6355%u635E%2C%u5BA2%u8239%2C%u641C%u6551%u8239%2C%u6E2F%u53E3%u4F9B%u5E94%u8239%2C%u88C5%u6709%u9632%u6C61%u88C5%u7F6E%u548C%u8BBE%u5907%u7684%u8239%u8236%2C%u6267%u6CD5%u8247%2C%u5907%u7528-%u7528%u4E8E%u5F53%u5730%u8239%u8236%u7684%u4EFB%u52A1%u5206%u914D%2C%u5907%u7528-%u7528%u4E8E%u5F53%u5730%u8239%u8236%u7684%u4EFB%u52A1%u5206%u914D%2C%u533B%u7597%u8239%2C%u7B26%u540818%u53F7%u51B3%u8BAE%28Mob-83%29%u7684%u8239%u8236%2C%u62D6%u5F15%u5E76%u4E14%u8239%u957F%3E200m%u6216%u8239%u5BBD%3E25m%2C%u758F%u6D5A%u6216%u6C34%u4E0B%u4F5C%u4E1A%2C%u6F5C%u6C34%u4F5C%u4E1A%2C%u53C2%u4E0E%u519B%u4E8B%u884C%u52A8%2C%u5E06%u8239%u822A%u884C%2C%u5A31%u4E50%u8239%2C%u5730%u6548%u5E94%u8239%2C%u9AD8%u901F%u8239%2C%u5176%u4ED6%u7C7B%u578B%u7684%u8239%u8236%2C%u5176%u4ED6; FD857C2AF68165D4=qsGRGsDf6D8Wz55nPUvBDjzTha8DTx4gTDpdiCq17qO1Z183FB7/wwmBj+EviGZR; Hm_lpvt_adc1d4b64be85a31d37dd5e88526cc47=1590343578; shipxy_v3_history_serch=s%u2606DAIWAN%20WISDOM%u2606355586000%u260670%u2606MMSI%uFF1A355586000%7Cs%u2606LIDIA%u2606372811000%u260670%u2606MMSI%uFF1A372811000%7Cp%u2606Heshangdao%u260611316%u260639.016668%u2606121.75%7Cs%u2606LIAN%20GANG%2029%u2606412002460%u2606%u2606MMSI%uFF1A412002460%7Cs%u2606HONG%20WEI%20319%u2606413239730%u260670%u2606MMSI%uFF1A413239730%7Cs%u2606JUNHUI999%u2606413526680%u260670%u2606MMSI%uFF1A413526680%7Cs%u2606XIEHAITONGZHOU%u2606413458350%u260670%u2606MMSI%uFF1A413458350%7Cs%u2606ENJIE2%u2606412761310%u260670%u2606MMSI%uFF1A412761310%7Cp%u2606Jiucaigang%u2606212128%u260631.9%u2606120.266667%7Cs%u2606HANSA%20STEINBURG%u2606636092570%u2606100%u2606MMSI%uFF1A636092570; SERVERID=8dac9e937b8701fba4cb1394cffade3e|1590343879|1590343031'
    }
    response = requests.post(url, headers=headers, data=data)
    return json.loads(response.text)


def dataquery(data_dict):
    analysis_dict = {
        'ship_name：': 'name',
        '纬度：': 'lat',
        '呼号：': 'callsign',
        '经度：': 'lon',
        'MMSI：': 'mmsi',
        '船首向：': 'hdg',
        'IMO：': 'imo',
        '航迹向：': '',
        '船籍：': '*****',
        '航速：': 'sog',
        '类型：': 'type',  #
        '状态：': 'navistatus',  #
        '目的地：': 'dest',
        '船长：': 'length',
        '预到时间：': 'eta',
        '船宽：': 'width',
        '更新时间：': 'lastdyn',
        '吃水：': 'draught',
        '旋转角速度：': 'rot',
    }

    state_type = {
        0: "在航(主机推动)",
        1: "锚泊",
        2: "失控",
        3: "操作受限",
        4: "吃水受限",
        5: "靠泊",
        6: "搁浅",
        7: "捕捞作业",
        8: "靠船帆提供动力",
    }

    def shiptype(code):
        goods_type = {
            '50': '引航船',
            '51': '搜救船',
            '52': '拖轮',
            '53': '港口供应船',
            '54': '载有防污染装置和设备的船舶',
            '55': '执法艇',
            '56': '备用-用于当地船舶的任务分配',
            '57': '备用-用于当地船舶的任务分配',
            '58': '医疗船（如1949年日内瓦公约及附加条款所规定）',
            '59': '符合18号决议（Mob-83）的船舶',
            '30': '捕捞',
            '31': '拖引',
            '32': '拖引并且船长>200m或船宽>25m',
            '33': '疏浚或水下作业',
            '34': '潜水作业',
            '35': '参与军事行动',
            '36': '帆船航行',
            '37': '娱乐船',
        }
        if 20 <= code <= 29:
            ship_type = '地效应船'
        elif 40 <= code <= 49:
            ship_type = '高速船'
        elif 60 <= code <= 69:
            ship_type = '客船'
        elif 70 <= code <= 79:
            ship_type = '货船'
        elif 80 <= code <= 89:
            ship_type = '油轮'
        elif 90 <= code <= 99 or code == 0:
            ship_type = '其他类型的船舶'
        else:
            try:
                ship_type = goods_type[str(code)]
            except KeyError:
                ship_type = '其他类型的船舶'
        return ship_type

    # 转换经纬度
    def unit_conversion(degrees):
        if len(degrees) == 9:
            degree = degrees[0:3]
            minute = float('0.' + degrees[3:-1]) * 60
            second = float('0.' + str(minute).split('.')[-1]) * 60
            return f'{degree}°{int(minute)}.{str(second)[0:4].replace(".", "")}'
        elif len(degrees) <= 8:
            degree = degrees[0:2]
            minute = float('0.' + degrees[2:-1]) * 60
            second = float('0.' + str(minute).split('.')[-1]) * 60
            return f'{degree}°{int(minute)}.{str(second)[0:4].replace(".", "")}'

    data_dic = {}
    for keys, values in analysis_dict.items():
        dic = data_dict
        try:
            value = dic['data'][0][values]
        except KeyError:
            value = values
        if keys == '类型：':
            value = shiptype(dic['data'][0][values])
        elif keys == '状态：':
            value = state_type[dic['data'][0][values]]
        elif keys == '吃水：':
            value = f"{dic['data'][0][values]/1000} 米"
        elif keys == '船首向：':
            value = f"{dic['data'][0][values]/100} 度"
        elif keys == '航速：':
            value = "0.0节"
        elif keys == '经度：':
            value = unit_conversion(str(dic['data'][0][values])) + ' E'
        elif keys == '纬度：':
            value = unit_conversion(str(dic['data'][0][values])) + ' N'
        elif keys == '预到时间：':
            value = '2020-' + dic['data'][0][values]
        elif keys == '更新时间：':
            timeArray = time.localtime(int(dic['data'][0][values]))
            value = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        elif keys == '船长：' or keys == '船宽：':
            value = f"{dic['data'][0][values]/10} 米"

        data_dic[keys] = value
    return data_dic


if __name__ == '__main__':
    file_dict = {}
    file_dict['heshangdao'] = 'heshangdao'
    latitude_longitude = ['121º 43.268 E', '39º 1.818 N', '121º 46.193 E', '39º 0.428 N']
    latitude_longitude_list = [degree_reversal(i) for i in latitude_longitude]
    mmsi_list, name_dict = get_mmsi(latitude_longitude_list)
    for mmsi_id in mmsi_list:
        json_dict = get_data(mmsi_id)
        data_dict = dataquery(json_dict)
        file_dict[data_dict['MMSI：']] = data_dict
        file_dict[data_dict['MMSI：']]['船名'] = name_dict[data_dict['MMSI：']]
        print(data_dict)
    with open('heshangdao.js', 'w', encoding='utf-8') as file:

        json.dump(file_dict, file, ensure_ascii=False)
