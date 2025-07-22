# antimon Development Roadmap

## Current Status (2025-07-22)

### Recent Achievements:
- ✅ **v0.2.11**: Fixed exit codes (0=success, 1=error, 2=security issue) and comprehensive FAQ documentation
- ✅ **v0.2.10**: Verified `--quickstart`, `--stats`, and `--config` functionality
- ✅ **v0.2.1-v0.2.8**: Core features including detector fixes, direct file checking, Claude Code integration, and structured logging

### Quality Check Summary:
- ✅ **pytest**: 119/119 tests passing (75% code coverage)
- ✅ **ruff**: All style issues fixed (18 SIM117 warnings acceptable)
- ⚠️ **mypy**: 81 type errors remaining (future version)
- ⚠️ **src-check**: Score 53.0/100 - Main issues:
  - Architecture: High coupling in several modules
  - Code quality: Many print statements should use logging
  - Type safety: Missing type hints
  - Documentation: Missing parameter/return documentation

## Project Vision

Transform antimon from a standalone script into a robust, extensible Python package that can be easily integrated into various AI coding assistant workflows and CI/CD pipelines.

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

## Next Immediate Tasks

1. **Code Quality Improvements**
   - [ ] Replace print statements with proper logging throughout codebase
   - [ ] Add missing type hints (60+ functions need type hints)
   - [ ] Reduce module coupling (split large modules, reduce imports)
   - [ ] Fix high complexity functions (10+ functions exceed complexity limit)
   - [ ] Improve test coverage from 75% to 85%+

2. **Documentation Enhancement**
   - [ ] Add missing parameter/return documentation for functions
   - [ ] Add API documentation
   - [ ] Create contributor's guide
   - [ ] Add more examples in the examples/ directory


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



## User Testing Insights

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

## Developer-Centric Features

### 🛠️ Making antimon Developer-Friendly

Based on real-world usage patterns, developers need:

#### **Quick Wins for Daily Use**
1. **Shell Aliases Support**
   ```bash
   # Add to documentation
   alias check='antimon --check-file'
   alias checkall='antimon --check-files "**/*.py"'
   alias checksafe='antimon --dry-run --check-file'
   ```

2. **Editor Integration Snippets**
   - VS Code: Task runner configuration
   - Vim: Async lint integration
   - Emacs: Flycheck checker
   - Sublime: Build system config

3. **Git Integration**
   - Pre-commit hook template
   - Pre-push validation script
   - Commit message validation
   - Branch protection rules

4. **Smart Defaults**
   - Auto-detect project type (Python/JS/Go)
   - Language-specific rule sets
   - Framework detection (Django/React/etc)
   - Severity-based filtering

#### **Developer Education**
1. **Security Learning Mode**
   - Explain why each pattern is dangerous
   - Show real-world exploit examples
   - Provide secure coding alternatives
   - Link to OWASP/CWE references

2. **Pattern Playground**
   - Test custom patterns safely
   - See what existing patterns catch
   - Generate pattern documentation
   - Share patterns with team

## Testing Checklist

Before marking any feature as "completed", verify:
- [ ] Exit codes work correctly (echo $? after running)
- [ ] Documentation referenced in error messages exists
- [ ] Feature works in both Linux and Windows
- [ ] --quiet mode is actually quiet
- [ ] Error output goes to stderr, not stdout
- [ ] Success messages appear in normal mode
- [ ] Batch operations show progress
- [ ] Configuration files are loaded correctly

## User Experience Enhancement Plan

### 🎯 Based on User Perspective Analysis

The following enhancements would significantly improve the antimon experience:

#### 1. **Clear Success Feedback** 🟢
**Issue**: When files pass security checks, users get no feedback in normal mode
**Solution**: 
- Add success messages by default: "✓ config.py: No security issues detected"
- Show summary for batch operations: "✓ Checked 15 files, all secure"
- Make --quiet truly silent, normal mode informative

#### 2. **Better Error Context and Recovery** 🔧
**Issue**: Users know what's wrong but not always how to fix it
**Solution**:
- Add `--suggest-fix` flag that shows safe code alternatives
- Provide copy-paste ready solutions for common issues
- Link to specific documentation sections for each error type
- Example: "API key detected. Try: API_KEY = os.environ.get('API_KEY')"

