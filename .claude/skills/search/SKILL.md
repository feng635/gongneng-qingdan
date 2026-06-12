---
name: search
description: "当用户提到搜索、查询信息，或提到小红书、知乎、B站、抖音等平台时，使用 opencli 在各平台搜索。也用于获取笔记详情、下载图片。"
when_to_use: "用户说"搜一下""查查""找找"后面跟平台名(小红书/知乎/B站/微博/抖音)，或直接说"帮我搜xxx""
---

# OpenCLI 搜索工具

通过 opencli 命令行工具在各互联网平台搜索信息、获取笔记/文章详情和下载图片。

## 已安装环境

| 项目 | 说明 |
|------|------|
| 工具 | `@jackwener/opencli` v1.7.7 |
| 安装方式 | `npm install -g @jackwener/opencli` |
| 浏览器 | Microsoft Edge (Chromium) |
| 扩展 | OpenCLI Browser Bridge v1.0.2（已加载到 Edge） |
| 扩展路径 | `D:\cursor_workspace\.claude\opencli-extension\` |

## 使用前检查

运行 opencli 前需确保 Edge 浏览器开着，且扩展已连接：

```bash
opencli doctor
```

如果扩展没连上，先重启守护进程：
```bash
opencli daemon stop && opencli doctor
```

## 常用平台与命令

### 小红书 (xiaohongshu)

```bash
# 搜索笔记
opencli xiaohongshu search "<关键词>"

# 查看笔记详情（需要完整的带 xsec_token 的 URL）
opencli xiaohongshu note "<完整URL>"

# 下载笔记中的图片/视频（需要完整URL）
opencli xiaohongshu download "<完整URL>" --output "<保存路径>"

# 查看笔记评论
opencli xiaohongshu comments "<note-id>"
```

### 知乎 (zhihu)

```bash
# 搜索
opencli zhihu search "<关键词>"

# 查看回答
opencli zhihu answer <answer-id>
```

### B站 (bilibili)

```bash
# 搜索视频
opencli bilibili search "<关键词>"

# 查看视频信息
opencli bilibili video <bvid>
```

### 微博 (weibo)

```bash
# 搜索
opencli weibo search "<关键词>"
```

### 抖音 (douyin)

```bash
# 搜索
opencli douyin search "<关键词>"
```

## 搜索后处理

1. 搜索结果会返回标题、作者、点赞数、发布时间等信息
2. 查看笔记/文章详情需要用到完整的 URL（含 `xsec_token`）
3. 下载的图片保存在指定目录，可直接查看
4. 部分笔记的内容在图片里，需要配合 OCR 技能读取

## 注意事项

- opencli 需要依赖浏览器中的扩展，所以 **Edge 浏览器必须保持打开**
- 如果守护进程连不上扩展，试：`opencli daemon stop && opencli doctor`
- 小红书等平台的 xsec_token 有时效性，搜索结果要尽快使用
- 下载图片时用 `--output` 指定目录，不指定默认保存到 `./xiaohongshu-downloads`
