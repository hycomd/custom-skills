# custom-skills

Personal Codex/Claude-style skills customized from public projects.

Current skills:

| Skill | Purpose | Upstream |
|---|---|---|
| `beautiful-svg-whiteboard` | Create polished, editable standalone SVG whiteboards from a curated set of 10 retained visual styles. | [`zarazhangrui/beautiful-feishu-whiteboard`](https://github.com/zarazhangrui/beautiful-feishu-whiteboard) |
| `html-standalone` | Convert Markdown, JSON, plain text, pasted content, or URLs into a single offline HTML file with images embedded as base64 data URIs. | [`iharnoor/html-everything`](https://github.com/iharnoor/html-everything) |

See [`docs/skill-sources.md`](docs/skill-sources.md) for source, attribution,
and local customization notes.

## Layout

```text
.
|-- beautiful-svg-whiteboard/
|   |-- SKILL.md
|   |-- CATALOG.md
|   |-- RULES.md
|   `-- templates/
|-- html-standalone/
|   |-- SKILL.md
|   `-- scripts/
|       `-- embed-images.py
|-- docs/
|   `-- skill-sources.md
|-- LICENSE
|-- THIRD_PARTY_NOTICES.md
`-- README.md
```

## License

This repository is MIT licensed. Some content is derived from third-party
MIT-licensed projects; see [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
