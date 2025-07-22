# antimon Development Roadmap

## Current Status (2025-07-22)

🎉 **Version 0.2.7 Major Features Completed!** 

### Recent Achievements:
- ✅ Transformed into a proper Python package with comprehensive testing
- ✅ Fixed detector functions and added Edit/MultiEdit tool support
- ✅ Enhanced UX with colors, test command, and better error messages
- ✅ Added `--allow-file` option with glob pattern support
- ✅ Implemented `--status`, `--dry-run`, and `--explain-last-error` commands
- ✅ Created structured logging foundation and setup wizard

### Quality Check Summary (2025-07-22)
- ✅ **pytest**: 119/119 tests passing! (75% code coverage)
  - Fixed: UnboundLocalError in core.py:472 - properly initialized 'config' variable
  - Fixed: AttributeError in core.py:153 - changed logger.isEnabledFor() to logger.is_enabled_for()
  - All tests are now passing
- ✅ **ruff**: All errors passed! No issues found
  - Previously fixed: Whitespace issues (W293), bare except (E722), undefined names (F821)
  - Previously fixed: Variable naming conventions (N806, N802)
  - Previously fixed: Unused loop variables (B007)
  - Added RUF001 and SIM102 to ignore list for better code readability
- ⚠️ **mypy**: 81 type errors remaining (to be addressed)
  - Main issues: Missing type parameters for generics, missing return type annotations
  - AttributeError issues with ColorFormatter in setup_claude_code.py
- ⚠️ **src-check**: Score 51.2/100 🟠 (105 issues: 10 high, 87 medium, 8 low)
  - Main issues: High coupling, unused imports, print statements instead of logging
  - Security concerns: Usage of input() and os.system()
  - Architecture score: 40/100 (needs improvement)
  - God classes detected: Colors (16 attributes), InteractiveDemo (336 lines)

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




### Version 0.2.10 (Critical Fixes & UX Polish) - NEXT RELEASE

#### Critical Bug Fixes:
- [ ] Fix `--quickstart` NotImplementedError
- [ ] Implement `--stats` functionality
- [ ] Fix exit codes (0=OK, 1=Error, 2=Security Issue)
- [ ] Create docs/faq.md file with common questions
- [ ] Remove or hide `--config` option until v0.3.0

#### User Experience Improvements:
- [ ] Batch file checking with glob patterns (`antimon --check-files "*.py"`)
- [ ] JSON output format (`--output-format json`)
- [ ] Windows-specific Claude Code setup instructions
- [ ] Success message improvements (show what was checked)
- [ ] Quiet mode fixes (truly silent except errors)
- [ ] Progress bar for large file checks
- [ ] Simple caching for repeated checks
- [ ] Pipeline-friendly output options

#### Documentation Improvements:
- [ ] Create comprehensive FAQ document
- [ ] Add `--verbose` output examples to help
- [ ] Windows installation guide
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
| 0.2.10 | 2025 Q3 | Critical Fixes & UX Polish |
| 0.3.0 | 2025 Q4 | Configuration |
| 0.4.0 | 2026 Q1 | Enhanced detection |
| 0.5.0 | 2026 Q2 | Integrations |
| 1.0.0 | 2027 Q3 | Production ready |



## Project Maintenance Notes (2025-07-22)

### Current Project Health:
- ✅ All tests passing (119/119) with 75% coverage
- ✅ No ruff issues - all checks passing
- ⚠️ 81 mypy type errors remaining
- ⚠️ src-check score: 51.2/100

### Next Priority Tasks:
1. **Type Safety**: Fix 81 mypy errors
2. **Code Quality**: Address src-check issues (unused imports, print statements)
3. **Architecture**: Refactor god classes (Colors, InteractiveDemo)



## User Feedback Summary (2025-07-22)

Based on comprehensive user testing, the following improvements would significantly enhance the user experience:

### 🌟 Strengths (What's Working Well)
- Excellent demo mode with clear, practical examples
- Comprehensive help documentation
- Clear security detection messages with actionable fixes
- Good use of colors and icons for visual clarity
- Simple and intuitive command-line interface

### 🔧 Critical Issues (Must Fix for v0.2.10)
1. **Broken Features**: 
   - `--quickstart` option throws NotImplementedError
   - `--stats` option is not implemented
   - `--config` option is shown but not implemented (planned for v0.3.0)
2. **Exit Codes**: Always returns 0, breaking CI/CD integration
   - Should return: 0=success, 1=error, 2=security issue detected
3. **Documentation**: Referenced docs/faq.md file doesn't exist
4. **Cross-Platform**: Windows setup instructions missing for Claude Code integration

### 💡 Top User Requests
1. **Batch Operations**: Check multiple files with wildcards (`antimon --check-files "*.py"`)
2. **Machine-Readable Output**: JSON format for automation (`--output-format json`)
3. **Better Success Feedback**: Show what was actually checked
4. **Performance**: Progress bars and caching for large operations
5. **Integration**: Examples for CI/CD pipelines

### 📊 Usage Patterns Observed
- Users primarily use direct file checking (`--check-file`) over JSON input
- Dry-run mode is popular for understanding detections
- Many users struggle with initial Claude Code integration
- False positives in documentation/example code are common pain points

## How to Contribute

1. Check the [Issues](https://github.com/antimon-security/antimon/issues) for tasks
2. Fork the repository
3. Create a feature branch
4. Submit a pull request
5. Join our discussions

## Feedback

We welcome feedback and suggestions! Please open an issue or start a discussion to share your ideas for improving antimon.


