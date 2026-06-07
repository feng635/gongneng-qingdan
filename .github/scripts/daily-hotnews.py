import urllib.request, urllib.parse, json, os, re
from datetime import datetime, timezone, timedelta

bj = timezone(timedelta(hours=8))
now = datetime.now(bj).strftime('%m/%d %H:%M')
items = []
srcs = []

# 1. 百度热搜
try:
    r = urllib.request.Request('https://top.baidu.com/api/board?tab=realtime',
        headers={'User-Agent': 'Mozilla/5.0'})
    d = json.loads(urllib.request.urlopen(r, timeout=15).read())
    for x in d.get('data', {}).get('cards', [{}])[0].get('content', []):
        if len(items) >= 10: break
        w, desc = x.get('word', x.get('query', '')), x.get('desc', '')
        if w and desc: items.append((w, desc, 'baidu'))
    if items: srcs.append('百度')
except: pass

# 2. 抖音（天聚数行）
key = os.environ.get('TIAN_API_KEY', '')
if key and len(items) < 10:
    try:
        r = urllib.request.Request(f'https://apis.tianapi.com/douyinhot/index?key={key}',
            headers={'User-Agent': 'Mozilla/5.0'})
        d = json.loads(urllib.request.urlopen(r, timeout=15).read())
        if d.get('code') == 200:
            for x in d.get('result', []):
                if len(items) >= 10: break
                w = x.get('word', '')
                if w and not any(w == t for t, _, _ in items):
                    items.append((w, '抖音热榜', 'douyin'))
            if any(s == 'douyin' for _, _, s in items): srcs.append('抖音')
    except: pass

# 3. 如果不足10条，补百度纯标题
if len(items) < 10:
    try:
        r = urllib.request.Request('https://top.baidu.com/api/board?tab=realtime',
            headers={'User-Agent': 'Mozilla/5.0'})
        d = json.loads(urllib.request.urlopen(r, timeout=15).read())
        for x in d.get('data', {}).get('cards', [{}])[0].get('content', []):
            if len(items) >= 10: break
            w = x.get('word', x.get('query', ''))
            if w and not any(w == t for t, _, _ in items):
                items.append((w, '百度热搜', 'baidu'))
    except: pass

if not items: items = [('今日热点暂无数据', '请稍后再试', 'other')]

emoji_map = {
    '苹果|iPhone|手机|华为|小米|oppo|vivo|三星|荣耀':'\U0001f4f1',
    'AI|人工智能|大模型|ChatGPT|Claude|OpenAI|谷歌|百度|模型':'\U0001f916',
    '汽车|新能源|特斯拉|比亚迪|蔚来|小鹏|理想|燃油':'\U0001f697',
    '微信|抖音|TikTok|微博|小红书|快手|B站|美团|支付':'\U0001f4ac',
    '股市|基金|理财|银行|美元|黄金|比特币|经济|贸易|关税':'\U0001f4b0',
    '游戏|电竞|原神|王者|吃鸡|PS5|Switch':'\U0001f3ae',
    '电影|电视|综艺|视频|音乐|娱乐|明星|演唱会':'\U0001f3ac',
    '教育|高考|考研|大学|学生|老师|考试':'\U0001f393',
    '天气|地震|台风|暴雨|洪水|灾害|气候':'\U000026a1',
    '航天|火箭|卫星|登月|NASA|SpaceX|神舟':'\U0001f680',
    '芯片|半导体|5G|6G|专利|技术|科技':'\U0001f4bb',
}
def emoji(t):
    for k, e in emoji_map.items():
        if re.search(k, t, re.I): return e
    return '\U0001f4f0'

labels = {'baidu':'百度', 'douyin':'抖音', 'other':'综合'}
lines = ['# \U0001f4f0 今日热点 TOP10', '', '---', '']
for i, (t, d, s) in enumerate(items, 1):
    link = f'https://www.douyin.com/search/{urllib.parse.quote(t)}' if s == 'douyin' else f'https://www.baidu.com/s?wd={urllib.parse.quote(t)}'
    hot = '\U0001f525' if i <= 3 else ''
    lines.append(f'### {i}. {emoji(t)} [{t}]({link}) {hot}')
    lines.append(f'> <{labels.get(s, "综合")}> {d}')
    lines.append('')

lines.append('---')
lines.append(f'\U0001f550 **{now}**')
if srcs: lines.append(f'\U0001f4e1 来源: {" + ".join(srcs)}')
lines.append('')
lines.append('\U0001f916 *由 Nova 自动聚合推送*')
lines.append('')
lines.append('💌 亲爱的枫，愿你今天元气满满，好运连连！')

content = '\n'.join(lines)
title = f'\U0001f4f0 每日热点新闻 - {now.split()[0]}'

sct_key = os.environ.get('SCT_KEY', '')
if not sct_key: exit(1)

data = urllib.parse.urlencode({'title': title, 'desp': content}).encode()
req = urllib.request.Request(f'https://sctapi.ftqq.com/{sct_key}.send', data=data,
    headers={'Content-Type': 'application/x-www-form-urlencoded'})
resp = json.loads(urllib.request.urlopen(req).read())

if resp.get('code') == 0:
    print(f'OK - {len(items)}条, 来源: {", ".join(srcs)}')
else:
    print(f'FAIL: {resp}')
