# Kimi Skills

This directory is the skill catalog: **120** skills from the official Kimi library and **9** tool skills shipped with kimi-cli, **129** in total. The previous Chinese index is archived as [README.zh-CN.md](README.zh-CN.md).

Each skill is its own directory. `SKILL.md` is the entry file. Some skills also include references, scripts, and templates.

---

## Contents

- [Investment research and financial analysis](#-investment-research-and-financial-analysis)
- [Startups and business strategy](#-startups-and-business-strategy)
- [Marketing and content](#-marketing-and-content)
- [Software engineering](#-software-engineering)
- [Data analysis and visualization](#-data-analysis-and-visualization)
- [Product and project management](#-product-and-project-management)
- [Writing and academic research](#-writing-and-academic-research)
- [Workplace productivity](#-workplace-productivity)
- [Legal and compliance](#-legal-and-compliance)
- [Visual design and layout](#-visual-design-and-layout)
- [kimi-cli built-in tools](#-kimi-cli-built-in-tools)

---

## 📈 Investment research and financial analysis

> Equity research, financial statements, valuation, backtests, and market data.

| Skill | Summary |
|---------|------|
| [equity-researcher](equity-researcher/) | Institutional equity research for A-shares, Hong Kong, and the US. Two modes: a 3–5 page tear sheet and a deep report of 25 pages or more |
| [equity-research-report-cn](equity-research-report-cn/) | Sell-side research reports in a Goldman Sachs / Morgan Stanley visual style. Output as PDF, DOCX, or PPTX |
| [equity-earnings-review](equity-earnings-review/) | Sell-side earnings reviews: EPS surprise, forecast revisions, valuation updates, and segment commentary |
| [stock-research-report-cn](stock-research-report-cn/) | Guotai Haitong / Haitong International style research notes for single names and industry updates |
| [financial-report-reader](financial-report-reader/) | Reads the income statement, balance sheet, and cash flow statement. Flags year-over-year and sequential changes and financial anomalies |
| [stock-finance-profiler](stock-finance-profiler/) | Computes 20+ ratios from the three statements and runs a DuPont breakdown |
| [stock-tech-analysis](stock-tech-analysis/) | OHLCV technicals: MA, MACD, RSI, Bollinger Bands, KDJ, and 15+ other indicators, with a long/short signal report |
| [fund-risk-analyzer](fund-risk-analyzer/) | Compares ETFs on annualized return, max drawdown, and Sharpe ratio, and plots a correlation matrix |
| [trading-strategy-backtest](trading-strategy-backtest/) | Turns a strategy description into runnable backtest code, with results and charts |
| [cashflow-valuation](cashflow-valuation/) | DCF model: free-cash-flow forecast, terminal value, and a sensitivity matrix |
| [value-invest-scorer](value-invest-scorer/) | Buffett / Graham style scorecard: moat, management, financials, and valuation, 20 items in four groups |
| [event-etf-study](event-etf-study/) | Event-driven ETF study. Builds a market-cap-weighted ETF index and an interactive HTML dashboard |
| [cn-finance-data](cn-finance-data/) | China market data through Tushare Pro: A-shares, Hong Kong, funds, futures, and 220+ endpoints |
| [investment-memo](investment-memo/) | Investment memos in two formats: a venture deal memo and a macro theme memo |
| [market-insight-report](market-insight-report/) | Consulting-style, data-driven market insight report with an executive summary and strategic recommendations |
| [primary-market-research](primary-market-research/) | PE/VC industry research for TMT, consumer, healthcare, and similar tracks |
| [commodity-research-outlook](commodity-research-outlook/) | Institutional commodity outlooks for energy, metals, and agriculture |
| [saas-analyzer](saas-analyzer/) | SaaS metrics: ARR, churn, LTV, CAC, NRR, and a health report |

---

## 🚀 Startups and business strategy

> Naming, pricing, fundraising, and the other decisions that take a company from zero to one.

| Skill | Summary |
|---------|------|
| [business-plan-ppt](business-plan-ppt/) | Investor pitch deck and business plan. 18 pages, white and navy, in Chinese or English |
| [fundraising-bp-planner](fundraising-bp-planner/) | Fundraising business-plan outline across six core sections, with guidance on data and visuals |
| [pricing-advisor](pricing-advisor/) | SaaS pricing: packages, value metric, pricing page, and a price-increase plan |
| [retention-manager](retention-manager/) | Churn prevention: cancel flows, save offers, and failed-payment recovery |
| [brand-naming-lab](brand-naming-lab/) | Systematic naming with eight classic methods, plus meaning, domain ideas, and a trademark screen |
| [weighted-scoring](weighted-scoring/) | Weighted decision matrix for vendor choice, technical selection, and other multi-criteria calls |
| [okr-planner](okr-planner/) | OKR coach for setting objectives, writing key results, and scoring the quarter |

---

## 📣 Marketing and content

> Ads, SEO, social, short video, and email across channels.

| Skill | Summary |
|---------|------|
| [ad-copywriter](ad-copywriter/) | Ad creative for Google Ads, Meta, LinkedIn, TikTok, Twitter, and similar platforms |
| [campaign-planner](campaign-planner/) | Full campaign plan: goals, audience, channels, content calendar, and success metrics |
| [copy-editor](copy-editor/) | Seven-pass edit of marketing copy: clarity, voice, evidence, emotion, and risk reversal |
| [marketing-writer](marketing-writer/) | Page copy and conversion writing for homepages, landing pages, pricing pages, and feature pages |
| [seo-analyzer](seo-analyzer/) | Site SEO diagnosis: technical audit, on-page review, and prioritized fixes |
| [seo-copywriting-guide](seo-copywriting-guide/) | 12-step SEO article: full draft, meta description, FAQ, and an E-E-A-T checklist |
| [competitive-seo-intel](competitive-seo-intel/) | Competitor SEO: rankings, content patterns, backlink profile, and AI-citation patterns |
| [lp-proto-gen](lp-proto-gen/) | One-shot landing-page HTML: hero, social proof, features, pricing, and CTA |
| [ecom-copy-assistant](ecom-copy-assistant/) | Product-detail copy styled for Taobao, JD.com, and Amazon |
| [wechat-post-craft](wechat-post-craft/) | WeChat official-account posts: headlines, layout, and a follow CTA |
| [xhs-note-creator](xhs-note-creator/) | Xiaohongshu notes end to end: writes the copy and renders image cards |
| [zhihu-viral-answer](zhihu-viral-answer/) | Zhihu answers matched to the question type, using story, substance, and a closing line |
| [short-video-script](short-video-script/) | Douyin / TikTok / Reels scripts: 3-second hook, conflict, turn, CTA |
| [podcast-blueprint](podcast-blueprint/) | Full podcast script with cold open, segments, prepared questions, close, and timestamps |
| [video-outline-planner](video-outline-planner/) | Bilibili video plan: topic heat, structure, danmaku beats, and an end-screen ask |
| [html-email-builder](html-email-builder/) | HTML newsletters that render in Gmail and Outlook: single column, two column, or hero banner |
| [html-mail-builder](html-mail-builder/) | Responsive HTML email templates for welcome, promo, notification, and order confirmation |
| [rhetoric-speech-craft](rhetoric-speech-craft/) | Launch, annual-meeting, and TED-style speeches, with rhetorical strategy and stage directions |
| [humanizer-zh](humanizer-zh/) | Strips common AI tells: inflated symbols, promotional tone, stock AI vocabulary, and six other patterns |

---

## 💻 Software engineering

> Code quality, architecture, API docs, tests, deploy, databases, and security.

| Skill | Summary |
|---------|------|
| [code-arch-optimizer](code-arch-optimizer/) | Finds architectural friction in a codebase and writes a refactor RFC with several interface options |
| [code-safety-audit](code-safety-audit/) | Scans for vulnerable dependencies, leaked secrets, and OWASP-style security issues |
| [code-to-chart](code-to-chart/) | Maps imports and dependencies into architecture and flow diagrams for Python, JS, TS, Go, and Java |
| [api-doc-gen](api-doc-gen/) | Scans Flask, FastAPI, Express, and Gin routes and emits an OpenAPI 3.0 spec |
| [ddd-glossary-gen](ddd-glossary-gen/) | Pulls domain terms out of a conversation and writes a DDD ubiquitous-language glossary |
| [dev-guide-writer](dev-guide-writer/) | Turns a technical topic into a tutorial plus a cheatsheet |
| [interface-design-lab](interface-design-lab/) | Drafts several module interfaces and compares them on simplicity, generality, depth, and ease of use |
| [locale-guard](locale-guard/) | i18n audit: wire up i18n, replace hardcoded strings, and check translation-key consistency |
| [smart-commit-gen](smart-commit-gen/) | Reads a git diff and writes a Conventional Commits message |
| [smart-web-scraper](smart-web-scraper/) | Playwright scraper with built-in handling for Cloudflare and similar bot checks |
| [rust-browser-pilot](rust-browser-pilot/) | Fast browser automation in Rust over the Chrome DevTools Protocol |
| [tdd-coach](tdd-coach/) | Test-driven development coach: red, green, refactor, with behavior-focused tests |
| [software-testing-guide](software-testing-guide/) | QA workflow: test strategy, cases, defect tracking, and quality metrics |
| [http-load-tester](http-load-tester/) | Stepped HTTP concurrency test. Collects p50/p90/p99 and looks for the knee. No extra dependencies |
| [py-perf-analyzer](py-perf-analyzer/) | Finds Python bottlenecks with cProfile, tracemalloc, and line_profiler. Can emit JSON |
| [terraform-deploy-traps](terraform-deploy-traps/) | Terraform deploy traps: provisioner ordering, SSH conflicts, duplicate DNS, and similar fixes |
| [web-security-audit](web-security-audit/) | OWASP Top 10 review with fixes for SQL injection, XSS, SSRF, and related issues |
| [sql-tutor](sql-tutor/) | Natural language to SQL, query tuning, and EXPLAIN walkthroughs |
| [programming-tutor](programming-tutor/) | Programming tutor: lessons, code review, Socratic debugging, and algorithm drills |
| [database-inspector](database-inspector/) | Explores SQLite and PostgreSQL, draws a Mermaid ER diagram, and runs read-only queries |
| [log-diagnostic](log-diagnostic/) | Clusters errors in JSON, syslog, and Nginx logs and reports frequency |
| [git-repo-audit](git-repo-audit/) | Git history audit: hot files, contribution ownership, and secrets that were committed |
| [gitlab-cli-guide](gitlab-cli-guide/) | glab reference covering merge requests, CI/CD, issues, and 30+ other commands |
| [k8s-cluster-ops](k8s-cluster-ops/) | kubectl workflows for inspect, deploy, logs, debug, and monitoring |

---

## 📊 Data analysis and visualization

> Statistics, anomaly detection, charts, and timelines.

| Skill | Summary |
|---------|------|
| [data-viz-gen](data-viz-gen/) | Self-contained HTML/SVG infographics from JSON: KPI cards, bars, flows, and dashboards |
| [chart-gen](chart-gen/) | PNG and SVG charts from JSON: line, bar, candlestick, heatmap, and more |
| [chrono-flow](chrono-flow/) | Interactive HTML timelines in vertical, horizontal, or two-sided layouts, including mobile |
| [dataset-health-audit](dataset-health-audit/) | 12-dimension quality review of CSV, Excel, and JSON tables, with a score and fixes |
| [corr-insight](corr-insight/) | Pearson and Spearman matrices plus partial correlation, with spurious correlations called out |
| [regression-insight](regression-insight/) | Linear and logistic regression with R², p-values, VIF, and a plain-language readout |
| [auto-stat-test](auto-stat-test/) | Picks t-test, chi-square, ANOVA, Mann-Whitney, or a similar test, and explains the p-value |
| [outlier-scan](outlier-scan/) | Outliers in CSV via z-score, IQR, and moving-average deviation, then classified |
| [split-test-evaluator](split-test-evaluator/) | A/B analysis: significance, confidence interval, power, and minimum sample size |
| [risk-heatmap](risk-heatmap/) | 5×5 probability-impact risk heatmap with scores and responses |
| [sunlight-analysis](sunlight-analysis/) | Sun-path diagrams, building shadow, annual sun hours, and thermal comfort |
| [video-compare-tool](video-compare-tool/) | Compares video compression with PSNR and SSIM and writes a frame-by-frame HTML report |

---

## 📋 Product and project management

> From intake to delivery for product and project work.

| Skill | Summary |
|---------|------|
| [idea-to-prd](idea-to-prd/) | Turns a one-line request into a PRD: user stories, feature list, MoSCoW priority, and acceptance criteria |
| [user-story-canvas](user-story-canvas/) | Interactive HTML story map: epic, feature, story, with MoSCoW priority |
| [gantt-chart-builder](gantt-chart-builder/) | Interactive HTML Gantt chart with critical-path analysis and dependency lines |
| [iteration-planner](iteration-planner/) | Sprint planning from team capacity: scope, task split, and load balance |
| [incident-retrospective](incident-retrospective/) | Blameless postmortem in six steps, including a 5 Whys root-cause pass |
| [workload-calculator](workload-calculator/) | Effort estimates with three-point PERT, T-shirt sizing, and function-point analysis |
| [sop-writer](sop-writer/) | Turns a business process into an SOP: flowchart, RACI, steps, and exception handling |
| [meeting-recap](meeting-recap/) | Turns notes or a transcript into minutes with topics, decisions, and action items |
| [work-report-writer](work-report-writer/) | Weekly or monthly reports from work logs and git history, in a data, narrative, or OKR style |
| [deep-probe](deep-probe/) | Stress-tests a plan by walking every branch of the decision tree until the group agrees |

---

## ✍️ Writing and academic research

> Papers, research writing, translation, flashcards, and quizzes.

| Skill | Summary |
|---------|------|
| [research-writer](research-writer/) | Research writing support: source gathering, citations, openings, outlines, and section feedback |
| [research-advisor](research-advisor/) | Research advisor for topic choice, project planning, and troubleshooting, with a plan and a risk matrix |
| [research-paper-refiner](research-paper-refiner/) | Academic English line edit: grammar, word choice, voice, and logical links |
| [paper-review-coach](paper-review-coach/) | Simulated peer review across originality, method, results, and writing |
| [ref-style-converter](ref-style-converter/) | Converts references among APA, MLA, IEEE, and Harvard, including batches |
| [xindaya-translator](xindaya-translator/) | Chinese–English translation for academic, business, technical, and legal text |
| [flashcard-studio](flashcard-studio/) | Pulls key facts from study material into flashcards and an Anki-ready CSV |
| [bloom-quiz-maker](bloom-quiz-maker/) | Quizzes across Bloom's six levels: multiple choice, short answer, and cases, with explanations |
| [speech-synthesis](speech-synthesis/) | Text to speech in multiple languages and voices, with rate and pitch control, MP3, and subtitles |

---

## 🏢 Workplace productivity

> Resumes, interviews, email, and customer replies.

| Skill | Summary |
|---------|------|
| [resume-craft](resume-craft/) | Resume rewrite against a job description: keyword match, STAR quantification, and an ATS check |
| [interview-simulator](interview-simulator/) | Interview practice with follow-ups for behavioral, technical, and case rounds, plus a STAR score |
| [pro-email-composer](pro-email-composer/) | Business email for chase, follow-up, decline, thanks, and apology, in Chinese or English |
| [email-manager](email-manager/) | Send, receive, and file mail for Gmail, Outlook, 163, QQ Mail, and similar providers |
| [audience-adapter](audience-adapter/) | Rewrites a message for the audience: CEO, VP, engineering, or operations |
| [customer-reply-craft](customer-reply-craft/) | Support replies for pre-sales, after-sales, complaints, and returns, with a five-level de-escalation scale |
| [adhd-daily-planner](adhd-daily-planner/) | Daily planning for ADHD: task breakdown, time awareness, and emotional support |

---

## ⚖️ Legal and compliance

> Drafts, risk scoring, and compliance checklists.

| Skill | Summary |
|---------|------|
| [legal-contract-gen](legal-contract-gen/) | Interactive drafts of NDAs, service agreements, privacy policies, and cooperation frameworks |
| [legal-risk-analyzer](legal-risk-analyzer/) | Scores legal risk as severity times likelihood, with a rating and a recommended action |
| [compliance-review-planner](compliance-review-planner/) | Compliance checklists for GDPR, China's PIPL, advertising rules, and data-security laws |
| [tos-risk-checker](tos-risk-checker/) | Consumer-side terms review: one-sided clauses, data grants, auto-renewal, and similar risks |

---

## 🎨 Visual design and layout

> Design systems, journal layouts, and magazine-style documents.

| Skill | Summary |
|---------|------|
| [theme-kit](theme-kit/) | Ten preset themes (color and type) for slides, documents, and HTML pages |
| [ui-blueprint](ui-blueprint/) | Extracts a design system from a UI screenshot: color, type, components, spacing, and an MVP prompt |
| [sci-paper-cn](sci-paper-cn/) | Writing and layout guide for CVPR, NeurIPS, ACL, and similar venues, from section drafts to camera-ready |
| [astro-observation-report-cn](astro-observation-report-cn/) | Gravitational-wave observation papers in a Physical Review X two-column style |
| [photo-magazine-cn](photo-magazine-cn/) | Magazine-style reports: oversized type, full-bleed photography, data cards, and narrative layouts |
| [journalistic-portrait-cn](journalistic-portrait-cn/) | Chinese magazine HTML in the visual style of Southern People Weekly, for profile features |
| [geo-magazine-slides-cn](geo-magazine-slides-cn/) | Geographic-magazine PPTX for place roundups, travel destinations, and architecture portfolios |
| [retro-tech-illustration-cn](retro-tech-illustration-cn/) | Retro-tech visuals: synthwave, vaporwave, cyberpunk, and related looks |
| [fashion-sketch-cn](fashion-sketch-cn/) | Apparel tech packs: line overview, style specs, size chart, and bill of materials |

---

## 🔧 kimi-cli built-in tools

> Developer skills from [MoonshotAI/kimi-cli](https://github.com/MoonshotAI/kimi-cli), written for the Kimi Code CLI workflow.

| Skill | Summary |
|---------|------|
| [codex-worker](codex-worker/) | Starts and manages several Codex CLI agents in tmux so independent subtasks can run in parallel |
| [feature-smoke-test](feature-smoke-test/) | Plans and runs a repeatable end-to-end smoke test for a new or changed Kimi Code CLI feature |
| [gen-changelog](gen-changelog/) | Writes a changelog entry for a code change |
| [gen-docs](gen-docs/) | Updates the Kimi Code CLI user docs |
| [gen-rust](gen-rust/) | Ports a Python change to the Rust implementation, skipping UI and login code |
| [pull-request](pull-request/) | Opens a GitHub pull request |
| [release](release/) | Runs the Kimi Code CLI package release |
| [translate-docs](translate-docs/) | Translates and keeps bilingual docs in sync |
| [worktree-status](worktree-status/) | Audits git worktrees in the current project and flags ones that can be removed |

---

## Other

| Skill | Summary |
|---------|------|
| [kimi-skills-finder](kimi-skills-finder/) | Searches the catalog and recommends a skill for a stated task |

---

## Counts

| Source | Count |
|------|------|
| Kimi official library | 120 |
| kimi-cli built-in tools | 9 |
| **Total** | **129** |
