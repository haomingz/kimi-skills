# 安装指南

## 📦 快速安装

### 1. 克隆或下载本工具

```bash
# Method 1: Using git clone (if public repo)
git clone https://github.com/waisimon/playwright-scraper-skill.git
cd playwright-scraper-skill

# Method 2: Download ZIP and extract
# After downloading, enter the directory
cd playwright-scraper-skill
```

### 2. 安装依赖

```bash
# Install Playwright (recommended)
npm install

# Install browser (Chromium)
npx playwright install chromium
```

### 3. 测试

```bash
# Quick test
node scripts/playwright-simple.js https://example.com

# Test Stealth version
node scripts/playwright-stealth.js https://example.com
```

---

## 🔧 高级安装

### 在 OpenClaw 中使用

如果你正在使用 OpenClaw，可以将本工具放置到 skills 目录中：

```bash
# Assuming your OpenClaw workspace is at ~/.openclaw/workspace
cp -r playwright-scraper-skill ~/.openclaw/workspace/skills/

# Then you can invoke it in OpenClaw
```

---

## ✅ 验证安装

运行示例脚本：

```bash
# Discuss.com.hk example (verified working)
bash examples/discuss-hk.sh
```

如果看到类似以下输出，说明安装成功：

```
🕷️  Starting Playwright Stealth scraper...
📱 Navigating to: https://m.discuss.com.hk/#hot
📡 HTTP Status: 200
✅ Scraping complete!
```

---

## 🐛 常见问题

### 问题：找不到 Playwright

**错误信息：** `Error: Cannot find module 'playwright'`

**解决方案：**
```bash
npm install
npx playwright install chromium
```

### 问题：浏览器启动失败

**错误信息：** `browserType.launch: Executable doesn't exist`

**解决方案：**
```bash
npx playwright install chromium
```

### 问题：权限错误

**错误信息：** `Permission denied`

**解决方案：**
```bash
chmod +x scripts/*.js
chmod +x examples/*.sh
```

---

## 📝 系统要求

- **Node.js：** 推荐 v18+
- **操作系统：** macOS / Linux / Windows
- **磁盘空间：** 约 500MB（包含 Chromium）
- **内存：** 推荐 2GB+

---

## 🚀 下一步

安装完成后，请查阅：
- [README.md](README.md) — 快速参考
- [SKILL.md](SKILL.md) — 完整文档
- [examples/](examples/) — 使用示例
