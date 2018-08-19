import requests
import json
import re

def get_lyrics(id):
    url = 'https://music.163.com/api/song/lyric?id=' + str(id) + '&lv=1&kv=1&tv=-1'
    r = requests.get(url)
    d = json.loads(r.text)
    lyric = d['lrc']['lyric']
    
    lyric = get_rid_of_specific_info('作词', lyric)
    lyric = get_rid_of_specific_info('作曲', lyric)    

    lyric = re.sub(r'\[.*\]', '', lyric)
    lyric = re.sub(r'\n', '', lyric)
    lyric = re.sub(r'\s','', lyric)

    punctuation_pattern = re.compile(r'[\d+\.\-\!\?\/_,$%^*(+\"\']+|[+——！，。？：:“”、~@#￥%……&*（）「」(\d+)]+|[a-zA-Z]')
    lyric = punctuation_pattern.sub('', lyric)
    lyric.strip()

    print(lyric)

    return lyric


def get_rid_of_specific_info(keyword, lyric):
    start = lyric.find(keyword)
    if start != -1:
        i = start
        while lyric[i] != '[':
            i += 1
        lyric = lyric[: start] + lyric[i: ]

    return lyric
