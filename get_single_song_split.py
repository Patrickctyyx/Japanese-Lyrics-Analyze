import re
import MeCab
from get_lyrics import get_lyrics
from collections import Counter


def get_single_song_split(id, detail=False):
    analysis = {}
    l = []

    mecab = MeCab.Tagger('-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/')

    lyric = get_lyrics(id)
    node = mecab.parseToNode(lyric)

    while node:
        try:
            if node.feature.split(",")[0] in ("名詞", "動詞", "形容詞"):
                # 如果这里使用 dict 存储数据，就有一定的可能会出现编码错误
                # 使用 list 储存之后，尽管还是会出现编码错误，但是可能性大大降低了
                if detail:
                    l.append(node.surface + ',' + node.feature)
                else:
                    l.append(node.surface)
        except UnicodeDecodeError:
            print(id)
        node = node.next

    analysis =  dict(Counter(l))
        
    return analysis


if __name__ == '__main__':
    d = get_single_song_split(460319)
    for key in d:
        print(key + '\t' + str(d[key]))
