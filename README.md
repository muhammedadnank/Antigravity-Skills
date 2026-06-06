# Antigravity Skills

[简体中文](README.zh-CN.md) | [English](README.md)

Empower agents with professional capabilities in specific fields (such as full-stack development, complex logic planning, multimedia processing, etc.) through modular **Skills** definitions, allowing agents to solve complex problems systematically like human experts.

## 📂 Directory Structure

```
.
├── .claude-plugin/     # Claude plugin configuration files
├── skills/             # Antigravity Skills library
│   ├── skill-name/     # Individual skill directory
│   │   ├── SKILL.md    # Core skill definition and Prompt (Required)
│   │   ├── scripts/    # Scripts relied upon by the skill (Optional)
│   │   ├── examples/   # Skill usage examples (Optional)
│   │   └── resources/  # Templates and resources relied upon by the skill (Optional)
├── docs/               # User manual and documentation guides
├── scripts/            # Maintenance scripts
├── skills_sources.json # Skills synchronization source config
├── skills_index.json   # Skills metadata index
├── spec/               # Specification documents
├── template/           # New skill template
└── README.md
```

## 🔌 Compatibility

Antigravity Skills follow the universal **SKILL.md** format and can work seamlessly with any AI coding assistant that supports Agentic Skills:

| Tool Name (Agent) | Type | Compatibility | Project Path | Global Path |
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
> Most tools will automatically discover skills in `.agent/skills/`. For maximum compatibility, please clone/copy into this directory.

## 📖 Quick Start

### 1. Prepare the Skills Library
First, clone this repository locally (it is recommended to place it in a fixed location for global reference):
```bash
git clone https://github.com/muhammedadnank/Antigravity-Skills.git ~/antigravity-skills
```

### 2. Install Skills (Symlink Method)
We strongly recommend using **Symbolic Links (Symlink)** for installation, so that when you update this repository via `git pull`, all tools will automatically sync the latest features.

#### 🔹 Method A: Project Level Installation
Enable skills only for the current project. Run in your project root:
```bash
mkdir -p .agent/skills
ln -s ~/antigravity-skills/skills/* .agent/skills/
```

#### 🔹 Method B: Global Level Installation
Enable skills by default in all projects. Run the corresponding command based on the tool; common examples:

| Tool Name | Global Installation Command (macOS/Linux) |
| :--- | :--- |
| **General** | `mkdir -p ~/.agent/skills && ln -s ~/antigravity-skills/skills/* ~/.agent/skills/` |
| **Claude Code** | `mkdir -p ~/.claude/skills && ln -s ~/antigravity-skills/skills/* ~/.claude/skills/` |
| **Antigravity** | `mkdir -p ~/.gemini/antigravity/skills && ln -s ~/antigravity-skills/skills/* ~/.gemini/antigravity/skills/` |
| **Gemini** | `mkdir -p ~/.gemini/skills && ln -s ~/antigravity-skills/skills/* ~/.gemini/skills/` |
| **Codex** | `mkdir -p ~/.codex/skills && ln -s ~/antigravity-skills/skills/* ~/.codex/skills/` |

#### 🔹 Method C: Claude Plugin Installation (Claude Code Only)
If you primarily use **Claude Code**, you can install with one click via the plugin marketplace (this method automatically handles skill loading):

```bash
# 1. Start Claude Code
# 2. Add the plugin marketplace
/plugin marketplace add muhammedadnank/Antigravity-Skills

# 3. Install the plugin from the marketplace
/plugin install antigravity-skills@antigravity-skills
```

### 3. Using Skills
Enter `@[skill-name]` or `/skill-name` in the chat box to invoke them, for example:
```text
/canvas-design Help me design a 16:9 blog cover about "Deep Learning"
```

### 4. More Information
- **View Manual**: For detailed usage, please refer to [docs/Antigravity_Skills_Manual.en.md](docs/Antigravity_Skills_Manual.en.md).
- **Environment Dependencies**: Some skills rely on Python environments; please ensure your system has necessary libraries installed (e.g., `pdf2docx`, `pandas`, etc.).


## 🔄 Keeping in Sync

Many skills in this project originate from excellent open-source communities. To keep in sync with upstream repositories, you can update them in the following ways:

1.  **Configuration**: The `skills_sources.json` file in the root directory is pre-configured with the upstream repositories for major skills and usually does not need manual adjustment.
2.  **Run Sync**:
    You can choose to sync all skills or just a specific one:

    ```bash
    # Sync all configured sources
    ./scripts/sync_skills.sh

    # Sync only a specific source (e.g., anthropics-skills)
    ./scripts/sync_skills.sh anthropics-skills
    ```
    The script will automatically pull the latest code and update the corresponding skill directories.

    > **Note**: The `ui-ux-pro-max` skill has a special directory structure and does not support automatic synchronization via script for now. Please use its official installation command `uipro init --ai antigravity` to install or update.

## 🚀 Integrated Skills (Total: 2275)

This library includes a vast collection of **2,275** active agent skills spanning across software engineering, system administration, security auditing, design, content creation, and more. 

To keep the repository clean and easily navigable, the full alphabetical index of all integrated skills is maintained in a dedicated registry file:

👉 **[View the Complete Skills List (SKILLS_LIST.md)](SKILLS_LIST.md)** 👈

The index is automatically updated daily. If you add or modify skills locally, you can rebuild the index using:
```bash
python3 scripts/update_skills_index.py
python3 scripts/generate_skills_list.py
```


## 🌟 Credits & Sources

This project integrates core ideas or skill implementations from the following excellent open-source projects. Respect to the original authors:

- **[Anthropic Skills](https://github.com/anthropics/skills)**: Official API usage paradigms and skill definition references provided by Anthropic.
- **[UI/UX Pro Max Skills](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)**: Top-tier UI/UX design intelligence, providing full design schemes for colors, layouts, etc.
- **[Superpowers](https://github.com/obra/superpowers)**: A toolkit and workflow inspiration aimed at giving LLMs "superpowers."
- **[Planning with Files](https://github.com/OthmanAdi/planning-with-files)**: Implements a Manus-style file-based task planning system to enhance persistent memory for complex tasks.
- **[NotebookLM](https://github.com/PleasePrompto/notebooklm-skill)**: Knowledge retrieval and Q&A skill implementation based on Google NotebookLM.
- **[Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)**: In-depth Context Engineering skills covering compression, optimization, and degradation handling.
- **[Obsidian Skills](https://github.com/kepano/obsidian-skills)**: Professional Obsidian integration skills, including JSON Canvas and enhanced Markdown support.
- **[Remotion Skills](https://github.com/remotion-dev/skills)**: Official Remotion skills for AI agents to create videos programmatically.
- **[Vercel Agent Skills](https://github.com/vercel-labs/agent-skills)**: Official Vercel skills for React best practices, composition patterns, and web design guidelines.
- **[Supabase Agent Skills](https://github.com/supabase/agent-skills)**: Official Supabase skills for Postgres performance optimization and best practices.
- **[Baoyu Skills](https://github.com/JimLiu/baoyu-skills)**: A collection of skills for content generation, publishing, and daily efficiency, including XHS image generator, infographic generator, and content converters.

## 🛡️ Security Policy

We take security seriously. Please refer to our [Security Policy](SECURITY.md) for information on supported versions and how to report vulnerabilities safely.

## 🤝 How to Contribute

We welcome contributions! Please refer to our **[CONTRIBUTING.md](CONTRIBUTING.md)** for detailed guidelines on how to add new skills, improve documentation, and report issues.

## 📄 License

This project is open-sourced under the [MIT License](LICENSE).
