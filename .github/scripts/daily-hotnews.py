import urllib.request, urllib.parse, json, sys, os, re
from datetime import datetime, timezone, timedelta

bj_tz = timezone(timedelta(hours=8))
now = datetime.now(bj_tz).strftime('%m/%d %H:%M')

news_items = []
fetched_sources = []

# 获取百度热搜
try:
    req = urllib.request.Request(
        'https://top.baidu.com/api/board?tab=realtime',
        headers={'User-Agent': 'Mozilla/5.0'},
    )
    resp = urllib.request.urlopen(req, timeout=15)
    data = json.loads(resp.read())
    items = data.get('data', {}).get('cards', [{}])[0].get('content', [])
    for item in items:
        if len(news_items) >= 10:
            break
        word = item.get('word', item.get('query', ''))
        desc = item.get('desc', '')
        if word and desc:
            news_items.append((word, desc, 'baidu'))
    if news_items:
        fetched_sources.append('百度')
except:
    pass

# GitHub Actions 上抓抖音热榜（用 douyin.com/hot 页面数据）
if len(news_items) < 10:
    try:
        req = urllib.request.Request(
            'https://www.douyin.com/aweme/v1/web/hot/search/list/',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json',
            }
        )
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read())
        for item in data.get('data', {}).get('word_list', []):
            if len(news_items) >= 10:
                break
            word = item.get('word', '')
            hot_val = item.get('hot_value', 0)
            if word:
                news_items.append((word, f'抖音热榜热度: {hot_val}', 'douyin'))
        if any(s == 'douyin' for _, _, s in news_items):
            fetched_sources.append('抖音')
    except:
        pass

# 如果还不足10条，从百度多取
if len(news_items) < 10:
    try:
        req = urllib.request.Request(
            'https://top.baidu.com/api/board?tab=realtime',
            headers={'User-Agent': 'Mozilla/5.0'},
        )
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read())
        items = data.get('data', {}).get('cards', [{}])[0].get('content', [])
        for item in items:
            if len(news_items) >= 10:
                break
            word = item.get('word', item.get('query', ''))
            if word:
                # 检查是否已存在
                if not any(w == word for w, _, _ in news_items):
                    news_items.append((word, '百度热搜', 'baidu'))
    except:
        pass

# 终极备用
if not news_items:
    news_items = [
        ('暂时无法获取热点新闻', '请稍后再试', 'other'),
    ]

emoji_map = {
    '苹果|iPhone|手机|华为|小米|oppo|vivo|三星|荣耀': '\U0001f4f1',
    'AI|人工智能|大模型|ChatGPT|Claude|OpenAI|谷歌|百度|模型': '\U0001f916',
    '汽车|新能源|特斯拉|比亚迪|蔚来|小鹏|理想|燃油': '\U0001f697',
    '微信|抖音|TikTok|微博|小红书|快手|B站|美团|支付': '\U0001f4ac',
    '股市|基金|理财|银行|美元|黄金|比特币|经济|贸易|关税': '\U0001f4b0',
    '游戏|电竞|原神|王者|吃鸡|PS5|Switch': '\U0001f3ae',
    '电影|电视|综艺|视频|音乐|娱乐|明星|演唱会': '\U0001f3ac',
    '疫情|疫苗|健康|医疗|医院|手术|药物': '\U0001f48a',
    '教育|高考|考研|大学|学生|老师|考试': '\U0001f393',
    '天气|地震|台风|暴雨|洪水|灾害|气候': '\U000026a1',
    '航天|火箭|卫星|登月|NASA|SpaceX|神舟': '\U0001f680',
    '芯片|半导体|5G|6G|专利|技术|科技': '\U0001f4bb',
}
def get_emoji(text):
    for keywords, emoji in emoji_map.items():
        if re.search(keywords, text, re.I):
            return emoji
    return '\U0001f4f0'

source_labels = {'baidu': '百度', 'douyin': '抖音', 'other': '综合'}
lines = ['# \U0001f4f0 今日热点 TOP10', '', '---', '']
for i, (title, desc, src) in enumerate(news_items, 1):
    emoji = get_emoji(title)
    hot = '\U0001f525' if i <= 3 else ''
    src_tag = source_labels.get(src, '')
    if src == 'douyin':
        link = f'https://www.douyin.com/search/{urllib.parse.quote(title)}'
    else:
        link = f'https://www.baidu.com/s?wd={urllib.parse.quote(title)}'
    lines.append(f'### {i}. {emoji} [{title}]({link}) {hot}')
    lines.append(f'> <{src_tag}> {desc}')
    lines.append('')

lines.append('---')
lines.append(f'\U0001f550 **{now}**')
if fetched_sources:
    lines.append(f'\U0001f4e1 来源: {" + ".join(fetched_sources)}')
lines.append('')
lines.append('\U0001f916 *由 Nova 自动聚合推送*')
lines.append('')
lines.append('💌 亲爱的枫，愿你每天都有新收获，好运气不请自来！')

content = '\n'.join(lines)
title = f'\U0001f4f0 每日热点新闻 - {now.split()[0]}'

sct_key = os.environ.get('SCT_KEY', '')
if not sct_key:
    print('SCT_KEY not set')
    sys.exit(1)

data = urllib.parse.urlencode({'title': title, 'desp': content}).encode()
req = urllib.request.Request(
    f'https://sctapi.ftqq.com/{sct_key}.send',
    data=data,
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
)
resp = urllib.request.urlopen(req)
result = json.loads(resp.read())
if result.get('code') == 0:
    print(f'推送成功! {len(news_items)} 条, 来源: {", ".join(fetched_sources)}')
else:
    print(f'推送失败: {result}')
