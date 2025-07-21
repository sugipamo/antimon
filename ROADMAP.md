# antimon Development Roadmap

## Current Status (2025-07-21)

🎉 **Version 0.2.7 Major Features Completed!** 

### Recent Achievements:
- ✅ Transformed into a proper Python package with comprehensive testing
- ✅ Fixed detector functions and added Edit/MultiEdit tool support
- ✅ Enhanced UX with colors, test command, and better error messages
- ✅ Added `--allow-file` option with glob pattern support
- ✅ Implemented `--status`, `--dry-run`, and `--explain-last-error` commands
- ✅ Created structured logging foundation and setup wizard

### Quality Check Summary (2025-07-21)
- ⚠️ **pytest**: 107/119 tests passing, 12 tests failing (74% code coverage)
  - Main failure: UnboundLocalError in core.py:472 - 'config' variable not properly initialized
  - Affects: Direct file/content checking functionality and CLI tests
- ⚠️ **Code quality tools**: Multiple issues detected
  - ruff: 529 errors (456 auto-fixable)
  - mypy: 82 type errors
  - src-check: 48.8/100 score

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


## 🚨 URGENT: Critical Fixes Needed (Version 0.2.9-hotfix)

### 1. **Fix failing tests** 🔴 CRITICAL
- [ ] Fix UnboundLocalError in core.py:472 - properly initialize 'config' variable
- [ ] Fix direct file/content checking functionality
- [ ] Ensure all 119 tests pass

### 2. **Code Quality** 🟠 HIGH PRIORITY
- [ ] Run `ruff check --fix src/` (456 auto-fixable issues)
- [ ] Fix remaining ruff issues (73 manual fixes)
- [ ] Add missing type annotations (82 mypy errors)




### Version 0.2.9 (User Experience Polish) ✅ MOSTLY COMPLETED

#### Completed Features:
- [x] GitHub URL fixes in README
- [x] dry-run mode documentation
- [x] Success feedback messages
- [x] Claude Code installation guidance
- [x] Configuration file clarification

#### Remaining Tasks:
- [ ] Multiple file check progress display
- [ ] Interactive tutorial mode
- [ ] Step-by-step configuration guide
- [ ] Staged error messages (simple → detailed → tutorial)

## Version 0.3.0 (Configuration Support)
- [ ] TOML configuration file support (`antimon.toml`)
- [ ] Custom pattern definitions
- [ ] Enable/disable specific detectors
- [ ] Severity levels for detections
- [ ] Whitelist/ignore patterns
- [ ] Global configuration (`~/.config/antimon/antimon.toml`)
- [ ] Environment variable overrides
- [ ] Configuration file validation and schema
- [ ] Configuration wizard: 対話的な設定ファイル生成ツール（antimon --init）
- [ ] Profile support: 開発/本番環境などプロファイル別設定
- [ ] Override mechanism: コマンドライン引数による設定の一時的な上書き

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


## Next Steps

🎯 **Version 0.2.10** (Beginner-friendly features) - Next implementation:
   - Interactive tutorial mode
   - Batch file checking
   - Staged error messages
   - Further UX improvements

🎯 **Version 0.3.0** (Configuration) - See Version 0.3.0 section for detailed tasks

## Release Schedule

| Version | Target Date | Focus Area |
|---------|------------|------------|
| 0.2.7-0.2.8 | 2025 Q3 | UX Enhancement (Complete) |
| 0.2.9 | 2025 Q3 | UX Polish (In Progress) |
| 0.2.10 | 2025 Q3 | Beginner-friendly features |
| 0.3.0 | 2025 Q4 | Configuration |
| 0.4.0 | 2026 Q1 | Enhanced detection |
| 0.5.0 | 2026 Q2 | Integrations |
| 1.0.0 | 2027 Q3 | Production ready |






## How to Contribute

1. Check the [Issues](https://github.com/antimon-security/antimon/issues) for tasks
2. Fork the repository
3. Create a feature branch
4. Submit a pull request
5. Join our discussions

## Feedback

We welcome feedback and suggestions! Please open an issue or start a discussion to share your ideas for improving antimon.


