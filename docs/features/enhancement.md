# Content Enhancement

Automatically improve existing documentation with AI-powered enhancements.

## Features

### Grammar & Spelling

Fix grammar errors and spelling mistakes while preserving technical terms:

```bash
mkdocs-ai enhance docs/guide.md --grammar
```

### Clarity Improvements

Improve readability and structure:

```bash
mkdocs-ai enhance docs/guide.md --clarity
```

### Consistency Checking

Ensure consistent terminology across documentation:

```bash
mkdocs-ai enhance docs/ --consistency
```

## Usage

### Preview Changes

See what will be changed before applying:

```bash
mkdocs-ai enhance docs/guide.md --preview
```

### Apply Changes

Apply enhancements to files:

```bash
mkdocs-ai enhance docs/guide.md --apply
```

### Interactive Mode

Review and approve each change:

```bash
mkdocs-ai enhance docs/guide.md --interactive
```

## Configuration

```yaml
plugins:
  - mkdocs-ai:
      enhancement:
        enabled: true
        auto_enhance: false  # Don't auto-enhance on build
        features:
          - grammar
          - clarity
          - consistency
        preserve_code: true
        preserve_frontmatter: true
```

## Content Preservation

The enhancement system automatically preserves:

- Code blocks (fenced and indented)
- Frontmatter (YAML, TOML)
- HTML tags and comments
- Tables
- Math expressions
- Links and images

## Best Practices

1. **Always preview first**: Use `--preview` to see changes
2. **Use version control**: Commit before enhancing
3. **Review changes**: Use `--interactive` for important docs
4. **Enable selectively**: Choose specific features you need

## Examples

### Enhance a Single File

```bash
mkdocs-ai enhance docs/api.md --grammar --clarity --apply
```

### Enhance a Directory

```bash
mkdocs-ai enhance docs/ --grammar --preview
```

### Interactive Review

```bash
mkdocs-ai enhance docs/guide.md --all --interactive
```

## Next Steps

- [Semantic Search](search.md) - Add AI-powered search
- [Asset Processing](assets.md) - Generate docs from code
