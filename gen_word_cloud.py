import jieba
import csv
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 按行读取文件，返回文件的行字符串列表


def read_file(file_name):
    fp = open(file_name, "r", encoding="utf-8")
    content_lines = fp.readlines()
    fp.close()
    # 去除行末的换行符，否则会在停用词匹配的过程中产生干扰
    for i in range(len(content_lines)):
        content_lines[i] = content_lines[i].rstrip("\n")
    return content_lines


def save_file(file_name, content):
    fp = open(file_name, "w", encoding="utf-8")
    fp.write(content)
    fp.close()


appId = 177088
filename = './output/taptap_{0}.csv'.format(appId)

all_comments = []
with open(filename, 'r', encoding='utf-8') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        all_comments.append(row['comment'])

comment_str = ''.join(all_comments)

# load stopwords
stop_words = read_file("./data/stopwords.txt")
# print(stop_words)

# jieba分词
jieba.load_userdict("./data/custom_dict.txt")

cut_words = []
for line in all_comments:
    cut_words += [word for word in jieba.cut(line,cut_all=False) if word not in stop_words]
# print(cut_words)
save_file("./output/cut_words.txt", "\n".join(cut_words))

# # 设置词云
wc_text = "\n".join(cut_words)
wc = WordCloud(background_color="white",  # 设置背景颜色
               # mask = "图片",  #设置背景图片
               width=1024,
               height=768,
               max_words=1000,  # 设置最大显示的字数
               stopwords = stop_words, #设置停用词
               font_path="NotoSerifCJKsc-Black.otf",
               # 设置中文字体，使得词云可以显示（词云默认字体是“DroidSansMono.ttf字体库”，不支持中文）
               max_font_size=80,  # 设置字体最大值
               random_state=32,  # 设置有多少种随机生成状态，即有多少种配色方案
               )
wc_img = wc.generate(wc_text)  # 生成词云
wc_img.to_file('./output/wc_{0}.png'.format(appId))
plt.imshow(wc_img, interpolation='bilinear')
plt.axis("off")
plt.show()
print("all done")