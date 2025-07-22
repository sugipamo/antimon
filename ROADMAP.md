# antimon Development Roadmap

## Current Status (2025-07-22)

### ⚠️ Critical Issues - MUST FIX IMMEDIATELY

1. **Exit Codes Are Broken** 🚨
   - Security detections return exit code 0 (should be 2)
   - This breaks CI/CD integration completely
   - File: Likely in `src/antimon/core.py` or main entry point

2. **Missing Documentation**
   - `docs/faq.md` referenced but doesn't exist
   - Error messages link to non-existent documentation

### Recent Achievements (v0.2.10):
- ✅ Verified `--quickstart` is working correctly
- ✅ Confirmed `--stats` functionality is implemented
- ✅ `--config` option shows appropriate v0.3.0 message

### Quality Check Summary:
- ✅ **pytest**: 119/119 tests passing (75% code coverage)
- ✅ **ruff**: All style issues fixed (18 SIM117 warnings acceptable)
- ⚠️ **mypy**: 81 type errors remaining (future version)
- ⚠️ **src-check**: Score 53.0/100 (needs improvement)

## Project Vision

Transform antimon from a standalone script into a robust, extensible Python package that can be easily integrated into various AI coding assistant workflows and CI/CD pipelines.

## Completed Features (v0.2.1 - v0.2.8)
- ✅ Detector fixes for Edit/MultiEdit tool support
- ✅ Direct file/content checking without JSON (`--check-file`, `--check-content`)
- ✅ Claude Code integration setup (`--setup-claude-code`)
- ✅ Status, dry-run, and error explanation commands
- ✅ Non-interactive demo mode
- ✅ Structured logging foundation
- ✅ Enhanced error messages with context




### Version 0.2.11 (Critical Fixes) - URGENT

#### Must Fix Before Any New Features:
- [ ] Fix exit codes (currently ALWAYS returns 0)
  - Must return: 0=success, 1=error, 2=security issue detected
- [ ] Create docs/faq.md file (referenced but missing)

### Version 0.2.12 (User Experience) - NEXT RELEASE

#### High Priority Features (Based on User Testing):
- [ ] Batch file checking with glob patterns (`antimon --check-files "*.py"`)
- [ ] JSON output format (`--output-format json`)
- [ ] Success message improvements (show what was checked)
- [ ] Quiet mode fixes (truly silent except errors)
- [ ] Progress indicators for multiple operations

#### Documentation:
- [ ] Windows-specific Claude Code setup instructions
- [ ] CI/CD integration examples
- [ ] Common false positive scenarios and solutions

## Version 0.3.0 (Configuration Support)
- [ ] TOML configuration file support (`antimon.toml`)
- [ ] Custom pattern definitions
- [ ] Enable/disable specific detectors
- [ ] Severity levels for detections
- [ ] Whitelist/ignore patterns
- [ ] Global configuration (`~/.config/antimon/antimon.toml`)
- [ ] Environment variable overrides
- [ ] Configuration file validation and schema

## Version 0.4.0 (Enhanced Detection)
- [ ] Additional security patterns:
  - [ ] SQL injection detection
  - [ ] Command injection detection
  - [ ] Path traversal detection
  - [ ] XXE (XML External Entity) detection
  - [ ] SSRF (Server-Side Request Forgery) patterns
- [ ] Language-specific detections:
  - [ ] Python: `eval()`, `exec()`, `__import__`
  - [ ] JavaScript: `eval()`, `Function()`, `innerHTML`
  - [ ] Shell: Command injection patterns
- [ ] Framework-specific patterns

## Version 0.5.0 (Integration Features)
- [ ] Plugin system for custom detectors
- [ ] Pre-commit hook support
- [ ] GitHub Actions integration
- [ ] GitLab CI integration
- [ ] VS Code extension API
- [ ] Reporting formats (SARIF, JUnit XML, HTML, Markdown)

## Version 0.6.0 - 0.9.0 (Advanced Features)
- [ ] **Performance**: Retry mechanisms, offline mode, progress indicators
- [ ] **ML Detection**: Context-aware analysis, dependency scanning, metrics dashboard
- [ ] **Enterprise**: SSO/LDAP, audit logging, RBAC, compliance reporting
- [ ] **Scale**: Distributed scanning, caching, webhooks, REST API

## Version 1.0.0 (Production Ready)
- [ ] Comprehensive documentation & 100% test coverage
- [ ] Performance benchmarks & security audit
- [ ] Stable API guarantee with LTS commitment
- [ ] Migration guides & professional support


## Long-term Goals

- **Developer Experience**: IDE plugins, debugging tools, plugin API, i18n support
- **Community**: GitHub organization, contribution guidelines, pattern sharing
- **Ecosystem**: Editor plugins (VS Code, IntelliJ, Vim), CI/CD integrations
- **Research**: AI-powered suggestions, automated fixes, pattern learning

## Release Schedule

| Version | Target Date | Focus Area |
|---------|------------|------------|
| 0.2.11 | Immediate | Critical Fixes (Exit codes & docs) |
| 0.2.12 | 2025 Q3 | User Experience |
| 0.3.0 | 2025 Q4 | Configuration |
| 0.4.0 | 2026 Q1 | Enhanced detection |
| 0.5.0 | 2026 Q2 | Integrations |
| 1.0.0 | 2027 Q3 | Production ready |



## User Testing Insights (2025-07-22)

### 🌟 What's Working Well
- Excellent demo mode with practical examples
- Clear security detection messages
- Good visual design with colors and icons
- `--quickstart` and `--stats` work correctly

### 📊 Key Usage Patterns
- Direct file checking (`--check-file`) is primary use case
- JSON input rarely used in practice
- Users expect proper exit codes for CI/CD automation
- Dry-run mode helpful for debugging false positives

## Testing Checklist for Contributors

Before marking any feature as "completed", verify:
- [ ] Exit codes work correctly (echo $? after running)
- [ ] Documentation referenced in error messages exists
- [ ] Feature works in both Linux and Windows
- [ ] --quiet mode is actually quiet
- [ ] Error output goes to stderr, not stdout

## How to Contribute

1. **Fix critical bugs first** - Check exit code issue
2. Check the [Issues](https://github.com/antimon-security/antimon/issues) for tasks
3. Fork the repository
4. Create a feature branch
5. Submit a pull request
6. Join our discussions

## Feedback

We welcome feedback and suggestions! Please open an issue or start a discussion to share your ideas for improving antimon.


