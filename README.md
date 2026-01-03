# MkDocs Redact

A simple MkDocs plugin that redacts marked sections in Markdown files during production builds while keeping them visible during development.

This plugin uses the markdown comment syntax instead of \`\`\` to preserve normal markdown highlighting and editing conditions. 

## Use Case

Hide sensitive or work-in-progress content from production builds while still being able to see and edit it during local development with `mkdocs serve`.

## Installation

```yaml
# mkdocs.yml
plugins:
  - redact
```

No configuration options required.

## Usage

Wrap content you want to redact with HTML comments:

```markdown
# My Documentation

This content is always visible.

<!-- REDACT -->
This section contains sensitive information that will be
replaced with **REDACTED** in production builds.

- Secret API keys
- Internal notes
- Draft content
<!-- REDACTEND -->

This content is also always visible.
```

### Syntax

| Marker | Description |
|--------|-------------|
| `<!-- REDACT -->` | Start of redacted section |
| `<!-- REDACTEND -->` | End of redacted section |

Whitespace around the keywords is flexible: `<!--REDACT-->` and `<!-- REDACT -->` both work.

---

## How It Works

### Processing Flow

```
┌─────────────────────────────────┐
│  on_pre_build()                 │
│  Check if running 'mkdocs build'│
│  └─► Set self.is_build flag     │
└─────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  on_page_markdown()             │
│  ┌───────────────────────────┐  │
│  │ If is_build = True:       │  │
│  │ Replace REDACT blocks     │  │
│  │ with **REDACTED**         │  │
│  └───────────────────────────┘  │
│  ┌───────────────────────────┐  │
│  │ If is_build = False:      │  │
│  │ Return markdown unchanged │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

### Build vs Serve Behavior

| Command | Redaction Applied |
|---------|-------------------|
| `mkdocs build` | Yes - content replaced with `**REDACTED**` |
| `mkdocs serve` | No - content visible for editing |
| `mkdocs gh-deploy` | Yes - uses build internally |

---

## Examples

### Input (Markdown)

```markdown
## API Configuration

The API endpoint is `https://api.example.com/v1`.

<!-- REDACT -->
**Internal Notes:**
- Production API key: `sk-prod-xxxxx`
- Staging API key: `sk-stage-xxxxx`
- Contact: admin@internal.example.com
<!-- REDACTEND -->

See the [API documentation](https://docs.example.com) for more details.
```

### Output (`mkdocs serve`)

Content appears unchanged - you can see and edit the internal notes.

### Output (`mkdocs build`)

```markdown
## API Configuration

The API endpoint is `https://api.example.com/v1`.

**REDACTED**

See the [API documentation](https://docs.example.com) for more details.
```

---

## Multiple Redactions

You can have multiple redacted sections per page:

```markdown
## Section 1

<!-- REDACT -->
Secret content 1
<!-- REDACTEND -->

## Section 2

<!-- REDACT -->
Secret content 2
<!-- REDACTEND -->
```

Each section is independently replaced with `**REDACTED**`.

---

## Console Output

During build, the plugin reports its status:

```
✅ Redaction will be applied for this build.
```

During serve:

```
ℹ️ Redaction skipped: 'build' command not detected (e.g., 'serve').
```

---

## License

MIT
