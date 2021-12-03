import jieba
jieba.load_userdict('wordlist.txt')
import jieba.analyse


def analyse_words(txtpath, wordpath):
    counts = {}
    with open(wordpath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        counts[line.rstrip('\n')] = 0

    txt = open(txtpath, "r").read()
    words = jieba.lcut(txt)

    for word in words:
        word = word.replace('  ', '')
        if len(word) == 1:continue
        if word not in counts:continue
        counts[word] = counts.get(word, 0) + 1

    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)
    for item in items:
        word, count = item
        print(f"{word}: {count}")


if __name__ == '__main__':
    txtpath = 'pdf/300013新宁物流：2018年年度报告_2019-04-25.txt'
    wordpath = './wordlist.txt'
    analyse_words(txtpath, wordpath)