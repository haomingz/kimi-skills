# Playwright 网页爬取工具 🕷️

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.40+-blue.svg)](https://playwright.dev/)

基于 Playwright 的网页爬取 OpenClaw Skill，内置反爬虫保护机制。已在 Discuss.com.hk 等复杂网站上验证成功。

> 📦 **安装方法：** 查看 [INSTALL.md](INSTALL.md)  
> 📚 **完整文档：** 查看 [SKILL.md](SKILL.md)  
> 💡 **使用示例：** 查看 [examples/README.md](examples/README.md)

---

## ✨ 特性

- ✅ **纯 Playwright** — 现代、强大、易用
- ✅ **反爬保护** — 隐藏自动化特征、真实 UA
- ✅ **已验证** — 在 Discuss.com.hk 上 100% 成功
- ✅ **简单易用** — 一行命令搞定
- ✅ **可自定义** — 支持环境变量配置

---

## 🚀 快速开始

### 安装

```bash
npm install
npx playwright install chromium
```

### 使用

```bash
# Quick scraping
node scripts/playwright-simple.js https://example.com

# Stealth mode (recommended)
node scripts/playwright-stealth.js "https://m.discuss.com.hk/#hot"
```

---

## 📖 两种模式

| 模式 | 适用场景 | 速度 | 反爬能力 |
|------|---------|------|---------|
| **简单模式** | 普通动态网站 | 快（3-5 秒） | 无 |
| **隐身模式** ⭐ | 有反爬保护的网站 | 中等（5-20 秒） | 中高 |

### 简单模式

适合没有反爬保护的网站：

```bash
node scripts/playwright-simple.js <URL>
```

### 隐身模式（推荐）

适合有 Cloudflare 或反爬保护的网站：

```bash
node scripts/playwright-stealth.js <URL>
```

**反爬技术：**
- 隐藏 `navigator.webdriver`
- 使用真实 User-Agent（iPhone）
- 模拟真人行为
- 支持截图和 HTML 保存

---

## 🎯 自定义配置

所有脚本支持通过环境变量配置：

```bash
# Show browser
HEADLESS=false node scripts/playwright-stealth.js <URL>

# Custom wait time (milliseconds)
WAIT_TIME=10000 node scripts/playwright-stealth.js <URL>

# Save screenshot
SCREENSHOT_PATH=/tmp/page.png node scripts/playwright-stealth.js <URL>

# Save HTML
SAVE_HTML=true node scripts/playwright-stealth.js <URL>

# Custom User-Agent
USER_AGENT="Mozilla/5.0 ..." node scripts/playwright-stealth.js <URL>
```

---

## 📊 测试结果

| 网站 | 结果 | 耗时 |
|------|------|------|
| **Discuss.com.hk** | ✅ 200 OK | 5-20 秒 |
| **Example.com** | ✅ 200 OK | 3-5 秒 |
| **Cloudflare 防护网站** | ✅ 多数成功 | 10-30 秒 |

---

## 📁 文件结构

```
playwright-scraper-skill/
├── scripts/
│   ├── playwright-simple.js       # 简单模式
│   └── playwright-stealth.js      # 隐身模式 ⭐
├── examples/
│   ├── discuss-hk.sh              # Discuss.com.hk 示例
│   └── README.md                  # 更多示例
├── SKILL.md                       # 完整文档
├── INSTALL.md                     # 安装指南
├── README.md                      # 本文件
├── README_ZH.md                   # 中文文档
├── CONTRIBUTING.md                # 贡献指南
├── CHANGELOG.md                   # 版本记录
└── package.json                   # npm 配置
```

---

## 💡 使用建议

1. **优先使用 web_fetch** — OpenClaw 内置工具速度最快
2. **动态网站用简单模式** — 没有反爬保护时
3. **防护网站用隐身模式** ⭐ — 主力工具
4. **特殊网站用专用工具** — YouTube、Reddit 等

---

## 🐛 故障排除

### 被 403 拦截？

使用隐身模式：
```bash
node scripts/playwright-stealth.js <URL>
```

### Cloudflare 验证？

增加等待时间 + 有头模式：
```bash
HEADLESS=false WAIT_TIME=30000 node scripts/playwright-stealth.js <URL>
```

### 找不到 Playwright？

重新安装：
```bash
npm install
npx playwright install chromium
```

更多问题请查看 [INSTALL.md](INSTALL.md)

---

## 🤝 参与贡献

欢迎贡献！查看 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 许可证

MIT License - 查看 [LICENSE](LICENSE)

---

## 🔗 相关链接

- [Playwright 官方文档](https://playwright.dev/)
- [完整文档 (SKILL.md)](SKILL.md)
- [安装指南 (INSTALL.md)](INSTALL.md)
- [使用示例 (examples/)](examples/)
