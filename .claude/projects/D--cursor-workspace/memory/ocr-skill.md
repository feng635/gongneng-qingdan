---
name: OCR识图流程
description: 枫发图片路径时，必须调用Tesseract OCR识别文字，不能用Read工具读图
type: feedback
---

当枫发图片路径时，必须调用 Tesseract OCR 识别文字，而不是用 Read 工具去读图片。

**Why:** 枫的 CLAUDE.md 里明确配置了 OCR 技能（Tesseract + 备用 paddleocr），之前犯了用 Read 读图的错误，被他指出来了。

**How to apply:** 每次遇到 `.jpg`、`.png`、`.bmp`、`.jpeg` 等图片路径时，直接调用：
```
TESSDATA_PREFIX="C:/Users/17384/AppData/Local/tesseract/tessdata" "C:\Program Files\Tesseract-OCR\tesseract.exe" "<路径>" stdout -l chi_sim+eng
```
如果 chi_sim+eng 失败，降级到纯英文 eng。不要先用 Read 去试。
