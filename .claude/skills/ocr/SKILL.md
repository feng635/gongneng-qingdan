---
name: ocr
description: "当用户发图片路径时，优先用 Tesseract OCR 识别图片文字。先中英(chi_sim+eng)，失败则纯英文(eng)。"
when_to_use: "用户发送图片路径/截图时自动触发。先中英混合识别，不行再纯英文。"
---

# OCR 文字识别

使用 Tesseract OCR 引擎识别本地图片中的文字（中英文）。

## 快速使用

```bash
export TESSDATA_PREFIX="C:/Users/17384/AppData/Local/tesseract/tessdata"
"C:\Program Files\Tesseract-OCR\tesseract.exe" "<图片路径>" stdout -l chi_sim+eng
```

如果只有英文：
```bash
"C:\Program Files\Tesseract-OCR\tesseract.exe" "<图片路径>" stdout -l eng
```

## 环境

| 项目 | 路径 |
|------|------|
| Tesseract | `C:\Program Files\Tesseract-OCR\tesseract.exe` |
| 中文语言包 | `C:\Users\17384\AppData\Local\tesseract\tessdata\` |
| 真实 Python | `D:\python\python.exe` |

**必须设置** `TESSDATA_PREFIX` 环境变量，否则找不到语言包。

## 已安装的 OCR 技能

| 技能 | 引擎 | 状态 |
|------|------|------|
| `find-skills` | - | 可用，用于搜索其他技能 |
| `ocr-document-processor` | Tesseract | 可用（和本技能相同） |
| `smart-ocr` | PaddleOCR | 版本冲突，不可用 |
| `paddleocr-text-recognition` | PaddleOCR 云API | 需要密钥+网络，不可用 |

## Python 环境说明

- 不要用 `python3`（WindowsApps 假壳子，会弹窗让你装）
- 用 `D:\python\python.exe`
- 国内 pip 源：`-i https://pypi.tuna.tsinghua.edu.cn/simple`
