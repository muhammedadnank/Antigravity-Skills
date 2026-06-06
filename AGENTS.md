# AGENTS.md

## Project Overview

Antigravity Skills is a centralized library of reusable agent skills. It contains 2,275 active skill directories under `skills/`. Each skill is designed to guide AI coding assistants (e.g., Antigravity, Claude, Cursor, Aider) in executing specific domain tasks.

### Core Structure

- `/skills/`: The home of all individual skill directories.
  - Each skill directory must contain a `SKILL.md` file with a YAML frontmatter block containing `name` and `description`.
- `/scripts/`: Automated tools for synchronization and metadata indexing:
  - `sync_skills.sh`: Bash script that fetches upstream skill folders configured in `skills_sources.json`.
  - `update_skills_index.py`: Scans all `skills/` directories, parses `SKILL.md` frontmatter, and updates `skills_index.json`.
  - `generate_skills_list.py`: Generates the master listings in `SKILLS_LIST.md` and `skills/README.md`.
- `skills_sources.json`: Config file listing git repository sources, target directories, and include/exclude patterns.
- `skills_index.json`: JSON index listing all active skills with their description, path, and name.
- `SKILLS_LIST.md`: Main index of all skills sorted alphabetically.
- `skills/README.md`: Mirror index file under the `skills/` directory.

---

## Setup & Dependencies

The scripting utilities are written in Python 3 and require standard packages.
There are no complex external runtime dependencies. `jq` and `rsync` are required by the bash sync script.

To check requirements:
- Python 3
- Git
- `jq` (for JSON parsing in sync bash script)
- `rsync` (for directory mirroring)

---

## Development Workflow

### Adding a New Skill

To add a new skill manually:
1. Create a subfolder under `skills/` using lowercase and hyphens:
   `skills/my-new-skill/`
2. Create a `SKILL.md` inside the subfolder.
3. Add the mandatory YAML frontmatter to the top of `SKILL.md`:
   ```yaml
   ---
   name: my-new-skill
   description: Briefly explain what this skill does and when to use it.
   ---
   ```
4. Write the detailed markdown instructions/content for the skill below the frontmatter.

### Modifying Upstream Sources

To modify, add, or remove third-party skill sources:
1. Edit `skills_sources.json`.
2. Add a new configuration entry matching the schema:
   ```json
   {
     "repo": "https://github.com/owner/repository",
     "source_dir": "path/in/upstream/repo",
     "dest_dir": "skills/target-directory",
     "exclude": ["optional", "patterns", "to", "ignore"],
     "include": ["optional", "patterns", "to", "only", "include"]
   }
   ```
3. Run the synchronization script:
   ```bash
   ./scripts/sync_skills.sh
   ```

---

## Indexing & Code Generation

Whenever any skill's frontmatter or files are added, modified, or deleted, the index and lists must be regenerated.

1. **Rebuild the metadata index (`skills_index.json`)**:
   ```bash
   python3 scripts/update_skills_index.py
   ```
2. **Rebuild the public list markdown files (`SKILLS_LIST.md` and `skills/README.md`)**:
   ```bash
   python3 scripts/generate_skills_list.py
   ```

Always run both commands together to ensure consistency.

---

## Pull Request & Commit Guidelines

We enforce the conventional commits format.

- **Format**: `<type>(<optional scope>): <subject>`
  - Example: `feat(sync): add new upstream repository for database skills`
  - Example: `docs(readme): update repository setup instructions`
  - Example: `refactor(index): optimize frontmatter parsing regex`
- **Rules**:
  - Keep subject line under 50 characters.
  - Use imperative mood ("add", not "added").
  - Do not capitalize the first letter after the type prefix.
  - Do not end the subject line with a period.
