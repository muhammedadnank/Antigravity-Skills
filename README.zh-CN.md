# Antigravity Skills

[简体中文](README.zh-CN.md) | [English](README.md)

通过模块化的 **Skills** 定义，赋予 Agent 在特定领域的专业能力（如全栈开发、复杂逻辑规划、多媒体处理等），让 Agent 能够像人类专家一样系统性地解决复杂问题。

## 📂 目录结构 (Directory Structure)

```
.
├── .claude-plugin/     # Claude 插件配置文件 (plugin.json)
├── skills/             # Antigravity Skills 技能库
│   ├── skill-name/     # 独立技能目录
│   │   ├── SKILL.md    # 技能核心定义与Prompt（必须）
│   │   ├── scripts/    # 技能依赖的脚本（可选）
│   │   ├── examples/   # 技能使用示例（可选）
│   │   └── resources/  # 技能依赖的模板与资源（可选）
├── docs/               # 用户手册与文档指南
├── scripts/            # 项目维护脚本
├── skills_sources.json # 技能同步源配置文件
├── skills_index.json   # 技能元数据索引
├── spec/               # 规范文档
├── template/           # 新技能模板
└── README.md
```

## 🔌 兼容性 (Compatibility)

Antigravity Skills 遵循通用的 **SKILL.md** 格式，可与任何支持 Agentic Skills 的 AI 编码助手协同工作：

| 工具名称 (Agent) | 类型 | 兼容性 | 项目路径 (Project Path) | 全局路径 (Global Path) |
| :--- | :--- | :--- | :--- | :--- |
| **Antigravity** | IDE | ✅ Full | `.agent/skills/` | `~/.gemini/antigravity/skills/` |
| **Claude Code** | CLI | ✅ Full | `.claude/skills/` | `~/.claude/skills/` |
| **Gemini CLI** | CLI | ✅ Full | `.gemini/skills/` | `~/.gemini/skills/` |
| **Codex** | CLI | ✅ Full | `.codex/skills/` | `~/.codex/skills/` |
| **Cursor** | IDE | ✅ Full | `.cursor/skills/` | `~/.cursor/skills/` |
| **GitHub Copilot** | Extension| ⚠️ Partial | `.github/skills/` | `~/.copilot/skills/` |
| **OpenCode** | CLI | ✅ Full | `.opencode/skills/` | `~/.config/opencode/skills/` |
| **Windsurf** | IDE | ✅ Full | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |
| **Trae** | IDE | ✅ Full | `.trae/skills/` | `~/.trae/skills/` |

> [!TIP]
> 大多数工具都会自动发现 `.agent/skills/` 中的技能。为了获得最大兼容性，请克隆/复制到此目录。

## 📖 快速开始 (Quick Start)

### 1. 准备技能库
首先将本仓库克隆到本地（建议放在一个固定位置以便全局引用）：
```bash
git clone https://github.com/muhammedadnank/Antigravity-Skills.git ~/antigravity-skills
```

### 2. 安装技能 (Symlink 方式)
我们强烈建议使用 **符号链接 (Symlink)** 进行安装，这样当你通过 `git pull` 更新本仓库时，所有工具都能自动同步最新功能。

#### 🔹 方案 A：项目级安装 (Project Level)
仅在当前项目启用技能。在你的项目根目录下运行：
```bash
mkdir -p .agent/skills
ln -s ~/antigravity-skills/skills/* .agent/skills/
```

#### 🔹 方案 B：全局安装 (Global Level)
在所有项目中默认启用技能。根据不同工具运行对应命令，给出部分示例：

| 工具名称 | 全局安装命令 (macOS/Linux) |
| :--- | :--- |
| **通用** | `mkdir -p ~/.agent/skills && ln -s ~/antigravity-skills/skills/* ~/.agent/skills/` |
| **Claude Code** | `mkdir -p ~/.claude/skills && ln -s ~/antigravity-skills/skills/* ~/.claude/skills/` |
| **Antigravity** | `mkdir -p ~/.gemini/antigravity/skills && ln -s ~/antigravity-skills/skills/* ~/.gemini/antigravity/skills/` |
| **Gemini** | `mkdir -p ~/.gemini/skills && ln -s ~/antigravity-skills/skills/* ~/.gemini/skills/` |
| **Codex** | `mkdir -p ~/.codex/skills && ln -s ~/antigravity-skills/skills/* ~/.codex/skills/` |

#### 🔹 方案 C：Claude Plugin 安装 (Claude Code 专用)
如果你主要使用 **Claude Code**，可以通过插件市场一键安装（该方式会自动处理技能加载）：

```bash
# 1. 启动 Claude Code
# 2. 添加插件市场
/plugin marketplace add muhammedadnank/Antigravity-Skills

# 3. 从市场安装插件
/plugin install antigravity-skills@antigravity-skills
```

