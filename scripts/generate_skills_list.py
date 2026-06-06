#!/usr/bin/env python3
"""
Generate SKILLS_LIST.md in the root and skills/README.md in the skills directory.
These files index all the available skills alphabetically.
"""
import json
import os
import string

def main():
    # Setup paths relative to repository root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)

    index_path = "skills_index.json"
    root_output_path = "SKILLS_LIST.md"
    skills_readme_path = "skills/README.md"

    if not os.path.exists(index_path):
        print(f"Error: {index_path} not found!")
        return

    with open(index_path, "r", encoding="utf-8") as f:
        skills = json.load(f)

    # Sort skills alphabetically by name/id
    skills.sort(key=lambda x: x["name"].lower())

    # Group by first letter
    grouped_skills = {}
    for skill in skills:
        first_char = skill["name"][0].upper()
        if first_char not in string.ascii_uppercase:
            first_char = "#"
        if first_char not in grouped_skills:
            grouped_skills[first_char] = []
        grouped_skills[first_char].append(skill)

    # Generate Index/Anchor Links
    index_links = []
    for char in sorted(grouped_skills.keys()):
        anchor = char.lower() if char != "#" else "num"
        index_links.append(f"[{char}](#{anchor})")
    index_section = "## Index\n\n" + " | ".join(index_links) + "\n\n"

    # --- 1. Generate SKILLS_LIST.md (Root level, links point to skills/...) ---
    root_md = []
    root_md.append("# Antigravity Integrated Skills List\n")
    root_md.append(f"This is the complete list of all **{len(skills)}** active skills integrated into the Antigravity Skills library.\n")
    root_md.append(index_section)

    for char in sorted(grouped_skills.keys()):
        anchor = char.lower() if char != "#" else "num"
        root_md.append(f'<a name="{anchor}"></a>')
        root_md.append(f"## {char}\n")
        for skill in grouped_skills[char]:
            desc = skill.get("description", "").strip()
            if not desc:
                desc = "No description provided."
            # Relative link from root
            link_path = f"skills/{skill['name']}/SKILL.md"
            root_md.append(f"- **[`@[{skill['name']}]`]({link_path})**: {desc}")
        root_md.append("\n")

    with open(root_output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(root_md))
    print(f"Successfully generated {root_output_path} with {len(skills)} skills.")

    # --- 2. Generate skills/README.md (Inside skills/ folder, links are direct relative) ---
    skills_md = []
    skills_md.append("# Antigravity Skills Library Folder\n")
    skills_md.append(f"This folder contains the raw definitions for all **{len(skills)}** active agent skills.\n")
    skills_md.append("To enable these skills in your project, check out the installation instructions in the [main README](../README.md).\n")
    skills_md.append(index_section)

    for char in sorted(grouped_skills.keys()):
        anchor = char.lower() if char != "#" else "num"
        skills_md.append(f'<a name="{anchor}"></a>')
        skills_md.append(f"## {char}\n")
        for skill in grouped_skills[char]:
            desc = skill.get("description", "").strip()
            if not desc:
                desc = "No description provided."
            # Relative link from skills directory
            link_path = f"{skill['name']}/SKILL.md"
            skills_md.append(f"- **[`@[{skill['name']}]`]({link_path})**: {desc}")
        skills_md.append("\n")

    with open(skills_readme_path, "w", encoding="utf-8") as f:
        f.write("\n".join(skills_md))
    print(f"Successfully generated {skills_readme_path} with {len(skills)} skills.")

if __name__ == "__main__":
    main()
