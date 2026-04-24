# Kimi Skills 技能库

本目录收录了 Kimi 官方技能库中所有 120 个技能，以及 kimi-cli 项目自带的 9 个工具技能，共计 **129 个技能**。

每个技能以独立目录存放，`SKILL.md` 为主入口文件，部分技能还包含参考资料、脚本及模板。

---

## 目录

- [投资研究与金融分析](#-投资研究与金融分析)
- [创业与商业策略](#-创业与商业策略)
- [营销与内容创作](#-营销与内容创作)
- [软件开发工程](#-软件开发工程)
- [数据分析与可视化](#-数据分析与可视化)
- [产品与项目管理](#-产品与项目管理)
- [写作与学术研究](#-写作与学术研究)
- [职场与效率提升](#-职场与效率提升)
- [法律与合规](#-法律与合规)
- [视觉设计与创意排版](#-视觉设计与创意排版)
- [kimi-cli 内置工具](#-kimi-cli-内置工具)

---

## 📈 投资研究与金融分析

> 覆盖股票研究、财报解读、估值模型、量化回测、市场数据获取等专业投研场景。

| 技能目录 | 简介 |
|---------|------|
| [equity-researcher](equity-researcher/) | 机构级投研报告生成，覆盖A股/港股/美股，支持3-5页投资速览和≥25页深度研报两种模式 |
| [equity-research-report-cn](equity-research-report-cn/) | 卖方研究视觉风格投资研报，对标高盛/摩根士丹利风格，支持PDF/DOCX/PPTX输出 |
| [equity-earnings-review](equity-earnings-review/) | 卖方股票财报点评，含EPS超预期分析、盈利预测调整、估值更新、分部业务评述 |
| [stock-research-report-cn](stock-research-report-cn/) | 国泰海通/海通国际风格证券研究报告，支持个股研究、行业跟踪 |
| [financial-report-reader](financial-report-reader/) | 财报三表（利润表/资产负债表/现金流）深度解读，自动进行同比/环比变动分析与财务异常检测 |
| [stock-finance-profiler](stock-finance-profiler/) | 基于三张财务报表计算20+核心财务指标，进行详细杜邦分析 |
| [stock-tech-analysis](stock-tech-analysis/) | OHLCV技术指标分析，计算MA/MACD/RSI/布林带/KDJ等15+指标，生成多空信号报告 |
| [fund-risk-analyzer](fund-risk-analyzer/) | ETF多维对比，计算年化收益/最大回撤/夏普比率，生成相关性矩阵图表 |
| [trading-strategy-backtest](trading-strategy-backtest/) | 将投资策略描述转为可运行回测代码，输出回测结果与可视化图表 |
| [cashflow-valuation](cashflow-valuation/) | DCF现金流折现估值模型，含自由现金流预测、终值计算和敏感性分析矩阵 |
| [value-invest-scorer](value-invest-scorer/) | 巴菲特/格雷厄姆风格价值投资评估，从护城河/管理层/财务/估值四维度共20项打分 |
| [event-etf-study](event-etf-study/) | 基于关键事件进行ETF研究，构建市值加权ETF指数，生成交互式HTML仪表盘 |
| [cn-finance-data](cn-finance-data/) | 通过Tushare Pro获取中国金融市场数据，覆盖A股/港股/基金/期货等220+接口 |
| [investment-memo](investment-memo/) | 投资分析备忘录，支持风投式交易备忘录和宏观主题备忘录两种格式 |
| [market-insight-report](market-insight-report/) | 顶级咨询公司视觉风格的数据驱动市场洞察报告，含高管摘要和战略建议 |
| [primary-market-research](primary-market-research/) | PE/VC一级市场行业研究报告，覆盖TMT/消费/医疗等赛道 |
| [commodity-research-outlook](commodity-research-outlook/) | 大宗商品专业研究报告，涵盖能源/金属/农产品，机构级展望报告 |
| [saas-analyzer](saas-analyzer/) | SaaS业务财务分析：计算ARR/流失率/LTV/CAC/NRR等指标，生成健康报告 |

---

## 🚀 创业与商业策略

> 从产品命名到融资路演，覆盖创业公司从0到1的关键商业决策场景。

| 技能目录 | 简介 |
|---------|------|
| [business-plan-ppt](business-plan-ppt/) | 专业投资路演PPT和商业计划书，18页白色+藏青色风格，支持中英文 |
| [fundraising-bp-planner](fundraising-bp-planner/) | 融资BP大纲，完整覆盖六大核心模块，含数据呈现建议与视觉化指引 |
| [pricing-advisor](pricing-advisor/) | SaaS产品定价体系设计，含套餐结构、价值指标、定价页面及涨价策略 |
| [retention-manager](retention-manager/) | 用户挽留与流失防控，设计取消流程、制定挽留方案、优化支付失败恢复 |
| [brand-naming-lab](brand-naming-lab/) | 系统性品牌命名，运用8种经典命名方法，含含义解读、域名建议和商标可注册性评估 |
| [weighted-scoring](weighted-scoring/) | 加权评分决策矩阵，适用于技术选型、供应商选择、方案对比等多准则决策 |
| [okr-planner](okr-planner/) | OKR制定/拆解/复盘教练，涵盖目标设定、关键结果制定与季度评分 |

---

## 📣 营销与内容创作

> 广告文案、SEO、社交媒体、短视频、邮件营销等全渠道内容生产工具。

| 技能目录 | 简介 |
|---------|------|
| [ad-copywriter](ad-copywriter/) | 广告创意写作，适配Google Ads/Meta/LinkedIn/TikTok/Twitter等主流平台 |
| [campaign-planner](campaign-planner/) | 完整营销活动策划，含目标设定/受众分析/渠道策略/内容日历/效果指标 |
| [copy-editor](copy-editor/) | 七轮专业编辑优化营销文案（清晰度/语气/证据/情感/风险消除等） |
| [marketing-writer](marketing-writer/) | 首页/落地页/定价页/功能页等各类页面营销文案写作与转化优化 |
| [seo-analyzer](seo-analyzer/) | 网站SEO诊断，提供技术审计、页面内容分析和可执行优化建议 |
| [seo-copywriting-guide](seo-copywriting-guide/) | 12步结构化SEO内容生成，输出完整草稿/Meta描述/FAQ/EEAT自评清单 |
| [competitive-seo-intel](competitive-seo-intel/) | 竞品SEO策略深度分析，涵盖关键词排名/内容打法/外链画像/AI引用模式 |
| [lp-proto-gen](lp-proto-gen/) | 一键生成完整落地页HTML原型，含Hero/Social Proof/Features/Pricing/CTA五大板块 |
| [ecom-copy-assistant](ecom-copy-assistant/) | 电商商品详情页文案，适配淘宝/京东/亚马逊三大平台风格规范 |
| [wechat-post-craft](wechat-post-craft/) | 微信公众号爆款文章写作，掌握标题党技巧/排版规范/引流CTA设计 |
| [xhs-note-creator](xhs-note-creator/) | 小红书笔记全流程创作，自动撰写内容并渲染生成精美图片卡片 |
| [zhihu-viral-answer](zhihu-viral-answer/) | 知乎高赞回答生成，分析问题类型匹配「故事+干货+金句」最佳结构 |
| [short-video-script](short-video-script/) | 抖音/TikTok/Reels短视频脚本，「3秒Hook→冲突→反转→CTA」黄金结构 |
| [podcast-blueprint](podcast-blueprint/) | 播客节目完整脚本，含开场白/分段话题/预设问题/收尾CTA，带时间戳 |
| [video-outline-planner](video-outline-planner/) | B站视频策划方案，含选题热度评估/结构设计/弹幕互动/一键三连话术 |
| [html-email-builder](html-email-builder/) | 兼容Gmail/Outlook的HTML Newsletter，支持单栏/双栏/Hero Banner等版式 |
| [html-mail-builder](html-mail-builder/) | HTML邮件模板生成，含欢迎/促销/通知/订单确认等场景，响应式设计 |
| [rhetoric-speech-craft](rhetoric-speech-craft/) | 发布会/年会/TED演讲稿，基于修辞三角设计说服策略，自动嵌入舞台提示 |
| [humanizer-zh](humanizer-zh/) | 去除AI生成痕迹，检测并修复夸大象征/宣传性语言/AI词汇等9种常见模式 |

---

## 💻 软件开发工程

> 代码质量、架构设计、API文档、测试、部署、数据库、安全等全栈开发技能。

| 技能目录 | 简介 |
|---------|------|
| [code-arch-optimizer](code-arch-optimizer/) | 探索代码库识别架构摩擦点，输出包含多种接口设计方案的重构建议与RFC |
| [code-safety-audit](code-safety-audit/) | 扫描代码安全漏洞，检测依赖漏洞/密钥泄露/OWASP安全模式 |
| [code-to-chart](code-to-chart/) | 解析import/依赖关系，生成架构图/流程图，支持Python/JS/TS/Go/Java |
| [api-doc-gen](api-doc-gen/) | 从Flask/FastAPI/Express/Gin源码自动扫描路由，生成OpenAPI 3.0规范文档 |
| [ddd-glossary-gen](ddd-glossary-gen/) | 从对话中提取规范领域术语，生成DDD风格统一语言术语表 |
| [dev-guide-writer](dev-guide-writer/) | 技术教程生成器，将技术主题转化为完整教程，含速查表（Cheatsheet） |
| [interface-design-lab](interface-design-lab/) | 为模块生成多种接口设计方案，详细对比简洁性/通用性/深度与易用性 |
| [locale-guard](locale-guard/) | 前端代码库国际化审计，配置i18n/替换硬编码字符串/校验翻译键一致性 |
| [smart-commit-gen](smart-commit-gen/) | Conventional Commits规范化工具，分析git diff自动生成符合规范的提交信息 |
| [smart-web-scraper](smart-web-scraper/) | 基于Playwright智能爬取网页，内置Cloudflare等反爬机制绕过能力 |
| [rust-browser-pilot](rust-browser-pilot/) | Rust高性能浏览器自动化，通过Chrome DevTools协议驱动，速度远超Puppeteer |
| [tdd-coach](tdd-coach/) | 测试驱动开发指导，遵循红-绿-重构循环编写聚焦行为的测试 |
| [software-testing-guide](software-testing-guide/) | 全面软件QA测试流程，含测试策略/用例编写/缺陷追踪/质量指标计算 |
| [http-load-tester](http-load-tester/) | HTTP阶梯式并发压测，采集p50/p90/p99延迟，分析性能拐点，零外部依赖 |
| [py-perf-analyzer](py-perf-analyzer/) | Python性能瓶颈定位，集成cProfile/tracemalloc/line_profiler，可输出JSON报告 |
| [terraform-deploy-traps](terraform-deploy-traps/) | Terraform部署踩坑指南，含provisioner时序/SSH冲突/DNS重复等常见问题修复 |
| [web-security-audit](web-security-audit/) | 基于OWASP Top 10的代码安全审查，含SQL注入/XSS/SSRF等漏洞修复方案 |
| [sql-tutor](sql-tutor/) | SQL查询助手，支持自然语言转SQL/查询优化/EXPLAIN执行计划解读 |
| [programming-tutor](programming-tutor/) | 全能编程导师，支持互动课程/代码审查/苏格拉底式调试引导/算法练习 |
| [database-inspector](database-inspector/) | SQLite/PostgreSQL数据库探索，生成Mermaid ER图，执行安全只读查询 |
| [log-diagnostic](log-diagnostic/) | 分析日志文件错误模式，支持JSON/syslog/Nginx格式，输出错误聚类与频率统计 |
| [git-repo-audit](git-repo-audit/) | 深度分析Git仓库历史，识别热点文件/分析贡献归属/扫描历史密钥泄露 |
| [gitlab-cli-guide](gitlab-cli-guide/) | GitLab命令行工具（glab）完整参考，覆盖MR/CI/CD/Issue管理等30+子命令 |
| [k8s-cluster-ops](k8s-cluster-ops/) | 通过kubectl管理Kubernetes集群，执行查询/部署/日志/调试/监控等操作 |

---

## 📊 数据分析与可视化

> 统计分析、异常检测、图表生成、时间线可视化等数据处理工具。

| 技能目录 | 简介 |
|---------|------|
| [data-viz-gen](data-viz-gen/) | 从JSON数据生成自包含HTML/SVG信息图，支持KPI卡片/柱状图/流程图/仪表盘 |
| [chart-gen](chart-gen/) | 从JSON数据生成高质量PNG/SVG图表，支持折线/柱状/K线/热力图等多种类型 |
| [chrono-flow](chrono-flow/) | 生成交互式时间线HTML页面，支持垂直/水平/双侧三种布局，适配移动端 |
| [dataset-health-audit](dataset-health-audit/) | CSV/Excel/JSON表格数据12维度质量审查，输出质量评分和修复建议 |
| [corr-insight](corr-insight/) | 计算Pearson/Spearman相关矩阵和偏相关分析，自动识别伪相关 |
| [regression-insight](regression-insight/) | 执行线性/逻辑回归分析，输出完整统计结果（R²/p值/VIF）和中文解读 |
| [auto-stat-test](auto-stat-test/) | 自动选择t检验/卡方/ANOVA/Mann-Whitney等统计方法，输出p值和通俗解读 |
| [outlier-scan](outlier-scan/) | CSV数据异常检测，使用Z-score/IQR/移动平均偏离三种方法，自动分类异常点 |
| [split-test-evaluator](split-test-evaluator/) | A/B测试分析，含显著性检验/置信区间/统计功效/最小样本量估算 |
| [risk-heatmap](risk-heatmap/) | 项目风险热力图，生成5×5概率-影响矩阵，含风险评分与应对措施 |
| [sunlight-analysis](sunlight-analysis/) | 生成太阳轨迹图，计算建筑阴影投射范围与全年日照时数，评估热舒适度 |
| [video-compare-tool](video-compare-tool/) | 对比视频压缩质量，计算PSNR/SSIM画质指标，生成逐帧对比HTML报告 |

---

## 📋 产品与项目管理

> 从需求收集到项目交付，覆盖产品经理和项目经理的全流程工作场景。

| 技能目录 | 简介 |
|---------|------|
| [idea-to-prd](idea-to-prd/) | 一句话需求生成完整PRD，含用户故事/功能清单/MoSCoW优先级/验收标准 |
| [user-story-canvas](user-story-canvas/) | 交互式HTML用户故事地图，Epic→Feature→Story三层结构，支持MoSCoW优先级 |
| [gantt-chart-builder](gantt-chart-builder/) | 交互式HTML甘特图，支持关键路径分析（CPM），可视化项目时间线与依赖关系 |
| [iteration-planner](iteration-planner/) | 敏捷Sprint规划助手，基于团队产能完成Sprint范围选定/任务拆分/负载均衡 |
| [incident-retrospective](incident-retrospective/) | 线上事故复盘与Blameless Postmortem，六步SOP含5 Whys根因分析 |
| [workload-calculator](workload-calculator/) | 软件项目工时估算，使用三点估算PERT/T-shirt sizing/功能点分析FPA方法 |
| [sop-writer](sop-writer/) | 将业务流程梳理成SOP文档，含流程图/RACI分工矩阵/操作步骤/异常处理 |
| [meeting-recap](meeting-recap/) | 将会议录音/笔记整理为结构化会议纪要，自动提取议题/结论/行动项 |
| [work-report-writer](work-report-writer/) | 从工作记录和git log生成周报/月报，支持数据导向/叙事型/OKR对齐等风格 |
| [deep-probe](deep-probe/) | 对方案进行连环追问，逐一排查决策树每个分支，直到达成共识 |

---

## ✍️ 写作与学术研究

> 学术论文、研究写作、翻译、记忆卡片、教育出题等学术场景工具。

| 技能目录 | 简介 |
|---------|------|
| [research-writer](research-writer/) | 研究写作全支持：资料调研/补充引用/优化开头/完善结构大纲/逐节反馈 |
| [research-advisor](research-advisor/) | 科研顾问，协助选题构思/项目规划/问题排查，输出研究方案和风险评估矩阵 |
| [research-paper-refiner](research-paper-refiner/) | 学术论文英文润色，按学术写作标准逐段审查语法/用词/语态/逻辑衔接 |
| [paper-review-coach](paper-review-coach/) | 模拟学术同行评审，从原创性/方法论/结果/写作四维度系统分析论文 |
| [ref-style-converter](ref-style-converter/) | 参考文献格式转换（APA/MLA/IEEE/Harvard相互转换），支持批量处理 |
| [xindaya-translator](xindaya-translator/) | 中英双向翻译，遵循信达雅原则，覆盖学术/商务/技术/法律四大领域 |
| [flashcard-studio](flashcard-studio/) | 从学习材料提取核心知识点生成闪卡，输出可直接导入Anki的CSV文件 |
| [bloom-quiz-maker](bloom-quiz-maker/) | 按布鲁姆认知分类学（六层）生成选择题/简答题/案例题，含完整解析 |
| [speech-synthesis](speech-synthesis/) | 文字转高质量语音，支持多语言/多音色，可调节语速音调，输出MP3和字幕 |

---

## 🏢 职场与效率提升

> 简历优化、面试练习、邮件写作、客服话术等职场通用效率工具。

| 技能目录 | 简介 |
|---------|------|
| [resume-craft](resume-craft/) | 简历优化，基于JD进行关键词匹配分析，用STAR法则量化改写，ATS友好度检查 |
| [interview-simulator](interview-simulator/) | 真实面试官追问训练，覆盖行为/技术/案例三大场景，含STAR框架诊断与评分 |
| [pro-email-composer](pro-email-composer/) | 商务邮件写作，涵盖催办/跟进/拒绝/感谢/道歉等场景，支持中英文双语 |
| [email-manager](email-manager/) | 收发和管理邮件，支持Gmail/Outlook/163/QQ邮箱等主流服务商 |
| [audience-adapter](audience-adapter/) | 向上汇报与跨部门沟通，根据受众角色（CEO/VP/技术/运营）自动调整表达策略 |
| [customer-reply-craft](customer-reply-craft/) | 客服话术生成，覆盖售前咨询/售后/投诉/退换货，含五级情绪安抚策略 |
| [adhd-daily-planner](adhd-daily-planner/) | ADHD生活管理助手，通过每日规划/任务拆解/时间感知辅助/情绪支持帮助管理日常 |

---

## ⚖️ 法律与合规

> 合同生成、法律风险评估、合规检查等法律场景辅助工具。

| 技能目录 | 简介 |
|---------|------|
| [legal-contract-gen](legal-contract-gen/) | 通过交互式问答生成NDA/服务协议/隐私政策/合作框架协议等法律文书初稿 |
| [legal-risk-analyzer](legal-risk-analyzer/) | 基于「严重性×发生概率」框架评估法律风险，提供评分/等级/行动建议 |
| [compliance-review-planner](compliance-review-planner/) | 构建合规检查清单，覆盖GDPR/个保法/广告法/数据安全法等主要法规 |
| [tos-risk-checker](tos-risk-checker/) | 以消费者视角审计服务条款，识别霸王条款/数据授权/自动续费等风险 |

---

## 🎨 视觉设计与创意排版

> UI设计提取、科学期刊排版、杂志风格视觉文档等设计创意技能。

| 技能目录 | 简介 |
|---------|------|
| [theme-kit](theme-kit/) | 主题样式工具箱，内置10种预设风格（配色+字体），适用于演示文稿/文档/HTML页面 |
| [ui-blueprint](ui-blueprint/) | 从UI截图提取完整设计系统，生成配色/字体/组件/间距规范，产出MVP界面提示词 |
| [sci-paper-cn](sci-paper-cn/) | CVPR/NeurIPS/ACL等顶会论文撰写排版指南，覆盖分章节起草到camera-ready全流程 |
| [astro-observation-report-cn](astro-observation-report-cn/) | 引力波观测结果论文撰写，复刻《Physical Review X》双栏期刊风格 |
| [photo-magazine-cn](photo-magazine-cn/) | 杂志级高端报告设计，粗体大字排版/满版摄影/数据可视化卡片/叙事化版面 |
| [journalistic-portrait-cn](journalistic-portrait-cn/) | 复刻《南方人物周刊》视觉风格的中文杂志HTML网页，适用于人物特稿版面 |
| [geo-magazine-slides-cn](geo-magazine-slides-cn/) | 地理杂志风格演示文稿（PPTX），适用于地点合集/旅行目的地/建筑作品集 |
| [retro-tech-illustration-cn](retro-tech-illustration-cn/) | 复古科技艺术风格视觉内容，覆盖Synthwave/Vaporwave/Cyberpunk等美学 |
| [fashion-sketch-cn](fashion-sketch-cn/) | 专业服装技术规格包（Tech Pack），含系列概览/款式规格/尺寸表/BOM清单 |

---

## 🔧 kimi-cli 内置工具

> 来自 [MoonshotAI/kimi-cli](https://github.com/MoonshotAI/kimi-cli) 项目的开发者工具技能，专为 Kimi Code CLI 工作流设计。

| 技能目录 | 简介 |
|---------|------|
| [codex-worker](codex-worker/) | 通过tmux并行启动和管理多个Codex CLI代理，用于分解独立子任务并行执行 |
| [feature-smoke-test](feature-smoke-test/) | 针对Kimi Code CLI新增/变更功能规划并执行可重复的端到端冒烟测试 |
| [gen-changelog](gen-changelog/) | 为代码变更生成规范化的Changelog条目 |
| [gen-docs](gen-docs/) | 更新Kimi Code CLI用户文档 |
| [gen-rust](gen-rust/) | 将Python变更同步到Rust实现，跳过UI/登录相关部分 |
| [pull-request](pull-request/) | 创建并提交GitHub Pull Request |
| [release](release/) | 执行Kimi Code CLI包的发布工作流 |
| [translate-docs](translate-docs/) | 翻译并同步双语文档 |
| [worktree-status](worktree-status/) | 审计当前项目所有git worktree状态，识别可安全清理的工作树 |

---

## 其他

| 技能目录 | 简介 |
|---------|------|
| [kimi-skills-finder](kimi-skills-finder/) | 帮助用户搜索和发现技能，根据用户需求推荐最适合的技能 |

---

## 统计

| 来源 | 数量 |
|------|------|
| Kimi 官方技能库 | 120 |
| kimi-cli 内置工具 | 9 |
| **合计** | **129** |