#### 3. **Simplified Configuration** ⚙️
**Issue**: No persistent configuration, must repeat flags
**Solution** (Priority for v0.3.0):
- Support `.antimonrc` or `antimon.yml` in project root
- Global config in `~/.config/antimon/`
- Environment variable support: `ANTIMON_ALLOW_FILES`, `ANTIMON_DISABLE_DETECTORS`
- Config wizard: `antimon --init-config`

#### 4. **Enhanced Logging and Reporting** 📊
**Issue**: Limited visibility into what was checked and why
**Solution**:
- Add `--report` flag for detailed analysis output
- Support multiple output formats: `--output-format json|yaml|html|markdown`
- Save scan history: `~/.antimon/history.log`
- Show detection statistics and trends

#### 5. **Batch Operations and Integration** 🚀
**Issue**: Checking multiple files is cumbersome
**Solution**:
- Support glob patterns: `antimon --check-files "src/**/*.py"`
- Add `--watch` mode for continuous monitoring
- Provide pre-commit hook template
- Better CI/CD examples (GitHub Actions, GitLab CI, Jenkins)

#### 6. **Interactive Mode Improvements** 💬
**Issue**: Current interaction is limited to demo and setup
**Solution**:
- Interactive fix mode: Guide users through resolving issues
- Pattern explorer: Test custom patterns interactively
- Learning mode: Explain why each pattern is dangerous

#### 7. **Documentation Accessibility** 📚
**Issue**: Help is scattered across multiple flags
**Solution**:
- Unified help system: `antimon help [topic]`
- In-context help: Show relevant docs for current error
- Offline documentation browser
- Quick reference card generation

#### 8. **Performance and Feedback** ⚡
**Issue**: No progress indication for large operations
**Solution**:
- Progress bars for multi-file operations
- Estimated time remaining
- Parallel file checking option
- Cache results for unchanged files

## Common User Scenarios & Pain Points

### 🔍 Scenario Analysis

#### 1. **New User First Experience**
**Current State**: Good - Interactive setup, demo mode, quickstart guide
**Pain Points**: 
- Unclear which mode to use (JSON vs direct checking)
- Confusion about when to use as hook vs CLI tool
**Improvement**: Add decision tree in quickstart

#### 2. **CI/CD Pipeline Integration**
**Current State**: Working - Proper exit codes, JSON input support
**Pain Points**:
- No ready-made pipeline templates
- Limited examples for different CI systems
- No built-in report generation for CI artifacts
**Improvement**: Provide copy-paste CI/CD configs

#### 3. **Development Workflow**
**Current State**: Basic - Manual file checking works
**Pain Points**:
- Repetitive checking of same files
- No IDE integration
- Can't check files before committing
**Improvement**: Watch mode, pre-commit hooks, IDE plugins

#### 4. **Team Collaboration**
**Current State**: Limited - No shared configurations
**Pain Points**:
- Each developer must configure individually
- No way to share custom patterns
- Inconsistent security policies across team
**Improvement**: Shared config files, pattern libraries

#### 5. **False Positive Management**
**Current State**: Basic - Can disable detectors or allow files
**Pain Points**:
- Must remember flags for each run
- No way to annotate code as safe
- Limited pattern customization
**Improvement**: Inline annotations, persistent allowlists

## Priority Implementation Order

### Phase 1: Immediate UX Fixes (v0.2.12)
1. Success message implementation
2. True quiet mode
3. Basic batch file checking
4. Improved error suggestions

### Phase 2: Configuration & Persistence (v0.3.0)
1. Configuration file support
2. Environment variable handling
3. Project and global configs
4. Config migration tools

### Phase 3: Advanced Features (v0.4.0+)
1. Interactive fix mode
2. Watch mode
3. Advanced reporting
4. IDE integrations

## How to Contribute

1. Check the [Issues](https://github.com/antimon-security/antimon/issues) for tasks
2. Fork the repository
3. Create a feature branch
4. Submit a pull request
5. Join our discussions

## Feedback

We welcome feedback and suggestions! Please open an issue or start a discussion to share your ideas for improving antimon.


