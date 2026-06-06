# Security Policy

## Supported Versions

We currently support security updates for the following versions:

| Version | Supported          | Notes        |
| ------- | ------------------ | ------------ |
| 2.x     | :white_check_mark: | Current Main Version |
| 1.x     | :x:                | End of Life  |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please **DO NOT** report it via public Issues. Please follow these steps:

1.  **Private Reporting**: Please send an email to the project maintainer (if applicable) or use GitHub's [Security Advisories](https://github.com/guanyang/antigravity-skills/security/advisories/new) feature (if enabled).
2.  **Details**: Please include as many details as possible in your report, such as reproduction steps, affected versions, and potential impact.
3.  **Response Time**: We will make every effort to acknowledge your report within 48 hours and provide a fix as soon as possible.

## Agentic Skills Security Best Practices

This project contains various AI Agent skills and workflows. Since these skills empower AI to execute code, manipulate files, and make network requests, please adhere to the following safety guidelines:

### 1. Code Audit
Before using any skill involving `run_command` (command execution) or `write_to_file` (file writing), be sure to review its `SKILL.md` definition and relevant scripts. Understand what operations the AI is about to perform on your system.

### 2. Sandbox Environment
It is recommended to run Agents in an isolated environment (such as a Docker container, virtual machine, or a dedicated development environment) to prevent accidental system modifications or data loss.

### 3. Sensitive Information Protection
*   **Do Not** hardcode API keys, passwords, or private keys directly into prompts or skill files.
*   Use environment variables or dedicated secret management tools to handle sensitive credentials.
*   When using `search_web` or other network tools, be careful not to leak sensitive data from your context.

### 4. Principle of Least Privilege
Try to run Agents as a non-root/admin user to limit their access permissions to critical system directories.

## Disclaimer

The skills and tools provided in this project are primarily for assisting development. Users must assume the risks associated with running AI-generated code or executing automated scripts.
