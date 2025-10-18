# Release Checklist - v0.5.0 Beta

**Target Date**: TBD  
**Release Type**: Beta  
**Version**: 0.5.0-beta

---

## Pre-Release Checklist

### Code Quality
- [x] All tests passing locally
- [x] No critical bugs
- [x] Code formatted (Black)
- [x] Linting passed (Ruff)
- [x] Type checking configured (mypy)
- [ ] Run full test suite one more time
  ```bash
  pytest tests/ -v --cov=mkdocs_ai --cov-report=html
  ```

### Documentation
- [x] README updated
- [x] CHANGELOG created/updated
- [x] Version numbers updated
- [x] Known issues documented
- [x] Beta testing guide created
- [x] API documentation complete
- [ ] Verify all links work
- [ ] Spell check all docs

### Version Updates
- [x] `mkdocs_ai/__init__.py` → 0.5.0
- [x] `pyproject.toml` → 0.5.0
- [ ] Create CHANGELOG.md with v0.5.0 entry
- [ ] Update any hardcoded version strings

### Testing
- [x] Unit tests pass
- [x] Integration tests pass
- [ ] Manual smoke test
  - [ ] Install from source
  - [ ] Run basic generation
  - [ ] Test with real API key
  - [ ] Build documentation site
- [ ] Test in clean environment
  ```bash
  python -m venv test-env
  source test-env/bin/activate
  pip install -e .
  mkdocs-ai --version
  ```

### Infrastructure
- [x] CI/CD pipeline working
- [x] GitHub Actions passing
- [x] Docker build successful
- [ ] Test Docker image
  ```bash
  docker build -t mkdocs-ultra-material:test .
  docker run mkdocs-ultra-material:test mkdocs-ai --version
  ```

---

## Release Process

### 1. Create Release Branch
```bash
git checkout -b release/v0.5.0-beta
git push origin release/v0.5.0-beta
```

### 2. Final Commits
- [ ] Update CHANGELOG.md
- [ ] Update version numbers (if any missed)
- [ ] Commit changes
  ```bash
  git add .
  git commit -m "chore: prepare v0.5.0-beta release"
  git push origin release/v0.5.0-beta
  ```

### 3. Create Tag
```bash
git tag -a v0.5.0-beta -m "Release v0.5.0 Beta"
git push origin v0.5.0-beta
```

### 4. Build Package
```bash
python -m build
```

### 5. Test Package Installation
```bash
pip install dist/mkdocs_ultra_material-0.5.0-py3-none-any.whl
mkdocs-ai --version
```

### 6. Create GitHub Release
- [ ] Go to GitHub Releases
- [ ] Click "Draft a new release"
- [ ] Select tag: v0.5.0-beta
- [ ] Title: "v0.5.0 Beta - Ready for Testing"
- [ ] Description: Use template below
- [ ] Mark as pre-release: ✅
- [ ] Attach built packages
- [ ] Publish release

**Release Description Template**:
```markdown
# MkDocs Ultra Material v0.5.0 Beta

🎉 First beta release! Ready for community testing.

## What's New

- ✅ Complete document generation system
- ✅ AI-powered content enhancement
- ✅ Semantic search with embeddings
- ✅ Asset processing (code, Docker Compose)
- ✅ Obelisk integration for RAG chatbots
- ✅ 52 tests, comprehensive documentation
- ✅ CI/CD pipeline, Docker support

## Installation

```bash
pip install mkdocs-ultra-material
```

Or from source:
```bash
git clone https://github.com/genpozi/mkdocs-ultra-material.git
cd mkdocs-ultra-material
pip install -e .
```

## Beta Testing

See [Beta Testing Guide](BETA_TESTING_GUIDE.md) for testing scenarios.

## Known Issues

See [Known Issues](KNOWN_ISSUES.md) for current limitations.

## Documentation

- [Quick Start](QUICK_START.md)
- [Usage Guide](USAGE_GUIDE.md)
- [Examples](PRACTICAL_EXAMPLES.md)

## Feedback

Please report issues at: https://github.com/genpozi/mkdocs-ultra-material/issues

Thank you for testing! 🙏
```

---

## Post-Release Checklist

### Documentation Deployment
- [ ] Verify GitHub Pages deployment
- [ ] Check documentation site loads
- [ ] Test all navigation links
- [ ] Verify search works

### Announcements
- [ ] Post on GitHub Discussions
- [ ] Tweet announcement (if applicable)
- [ ] Post on Reddit r/Python (if applicable)
- [ ] Post on relevant Discord servers
- [ ] Update project website (if exists)

### Monitoring
- [ ] Watch GitHub issues
- [ ] Monitor discussions
- [ ] Track download stats
- [ ] Collect feedback

### Communication
- [ ] Respond to issues within 24 hours
- [ ] Thank beta testers
- [ ] Update roadmap based on feedback
- [ ] Plan v0.6.0 features

---

## Rollback Plan

If critical issues found:

1. **Mark release as broken**
   - Add warning to release notes
   - Pin issue to repository

2. **Create hotfix**
   ```bash
   git checkout -b hotfix/v0.5.1-beta
   # Fix critical issue
   git commit -m "fix: critical issue"
   git tag v0.5.1-beta
   git push origin v0.5.1-beta
   ```

3. **Release hotfix**
   - Follow release process
   - Mark as hotfix in release notes

---

## Success Metrics

Track for 2 weeks:

- [ ] GitHub stars: Target 10+
- [ ] Issues opened: Track count
- [ ] Critical bugs: Target 0
- [ ] Beta testers: Target 10+
- [ ] Positive feedback: Target >80%

---

## Next Steps After Beta

### Week 1
- Monitor issues and feedback
- Fix critical bugs
- Update documentation based on questions

### Week 2
- Analyze feedback
- Plan v0.6.0 features
- Update roadmap

### Week 3-4
- Implement high-priority features
- Increase test coverage
- Performance optimization

### Week 5-6
- Prepare v0.6.0 release
- More beta testing
- Documentation updates

---

## Notes

- This is a beta release - expect rough edges
- Breaking changes possible before v1.0.0
- Community feedback is crucial
- Be responsive to issues

---

## Sign-off

**Prepared By**: _______________  
**Date**: _______________  
**Approved By**: _______________  
**Date**: _______________

---

**Ready to ship! 🚀**
