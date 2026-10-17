# bot-skills

Shared skills and helper scripts for Grok Bot agents.

A skill is a short `SKILL.md` that tells an agent when and how to do a specific job. Some skills come with a helper script that the skill calls. Each skill lives in its own folder under `skills/`.

## Skills

| Skill | What it does |
| --- | --- |
| [`screen-ledger`](skills/screen-ledger/) | Records which agent holds which desktop screen on a shared computer, and shows what is running on every screen. |

## Install a skill

1. Open the skill's folder under `skills/`.
2. In the Grok Bot app, create a new skill with the skill editor and paste in the contents of the folder's `SKILL.md`. Keep its `name` and `description` frontmatter.
3. If the folder contains scripts, copy them to the path the `SKILL.md` names. For `screen-ledger`, that is `/home/box/tools/screen-ledger.py`.

## License

[MIT](LICENSE)
