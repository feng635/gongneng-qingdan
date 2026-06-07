import urllib.request, urllib.parse, json, sys, os
from datetime import datetime, timezone, timedelta

# 获取北京时间
bj_tz = timezone(timedelta(hours=8))
now = datetime.now(bj_tz).strftime('%m/%d %H:%M')

# 尝试获取百度热搜
news_items = []
try:
    req = urllib.request.Request(
        'https://top.baidu.com/api/board?tab=realtime',
        headers={'User-Agent': 'Mozilla/5.0'},
        method='GET'
    )
    resp = urllib.request.urlopen(req, timeout=15)
    data = json.loads(resp.read())
    items = data.get('data', {}).get('cards', [{}])[0].get('content', [])
    for item in items[:10]:
        word = item.get('word', item.get('query', ''))
        desc = item.get('desc', '')
        if word:
            news_items.append((word, desc))
except:
    pass

# 备用：tenapi
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
        for item in items[:10]:
            name = item.get('name', '')
            if name:
                news_items.append((name, ''))
    except:
        pass

# 构建消息内容
lines = ['# 今日热点 TOP10', '']
for i, (title, desc) in enumerate(news_items, 1):
    lines.append(f'{i}. **{title}**')
    if desc:
        lines.append(f'   {desc}')
    lines.append('')

lines.append('---')
lines.append(f'\U0001f550 {now}')
lines.append('✏️ Nova 自动推送')

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