### 3. 使用技能
在对话框中输入 `@[skill-name]` 或 `/skill-name` 即可调用，例如：
```text
/canvas-design 帮我设计一张关于“Deep Learning”的博客封面，尺寸 16:9
```

### 4. 更多信息
- **查看手册**: 详细用法请查阅 [docs/Antigravity_Skills_Manual.zh-CN.md](docs/Antigravity_Skills_Manual.zh-CN.md)。
- **环境依赖**: 部分技能依赖 Python 环境，请确保系统已安装必要的库（如 `pdf2docx`, `pandas` 等）。


## 🔄 保持同步 (Keeping in Sync)

本项目中的许多技能源自优秀的开源社区。为了保持与上游仓库的同步，可以通过以下方式更新：

1.  **配置源**: 根目录下的 `skills_sources.json` 文件已预置了主要 Skill 的上游仓库配置，通常无需手动修改。
2.  **运行同步**:
    你可以选择同步所有 Skill，或者仅同步指定的某一个：
    
    ```bash
    # 同步所有配置的源
    ./scripts/sync_skills.sh

    # 仅同步指定源 (例如: anthropics-skills)
    ./scripts/sync_skills.sh anthropics-skills
    ```
    该脚本会自动拉取最新代码并更新对应的技能目录。

    > **注意**: `ui-ux-pro-max` 技能由于目录结构较为特殊，暂不支持通过脚本自动同步，请使用其官方安装命令 `uipro init --ai antigravity` 进行安装或更新。



## 🚀 已集成的 Skills (共 2275 个)

本库包含 **2,275** 个活跃的 AI Agent 技能，涵盖软件开发、系统管理、安全审计、设计、内容创作等多个领域。

为了保持仓库整洁且易于浏览，所有已集成技能的完整拼音/字母排序索引保存在一个专属的列表文件中：

👉 **[查看完整技能列表 (SKILLS_LIST.md)](SKILLS_LIST.md)** 👈

索引每天通过 GitHub Actions 自动更新。如果您在本地添加或修改了技能，可以使用以下命令手动重新构建索引：
```bash
python3 scripts/update_skills_index.py
python3 scripts/generate_skills_list.py
```

## 🌟 致谢与来源 (Credits & Sources)

本项目集成了以下优秀开源项目的核心思想或 Skill 实现，向原作者致敬：

- **[Anthropic Skills](https://github.com/anthropics/skills)**: Anthropic 官方提供的 API 使用范式与技能定义参考。
- **[UI/UX Pro Max Skills](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)**: 顶级的 UI/UX 设计智能，提供配色、布局等全套设计方案参考。
- **[Superpowers](https://github.com/obra/superpowers)**: 旨在赋予 LLM "超能力" 的工具集与工作流启发。
- **[Planning with Files](https://github.com/OthmanAdi/planning-with-files)**: 实现类似 Manus 的文件式任务规划系统，提升复杂任务的持久化记忆。
- **[NotebookLM](https://github.com/PleasePrompto/notebooklm-skill)**: 基于 Google NotebookLM 的知识检索与问答技能实现。
- **[Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)**: 深入的上下文工程（Context Engineering）技能，涵盖压缩、优化与降级处理。
- **[Obsidian Skills](https://github.com/kepano/obsidian-skills)**: 专业的 Obsidian 集成技能，包含 JSON Canvas 与增强型 Markdown 支持。
- **[Remotion Skills](https://github.com/remotion-dev/skills)**: Remotion 官方提供的 AI Agent 技能，用于通过代码创建视频。
- **[Vercel Agent Skills](https://github.com/vercel-labs/agent-skills)**: Vercel 提供的官方技能，涵盖 React 最佳实践、组合模式和 Web 设计指南。
- **[Supabase Agent Skills](https://github.com/supabase/agent-skills)**: Supabase 提供的官方技能，专注于 Postgres 性能优化和最佳实践。
- **[Baoyu Skills](https://github.com/JimLiu/baoyu-skills)**: 专注于内容生成、发布和日常效率的技能集合，包括小红书图片生成器、信息图表生成器和内容转换工具等。

## 🛡️ 安全策略 (Security Policy)

我们要非常重视安全性。请参阅我们的 [安全策略](SECURITY.md) 文档，了解受支持的版本以及如何安全地报告漏洞。

## 🤝 如何贡献 (How to Contribute)

我们欢迎任何形式的贡献！请参考 **[CONTRIBUTING.md](CONTRIBUTING.md)** 查看关于如何添加新技能、改进文档和报告问题的详细指南。

## 📄 开源协议 (License)

本项目采用 [MIT License](LICENSE) 协议开源。