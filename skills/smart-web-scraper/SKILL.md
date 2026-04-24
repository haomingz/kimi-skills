---
name: smart-web-scraper
description: "基于 Playwright 智能爬取网页内容，内置绕过 Cloudflare 等反爬机制的能力，提供简单模式和隐身模式两种方案以应对不同反爬强度，输出网页标题、文本内容和截图。当用户需要抓取动态网页、获取被保护网站的数据，或提到爬虫、反爬虫、Cloudflare、网页截图、JavaScript渲染等关键词时触发。"
version: 1.2.0
author: Simon Chan
---

<!-- 本地化自: playwright-scraper-skill -->

# Playwright 网页爬取工具

基于 Playwright 的网页爬取 OpenClaw Skill，内置反爬虫保护机制。可根据目标网站的反爬级别选择最佳方案。

---

## 🎯 使用场景矩阵

| 目标网站 | 反爬级别 | 推荐方案 | 脚本 |
|---------|---------|---------|------|
| **普通网站** | 低 | web_fetch 工具 | 无需脚本（内置） |
| **动态网站** | 中 | Playwright 简单模式 | `scripts/playwright-simple.js` |
| **Cloudflare 防护网站** | 高 | **Playwright 隐身模式** ⭐ | `scripts/playwright-stealth.js` |
| **YouTube** | 特殊 | deep-scraper | 需单独安装 |
| **Reddit** | 特殊 | reddit-scraper | 需单独安装 |

---

## 📦 安装

```bash
cd playwright-scraper-skill
npm install
npx playwright install chromium
```

---

## 🚀 快速开始

### 1️⃣ 简单网站（无反爬保护）

使用 OpenClaw 内置的 `web_fetch` 工具：

```bash
# Invoke directly in OpenClaw
Hey, fetch me the content from https://example.com
```

---

### 2️⃣ 动态网站（需要 JavaScript 渲染）

使用 **Playwright 简单模式**：

```bash
node scripts/playwright-simple.js "https://example.com"
```

**示例输出：**
```json
{
  "url": "https://example.com",
  "title": "Example Domain",
  "content": "...",
  "elapsedSeconds": "3.45"
}
```

---

### 3️⃣ 有反爬保护的网站（Cloudflare 等）

使用 **Playwright 隐身模式**：

```bash
node scripts/playwright-stealth.js "https://m.discuss.com.hk/#hot"
```

**功能特性：**
- 隐藏自动化标记（`navigator.webdriver = false`）
- 使用真实 User-Agent（iPhone、Android）
- 随机延迟模拟真人行为
- 支持截图和 HTML 保存

---

### 4️⃣ YouTube 视频字幕

使用 **deep-scraper**（需单独安装）：

```bash
# Install deep-scraper skill
npx clawhub install deep-scraper

# Use it
cd skills/deep-scraper
node assets/youtube_handler.js "https://www.youtube.com/watch?v=VIDEO_ID"
```

---

## 📖 脚本说明

### `scripts/playwright-simple.js`
- **适用场景：** 普通动态网站
- **速度：** 快（3-5 秒）
- **反爬能力：** 无
- **输出格式：** JSON（标题、内容、URL）

### `scripts/playwright-stealth.js` ⭐
- **适用场景：** 带有 Cloudflare 或反爬保护的网站
- **速度：** 中等（5-20 秒）
- **反爬能力：** 中高（隐藏自动化特征、真实 UA）
- **输出格式：** JSON + 截图 + HTML 文件
- **验证结果：** 在 Discuss.com.hk 上 100% 成功

---

## 🎓 最佳实践

### 1. 优先使用 web_fetch
如果网站没有动态加载，使用 OpenClaw 内置的 `web_fetch` 工具——速度最快。

### 2. 需要 JavaScript 渲染？使用简单模式
如果需要等待 JavaScript 渲染完成，使用 `playwright-simple.js`。

