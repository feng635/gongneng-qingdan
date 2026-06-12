# Daily Hotnews 参考

## 数据来源
| 来源 | API | 状态 |
|:----|:----|:----:|
| 百度热搜 | `top.baidu.com/api/board` | 稳定 |
| 抖音热榜 | `tianapi.com` 天聚数行 | 审核中 |

## 推送通道
- **Server酱 Turbo**: `https://sctapi.ftqq.com/{SENDKEY}.send`
- **SendKey**: 存在 GitHub Secrets (`SCT_KEY`)

## GitHub Actions
- **位置**: `.github/workflows/daily-hotnews.yml`
- **脚本**: `.github/scripts/daily-hotnews.py`
- **定时**: 每天 UTC 1:00 = 北京时间 9:00
