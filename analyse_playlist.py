import requests
import json
from googletrans import Translator
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from scipy.misc import imread
from get_single_song_split import get_single_song_split


def analyse_playlist(id):
    url = 'http://music.163.com/api/playlist/detail?id=' + str(id)
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
        'referer': 'http://music.163.com',
        'host': 'music.163.com'
    }
    r = requests.get(url, headers=headers)

    d = json.loads(r.text)

    song_list = d['result']['tracks']
    analyse_summary = {}

    for song in song_list:
        print(str(song['id']) + '\t' + song['name'])
        analyse_summary = merge_tesults(analyse_summary, get_single_song_split(song['id']))

    return sorted(analyse_summary.items(), key=lambda item: item[1], reverse=True)


def merge_tesults(original, new_result):
    for k, v in new_result.items():
        if original.get(k):
            original[k] += v
        else:
            original[k] = v
    
    return original


def translate_key(word):
    translator = Translator()
    meaning = translator.translate(word, dest='zh-CN').text
    return meaning


def generate_wc(content):
    path = r'851MkPOP_001.ttf'
    bg_pic = imread('beauty.jpg')  # 读取一张图片文件
    image_colors = ImageColorGenerator(bg_pic)  # 从背景图片生成颜色值
    wc = WordCloud(
        font_path=path, 
        background_color="white",
        mask=bg_pic,
        max_font_size=40,
        color_func=image_colors,
        random_state=42)
    wc = wc.generate(content)
    wc.to_file('result.jpg')


def main(playlist_no, top_num=150, translate=False):
    r = analyse_playlist(playlist_no)
    cnt = 0
    s = ''
    for elem in r:
        tsl = elem[0]
        if translate:
            tsl = translate_key(tsl)
        print(str(elem) + ' ' + tsl)
        s += tsl + ' '
        cnt += 1
        if cnt > top_num:
            break
    
    print(s)
    generate_wc(s.strip())


if __name__ == '__main__':
    main(940947514)
