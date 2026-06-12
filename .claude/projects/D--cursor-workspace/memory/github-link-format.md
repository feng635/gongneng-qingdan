---
name: GitHub 链接格式偏好
description: 发 GitHub 链接要精确定位到具体文件，不能只到目录页
type: feedback
---

发 GitHub 链接时用 `blob/main/路径/文件名` 定位到具体内容页，不能用 `tree/main/路径/` 目录页。枫在 Cursor 终端里点击目录页链接会 404 或看不懂。

**Why:** 目录页显示整个仓库文件列表，枫看不懂也找不到重点。直接定到文件内容页才能看到东西。

**How to apply:** 例如 ECC 技能用 `https://github.com/affaan-m/ECC/blob/main/skills/<技能名>/SKILL.md`，而不是 `https://github.com/affaan-m/ECC/tree/main/skills/<技能名>/`