### 3. 被拦截了？使用隐身模式
如果遇到 403 错误或 Cloudflare 验证，使用 `playwright-stealth.js`。

### 4. 特殊网站使用专用工具
- YouTube → deep-scraper
- Reddit → reddit-scraper
- Twitter → bird skill

---

## 🔧 自定义配置

所有脚本支持通过环境变量配置：

```bash
# Set screenshot path
SCREENSHOT_PATH=/path/to/screenshot.png node scripts/playwright-stealth.js URL

# Set wait time (milliseconds)
WAIT_TIME=10000 node scripts/playwright-simple.js URL

# Enable headful mode (show browser)
HEADLESS=false node scripts/playwright-stealth.js URL

# Save HTML
SAVE_HTML=true node scripts/playwright-stealth.js URL

# Custom User-Agent
USER_AGENT="Mozilla/5.0 ..." node scripts/playwright-stealth.js URL
```

---

## 📊 性能对比

| 方案 | 速度 | 反爬能力 | 成功率（Discuss.com.hk） |
|------|------|---------|------------------------|
| web_fetch | ⚡ 最快 | ❌ 无 | 0% |
| Playwright 简单模式 | 🚀 快 | ⚠️ 低 | 20% |
| **Playwright 隐身模式** | ⏱️ 中等 | ✅ 中等 | **100%** ✅ |
| Puppeteer 隐身模式 | ⏱️ 中等 | ✅ 中高 | ~80% |
| Crawlee (deep-scraper) | 🐢 慢 | ❌ 被检测 | 0% |
| Chaser (Rust) | ⏱️ 中等 | ❌ 被检测 | 0% |

---

## 🛡️ 反爬技术总结

从测试中总结的经验：

### ✅ 有效的反爬措施
1. **隐藏 `navigator.webdriver`** — 必不可少
2. **使用真实 User-Agent** — 使用真实设备标识（iPhone、Android）
3. **模拟真人行为** — 随机延迟、滚动页面
4. **避免框架特征** — Crawlee、Selenium 容易被检测
5. **使用 `addInitScript`（Playwright）** — 在页面加载前注入脚本

### ❌ 无效的反爬措施
1. **仅修改 User-Agent** — 远远不够
2. **使用高级框架（Crawlee）** — 更容易被检测
3. **Docker 隔离** — 对 Cloudflare 无效

---

## 🔍 故障排除

### 问题：403 Forbidden
**解决方案：** 使用 `playwright-stealth.js`

### 问题：Cloudflare 验证页面
**解决方案：**
1. 增加等待时间（10-15 秒）
2. 尝试 `headless: false`（有头模式有时成功率更高）
3. 考虑使用代理 IP

### 问题：空白页面
**解决方案：**
1. 增加 `waitForTimeout` 时间
2. 使用 `waitUntil: 'networkidle'` 或 `'domcontentloaded'`
3. 检查是否需要登录

---

## 📝 经验记录

### 2026-02-07 Discuss.com.hk 测试结论
- ✅ **纯 Playwright + 隐身模式**成功（5秒，200 OK）
- ❌ Crawlee (deep-scraper) 失败（403）
- ❌ Chaser (Rust) 失败（Cloudflare）
- ❌ Puppeteer 标准模式失败（403）

**最佳方案：** 纯 Playwright + 反爬技术（不依赖特定框架）

---

## 🚧 未来改进计划

- [ ] 添加代理 IP 轮换
- [ ] 实现 Cookie 管理（维持登录状态）
- [ ] 添加验证码处理（2captcha / Anti-Captcha）
- [ ] 批量爬取（并行处理多个 URL）
- [ ] 与 OpenClaw 的 `browser` 工具集成

---

## 📚 参考资料

- [Playwright 官方文档](https://playwright.dev/)
- [puppeteer-extra-plugin-stealth](https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth)
- [deep-scraper skill](https://clawhub.com/opsun/deep-scraper)
