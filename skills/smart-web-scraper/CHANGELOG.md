# 更新日志

## [1.2.0] - 2026-02-07

### 🔄 重大变更

- **项目重命名** — `web-scraper` → `playwright-scraper-skill`
- 更新了所有文档和链接
- 更新了 GitHub 仓库名称
- **双语文档** — 所有文档提供英文版本（同时提供中文 README）

---

## [1.1.0] - 2026-02-07

### ✅ 新增

- **LICENSE** — MIT 开源许可证
- **CONTRIBUTING.md** — 贡献指南
- **examples/README.md** — 详细使用示例
- **test.sh** — 自动化测试脚本
- **README.md** — 重新设计，添加徽章

### 🔧 改进

- 更清晰的文件结构
- 更详细的文档说明
- 更实用的示例

---

## [1.0.0] - 2026-02-07

### ✅ 初始版本

**创建的工具：**
- ✅ `playwright-simple.js` — 快速简单爬取脚本
- ✅ `playwright-stealth.js` — 反爬保护版本（主力工具）⭐

**测试结果：**
- ✅ Discuss.com.hk 爬取成功（200 OK，19.6 秒）
- ✅ Example.com 爬取成功（3.4 秒）
- ✅ 可自动降级到 deep-scraper 的 Playwright

**文档：**
- ✅ SKILL.md（完整文档）
- ✅ README.md（快速参考）
- ✅ 示例脚本（discuss-hk.sh）
- ✅ package.json

**关键发现：**
1. **Playwright 隐身模式是最佳方案**（在 Discuss.com.hk 上 100% 成功）
2. **不要使用 Crawlee**（容易被检测）
3. **Chaser (Rust) 目前不可用**（被 Cloudflare 拦截）
4. **隐藏 `navigator.webdriver` 是关键**

---

## 未来计划

- [ ] 添加代理 IP 轮换
- [ ] 验证码处理集成
- [ ] Cookie 管理（维持登录状态）
- [ ] 批量爬取（并行处理）
- [ ] 与 OpenClaw browser 工具集成
