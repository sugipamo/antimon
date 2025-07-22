# antimon Development Roadmap

## Current Status (2025-07-22)

### Recent Achievements:
- ✅ **v0.2.15 (In Progress)**: Fixed critical code quality issues - circular dependencies, unsafe input(), os.system, added Python dangerous code detection
- ✅ **v0.2.14**: Developer tools - watch mode, pattern testing, auto-fix suggestions, first-run setup
- ✅ **v0.2.13**: Batch processing & JSON output format 
- ✅ **v0.2.12**: Enhanced success messages showing detailed information about what was checked
- ✅ **v0.2.11**: Fixed exit codes (0=success, 1=error, 2=security issue) and comprehensive FAQ documentation
- ✅ **v0.2.10**: Verified `--quickstart`, `--stats`, and `--config` functionality
- ✅ **v0.2.1-v0.2.8**: Core features including detector fixes, direct file checking, Claude Code integration, and structured logging

### Quality Check Summary (2025-07-22):
- ✅ **pytest**: 202/204 tests passing (76% code coverage) - 2 tests failing in test_last_error.py due to state persistence
- ✅ **ruff**: All auto-fixable style issues fixed
- ⚠️ **mypy**: 108 type errors remaining (future version)
- ⚠️ **src-check**: Score 57.5/100 (slightly decreased due to stricter checks):
  - ✅ Fixed all 7 high severity circular dependency issues
  - ✅ Fixed os.system security vulnerability
  - ✅ Fixed unsafe input() usage for Python 2 compatibility
  - ✅ Added Python dangerous code detection (os.system, eval, exec, etc.)
  - Remaining: 4 high severity issues:
    - 2 instances of unsafe input() usage (false positives - already using safe_input helper)
    - 1 import inside function in color_utils.py line 76
    - 1 high coupling issue (color_utils.py: God class 'Colors' with 16 attributes)
  - Remaining: 128 medium severity issues (mostly print statements, complexity)
  - Remaining: 11 low severity issues

## Project Vision

Transform antimon from a standalone script into a robust, extensible Python package that can be easily integrated into various AI coding assistant workflows and CI/CD pipelines.

## Completed Versions

### Version 0.2.12 (User Experience) - COMPLETED
- Success message improvements (show what was checked)
- Fixed duplicate output bug in verbose mode
- Implemented --version flag properly
- Enhanced --stats flag with meaningful statistics

### Version 0.2.13 (Batch Processing & JSON) - COMPLETED
- Batch File Checking with progress indicators
- JSON Output Format for CI/CD integration
- Brief Mode for concise security reports
- Exit Code Documentation

### Version 0.2.14 (Developer Tools) - COMPLETED
- Watch Mode for continuous monitoring
- Pattern Testing to test detection patterns
- Auto-fix Suggestions for common security fixes
- Setup Status on First Run

## Version 0.2.15 (Code Quality & Performance) - IN PROGRESS

### Completed:
- Fixed critical code quality issues (circular dependencies, os.system, unsafe input())
- Added Python dangerous code detection (os.system, eval, exec, subprocess with shell=True)
- Created centralized logging infrastructure
- Fixed Ruff linting issues

### Remaining Tasks:
1. **Complete Logging Migration** (High Priority) - Convert 280+ print statements
2. **Performance Optimizations** (Medium Priority) - Caching, parallel processing
3. **Code Quality Improvements** (Medium Priority) - Type hints, reduce coupling
4. **Documentation Updates** - Windows setup, CI/CD examples, API docs

## Version 0.3.0 (Configuration Support)
- [ ] TOML configuration file support (`antimon.toml`)
- [ ] Custom pattern definitions
- [ ] Enable/disable specific detectors
- [ ] Severity levels for detections
- [ ] Whitelist/ignore patterns
- [ ] Global configuration (`~/.config/antimon/antimon.toml`)
- [ ] Environment variable overrides
- [ ] Configuration file validation and schema
- [ ] `.antimonignore` file support for project-specific exclusions
- [ ] `--generate-config` command to create configuration template
- [ ] Configuration inheritance (global → project → command-line)

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
- [ ] **Internationalization (i18n)**: Multi-language support starting with Japanese
- [ ] **Interactive Fix Mode**: `--fix-interactive` to apply suggested fixes with confirmation
- [ ] **Learning Mode**: `--learn` to understand why patterns are dangerous with examples

## Version 0.2.16 (User Experience Polish) - CRITICAL

### Critical Fixes (Must Do):
- [ ] Fix Silent Success - Change default log level to INFO
- [ ] Add Operation Context - Show what's being checked
- [ ] Fix --config Flag - Implement or remove
- [ ] Improve Default Verbosity - Add progress indicators

### High Priority:
- [ ] Quick Commands (`antimon .`, short aliases)
- [ ] .antimonignore file support
- [ ] Better success feedback
- [ ] Git integration (pre-commit hooks)

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

| Version | Target Date | Focus Area | Status |
|---------|------------|------------|--------|
| 0.2.11 | Released | Critical Fixes (Exit codes & docs) | ✅ Completed |
| 0.2.12 | Released | User Experience | ✅ Completed |
| 0.2.13 | Released | Batch Processing & JSON | ✅ Completed |
| 0.2.14 | Released | Developer Tools | ✅ Completed |
| 0.2.15 | 2025-07-25 | Code Quality & Performance | 🚧 In Progress |
| 0.2.16 | 2025-08-01 | User Experience Polish | 🔥 Critical |
| 0.3.0 | 2025-10-01 | Configuration | 📋 Planned |
| 0.4.0 | 2026-01-15 | Enhanced detection | 📋 Planned |
| 0.5.0 | 2026-04-01 | Integrations | 📋 Planned |
| 1.0.0 | 2027-07-01 | Production ready | 🎯 Goal |










## User Experience Summary (2025-07-22)

### Key Findings:
1. **The tool is too quiet in normal mode** - users don't see success confirmations
2. **Critical security gap fixed** - Added Python dangerous code detection
3. **Logging migration incomplete** - 280+ print statements remain
4. **Missing persistent settings** - .antimonignore support needed

### Most Common User Workflows:
- 80% use direct file checking (`--check-file`)
- 15% use content checking (`--check-content`)
- 5% use JSON mode (CI/CD pipelines)

## Next Immediate Tasks (2025-07-22)

1. **Complete Logging Migration** (Priority: HIGH)
   - Convert 280+ print statements to use logger.py
   - Implement proper verbose mode
   
2. **Add .antimonignore Support** (Priority: HIGH)
   - Allow persistent file/pattern exclusions
   - Support glob patterns
   
3. **Fix User Experience Issues** (Priority: HIGH)
   - Fix silent success in normal mode
   - Add operation context
   - Implement or remove --config flag
   
4. **Improve Test Coverage** (Priority: MEDIUM)
   - Current: 77%, Target: 85%+


