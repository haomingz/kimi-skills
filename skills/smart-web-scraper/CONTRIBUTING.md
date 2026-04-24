# 贡献指南

感谢你考虑为 playwright-scraper-skill 项目做出贡献！

## 🐛 报告问题

如果你发现了 Bug 或有功能建议：

1. 先查看 [Issues](https://github.com/waisimon/playwright-scraper-skill/issues) 是否已有相关问题
2. 如果没有，创建一个新的 Issue
3. 请提供以下信息：
   - 问题描述
   - 复现步骤
   - 期望行为与实际行为
   - 运行环境（Node.js 版本、操作系统）
   - 错误信息（如有）

## 💡 功能建议

1. 创建一个标题包含 `[Feature Request]` 的 Issue
2. 说明：
   - 期望的功能
   - 使用场景
   - 为什么这个功能有价值

## 🔧 提交代码

### 搭建开发环境

```bash
# Fork the repo and clone
git clone https://github.com/YOUR_USERNAME/playwright-scraper-skill.git
cd playwright-scraper-skill

# Install dependencies
npm install
npx playwright install chromium

# Test
node scripts/playwright-simple.js https://example.com
```

### 贡献流程

1. 创建新分支：
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. 进行修改

3. 测试你的改动：
   ```bash
   npm test
   node scripts/playwright-stealth.js <test-URL>
   ```

4. 提交：
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

5. 推送并创建 Pull Request：
   ```bash
   git push origin feature/my-new-feature
   ```

### 提交信息规范

请使用清晰的提交信息：

- `Add: new feature`
- `Fix: issue description`
- `Update: existing feature`
- `Refactor: code refactoring`
- `Docs: documentation update`
- `Test: add or modify tests`

示例：
```
Fix: playwright-stealth.js screenshot timeout issue

- Increase timeout parameter to 10 seconds
- Add try-catch error handling
- Update documentation
```

## 📝 文档

如果你的改动影响了使用方式：

- 更新 `SKILL.md`（完整文档）
- 更新 `README.md`（快速参考）
- 更新 `examples/README.md`（如有新增示例）
- 更新 `CHANGELOG.md`（记录变更）

## ✅ 提交前检查清单

提交 PR 前请确认：

- [ ] 代码能正常运行
- [ ] 没有破坏已有功能
- [ ] 已更新相关文档
- [ ] 提交信息清晰明了
- [ ] 未包含敏感信息（API 密钥、个人路径等）

## 🎯 优先贡献方向

目前欢迎以下方向的贡献：

1. **新的反爬技术** — 提高爬取成功率
2. **支持更多网站** — 测试并分享成功案例
3. **性能优化** — 提升爬取速度
4. **错误处理** — 更友好的错误信息和恢复机制
5. **文档改进** — 更清晰的说明和示例

## 🚫 不接受的贡献

- 添加复杂的依赖（保持轻量化）
- 违反隐私或法律的功能
- 破坏现有 API 的改动（除非有充分理由）

## 📞 联系方式

有问题欢迎：
- 创建 Issue 讨论
- 在 Pull Request 评论中提问

---

感谢你的贡献！🙏
