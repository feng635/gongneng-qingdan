import urllib.request, urllib.parse, json, sys, os
from datetime import datetime, timezone, timedelta

# 获取北京时间
bj_tz = timezone(timedelta(hours=8))
now = datetime.now(bj_tz).strftime('%m/%d %H:%M')

# 获取新闻：百度热搜 + 抖音热榜 混合
news_items = []
fetched_sources = []

# 1. 百度热搜
try:
    req = urllib.request.Request(
        'https://top.baidu.com/api/board?tab=realtime',
        headers={'User-Agent': 'Mozilla/5.0'},
        method='GET'
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

# 2. 抖音热榜
try:
    req = urllib.request.Request(
        'https://tenapi.cn/v2/douyinhot',
        headers={'User-Agent': 'Mozilla/5.0'},
        method='GET'
    )
    resp = urllib.request.urlopen(req, timeout=15)
    data = json.loads(resp.read())
    items = data.get('data', {}).get('list', [])
    # 混合：如果百度不足10条，用抖音补；否则拿5条抖音丰富内容
    for item in items:
        if len(news_items) >= 10:
            break
        name = item.get('name', '')
        hot = item.get('hot', '')
        if name:
            desc = f'抖音热榜 \U0001f525 {hot}' if hot else '抖音热榜'
            news_items.append((name, desc, 'douyin'))
    if any(s == 'douyin' for _, _, s in news_items[-6:]):
        fetched_sources.append('抖音')
except:
    pass

# 3. 备用：通用热榜
if not news_items:
    try:
        req = urllib.request.Request(
            'https://tenapi.cn/v2/hot',
            headers={'User-Agent': 'Mozilla/5.0'},
            method='GET'
        )
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read())
        items = data.get('data', {}).get('list', [])
        for item in items:
            if len(news_items) >= 10:
                break
            name = item.get('name', '')
            if name:
                news_items.append((name, '', 'other'))
        if news_items:
            fetched_sources.append('综合')
    except:
        pass

# emoji 关键词映射
EMOJI_MAP = {
    '苹果|iPhone|手机|华为|小米|oppo|vivo|三星|荣耀': '\U0001f4f1',
    'AI|人工智能|大模型|ChatGPT|Claude|OpenAI|谷歌|百度|科大讯飞|模型': '\U0001f916',
    '汽车|新能源|特斯拉|比亚迪|蔚来|小鹏|理想|燃油': '\U0001f697',
    '微信|抖音|TikTok|微博|小红书|快手|B站|美团|滴滴|支付': '\U0001f4ac',
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
    import re
    for keywords, emoji in EMOJI_MAP.items():
        if re.search(keywords, text, re.I):
            return emoji
    return '\U0001f4f0'

# 构建消息内容
import re
source_labels = {'baidu': '百度', 'douyin': '抖音', 'other': '综合'}
lines = ['# \U0001f4f0 今日热点 TOP10', '', '---', '']
for i, (title, desc, src) in enumerate(news_items, 1):
    emoji = get_emoji(title)
    hot = '\U0001f525' if i <= 3 else ''
    src_tag = source_labels.get(src, '')
    # 抖音用抖音搜索链接，其他用百度
    if src == 'douyin':
        link = f'https://www.douyin.com/search/{urllib.parse.quote(title)}'
    else:
        link = f'https://www.baidu.com/s?wd={urllib.parse.quote(title)}'
    lines.append(f'### {i}. {emoji} [{title}]({link}) {hot}')
    lines.append(f'> <{src_tag}> {desc}')
    lines.append('')

lines.append('---')
lines.append(f'\U0001f550 **{now}**')
lines.append(f'\U0001f4e1 来源：{" + ".join(fetched_sources)}')
lines.append('')
lines.append('\U0001f916 *由 Nova 自动聚合推送*')
lines.append('')
lines.append('💌 亲爱的枫，愿你今天元气满满，代码无Bug，心情如晴天！')

content = '\n'.join(lines)
title = f'\U0001f4f0 每日热点新闻 - {now.split()[0]}'

# 发送
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
    print(f'推送成功! {len(news_items)} 条新闻')
else:
    print(f'推送失败: {result}')
