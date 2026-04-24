# 使用示例

## 基础用法

### 1. 快速爬取（Example.com）

```bash
node scripts/playwright-simple.js https://example.com
```

**输出：**
```json
{
  "title": "Example Domain",
  "url": "https://example.com/",
  "content": "Example Domain\n\nThis domain is for use...",
  "metaDescription": "",
  "elapsedSeconds": "3.42"
}
```

---

### 2. 有反爬保护的网站（Discuss.com.hk）

```bash
node scripts/playwright-stealth.js "https://m.discuss.com.hk/#hot"
```

**输出：**
```json
{
  "title": "香港討論區 discuss.com.hk",
  "url": "https://m.discuss.com.hk/#hot",
  "htmlLength": 186345,
  "contentPreview": "...",
  "cloudflare": false,
  "screenshot": "./screenshot-1770467444364.png",
  "data": {
    "links": [
      {
        "text": "區議員周潔瑩疑消防通道違泊 道歉稱急於搬貨",
        "href": "https://m.discuss.com.hk/index.php?action=thread&tid=32148378..."
      }
    ]
  },
  "elapsedSeconds": "19.59"
}
```

---

## 高级用法

### 3. 自定义等待时间

```bash
WAIT_TIME=15000 node scripts/playwright-stealth.js <URL>
```

### 4. 显示浏览器（调试模式）

```bash
HEADLESS=false node scripts/playwright-stealth.js <URL>
```

### 5. 保存截图和 HTML

```bash
SCREENSHOT_PATH=/tmp/my-page.png \
SAVE_HTML=true \
node scripts/playwright-stealth.js <URL>
```

### 6. 自定义 User-Agent

```bash
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
node scripts/playwright-stealth.js <URL>
```

---

## 集成示例

### 在 Shell 脚本中使用

```bash
#!/bin/bash
# Run from playwright-scraper-skill directory

URL="https://example.com"
OUTPUT_FILE="result.json"

echo "🕷️  Starting scrape: $URL"

node scripts/playwright-stealth.js "$URL" > "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
  echo "✅ Success! Results saved to: $OUTPUT_FILE"
else
  echo "❌ Failed"
  exit 1
fi
```

### 批量爬取多个 URL

```bash
#!/bin/bash

URLS=(
  "https://example.com"
  "https://example.org"
  "https://example.net"
)

for url in "${URLS[@]}"; do
  echo "Scraping: $url"
  node scripts/playwright-stealth.js "$url" > "output_$(date +%s).json"
  sleep 5  # Avoid IP blocking
done
```

---

## 在 Node.js 中调用

```javascript
const { spawn } = require('child_process');

function scrape(url) {
  return new Promise((resolve, reject) => {
    const proc = spawn('node', [
      'scripts/playwright-stealth.js',
      url
    ]);
    
    let output = '';
    
    proc.stdout.on('data', (data) => {
      output += data.toString();
    });
    
    proc.on('close', (code) => {
      if (code === 0) {
        try {
          // Extract JSON (last line)
          const lines = output.trim().split('\n');
          const json = JSON.parse(lines[lines.length - 1]);
          resolve(json);
        } catch (e) {
          reject(e);
        }
      } else {
        reject(new Error(`Exit code: ${code}`));
      }
    });
  });
}

// Usage
(async () => {
  const result = await scrape('https://example.com');
  console.log(result.title);
})();
```

---

## 常见场景

### 爬取新闻文章

```bash
node scripts/playwright-stealth.js "https://news.example.com/article/123"
```

### 爬取电商产品信息

```bash
WAIT_TIME=10000 \
SAVE_HTML=true \
node scripts/playwright-stealth.js "https://shop.example.com/product/456"
```

### 爬取论坛帖子

```bash
node scripts/playwright-stealth.js "https://forum.example.com/thread/789"
```

---

## 故障排除

### 问题：页面未完全加载

**解决方案：** 增加等待时间
```bash
WAIT_TIME=20000 node scripts/playwright-stealth.js <URL>
```

### 问题：仍被 Cloudflare 拦截

**解决方案：** 使用有头模式 + 增加等待时间
```bash
HEADLESS=false \
WAIT_TIME=30000 \
node scripts/playwright-stealth.js <URL>
```

### 问题：需要登录

**解决方案：** 先手动登录，导出 Cookie，然后加载
（未来功能，目前暂不支持）

---

## 性能优化建议

1. **并行爬取：** 使用 `Promise.all()` 或 Shell 的 `&`
2. **请求间隔：** `sleep 5` 避免 IP 被封
3. **使用代理：** 轮换 IP（未来功能）
4. **缓存结果：** 避免重复爬取

---

更多信息请查看 [SKILL.md](../SKILL.md)
