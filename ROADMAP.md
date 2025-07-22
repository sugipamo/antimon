# antimon Development Roadmap

## Current Status (2025-07-22)

### Recent Achievements:
- ✅ **v0.2.12 (In Progress)**: Enhanced success messages showing detailed information about what was checked
- ✅ **v0.2.11**: Fixed exit codes (0=success, 1=error, 2=security issue) and comprehensive FAQ documentation
- ✅ **v0.2.10**: Verified `--quickstart`, `--stats`, and `--config` functionality
- ✅ **v0.2.1-v0.2.8**: Core features including detector fixes, direct file checking, Claude Code integration, and structured logging

### Quality Check Summary:
- ✅ **pytest**: 125/125 tests passing (75% code coverage) - All tests are stable
- ✅ **ruff**: All style issues fixed
- ⚠️ **mypy**: 81 type errors remaining (future version)
- ⚠️ **src-check**: Score 51.9/100 - See "Code Quality Improvements" section for detailed issues

## Project Vision

Transform antimon from a standalone script into a robust, extensible Python package that can be easily integrated into various AI coding assistant workflows and CI/CD pipelines.

### Version 0.2.12 (User Experience) - IN PROGRESS

#### Completed (2025-07-22):
- [x] Success message improvements (show what was checked)
  - Enhanced success messages to show file path, size, line count, and number of checks performed
  - Added comprehensive test coverage in `test_success_messages.py`
  - Maintains backward compatibility with quiet and verbose modes

#### Critical Bug Fixes (HIGHEST PRIORITY):
_See "User Experience Enhancement Plan" section for detailed list of critical fixes_

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

### Version 0.2.12 (Continuing):
_Critical bug fixes and feature implementations are tracked in the "User Experience Enhancement Plan" section above._

### Critical Code Quality Issues (Must address before v0.3.0):
- [ ] Fix circular dependency risks in 7 files (imports inside functions)
- [ ] Replace os.system in color_utils.py with safer alternative
- [ ] Add basic type hints to public API functions
- [ ] Start converting print statements to logging (at least in core.py)

### Code Quality Improvements (Priority for v0.3.0+):
- [ ] Replace print statements with proper logging throughout codebase (280+ occurrences)
- [ ] Add missing type hints (60+ functions need type hints)
- [ ] Reduce module coupling (split large modules, reduce imports)
  - Refactor modules with >15 external calls
- [ ] Fix high complexity functions (10+ functions exceed complexity limit)
  - cli.py: main() - complexity 31
  - core.py: process_stdin() - complexity 39
  - detectors.py: Multiple functions with complexity >10
- [ ] Improve test coverage from 75% to 85%+
- [ ] Address security concerns:
  - Handle input() safely for Python 2 compatibility

### Documentation Enhancement:
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

| Version | Target Date | Focus Area | Status |
|---------|------------|------------|--------|
| 0.2.11 | Released | Critical Fixes (Exit codes & docs) | ✅ Completed |
| 0.2.12 | 2025-08-15 | User Experience | 🚧 Next Release |
| 0.3.0 | 2025-10-01 | Configuration | 📋 Planned |
| 0.4.0 | 2026-01-15 | Enhanced detection | 📋 Planned |
| 0.5.0 | 2026-04-01 | Integrations | 📋 Planned |
| 1.0.0 | 2027-07-01 | Production ready | 🎯 Goal |



## User Testing Insights

_See detailed user testing analysis in the "User Experience Enhancement Plan" section below._

## Developer-Centric Features

### 🛠️ Making antimon Developer-Friendly

**Quick Wins**: Shell aliases, editor integrations (VS Code, Vim, Emacs), Git hooks, smart defaults

**Developer Education**: Security learning mode with explanations and pattern playground

_Detailed implementation planned for v0.5.0 (Integration Features) and beyond._

## User Recovery Guidance

### 🚨 When Detection Occurs - Enhancement Opportunities:

- **Current Strengths**: Clear explanations, quick fixes, best practices, informational links
- **Needed Enhancements**:
  - Show which detector triggered (for allowlisting)
  - Add severity levels
  - Provide copy-paste ready solutions
  - Add "override" instructions
  - Include "why dangerous" explanations
  - Support team exception sharing

_These enhancements are planned for v0.5.0 (Integration Features) and v0.6.0 (ML Detection)._

## Testing Checklist

Before marking any feature as "completed", verify:
- Exit codes work correctly
- Documentation exists for referenced features
- Cross-platform compatibility (Linux/Windows)
- Output stream consistency (stdout/stderr)
- All documented flags work as expected
- No duplicate output in any mode

## User Experience Enhancement Plan

### 🎯 Based on User Testing Analysis (2025-07-22)

After comprehensive testing from a user perspective, the following critical issues and enhancements have been identified:

### 🌟 What's Working Well
- **Error Messages**: Exceptionally clear with risks, fixes, and best practices
- **Demo Mode**: Excellent educational tool with 10 practical scenarios
- **Help System**: Well-organized with `--help`, `--quickstart`, `--help-errors`
- **Success Feedback**: Shows useful info (file size, checks performed) - Enhanced in v0.2.12
- **Multiple Input Modes**: Flexible with files, content, and JSON

### 🔴 Critical Issues to Fix (v0.2.12)
1. **Duplicate Output Bug**: All verbose mode messages appear twice with different formatting
2. **Missing Features**: 
   - `--version` flag documented but not implemented (shows error)
   - `--stats` flag doesn't provide meaningful statistics
3. **JSON Errors**: 
   - Error messages appear twice
   - Example JSON in error messages has syntax errors
4. **Output Stream Issues**: Mixed stdout/stderr causes automation problems
5. **Quickstart Message**: Claims to "only appear once" but appears every time

### 📊 Key Usage Patterns
- Primary use: Direct file checking (`--check-file`)
- JSON mode rarely used outside of CI/CD
- Users expect proper exit codes for automation
- Verbose mode used for debugging false positives
- Dry-run mode helpful for testing

### 🎯 Solutions by Priority

#### Phase 1: Critical Fixes (v0.2.12 - Immediate)
1. Fix duplicate logging bug in verbose mode
2. Implement `--version` flag properly
3. Make `--stats` show timing, pattern matches, file counts
4. Fix JSON error handling (no duplicates, correct syntax)
5. Standardize output streams (errors→stderr, normal→stdout)
6. Fix quickstart message behavior

#### Phase 2: Core Enhancements (v0.2.13)
1. **Batch File Checking**: `antimon --check-files "src/**/*.py"` with progress indicators
2. **JSON Output Format**: `--output-format json` for CI/CD integration
3. **Brief Mode**: `--brief` for concise security reports
4. **Exit Code Documentation**: Show meaning in error messages

#### Phase 3: Configuration Support (v0.3.0)
_See detailed configuration plans in Version 0.3.0 section_

#### Phase 4: Advanced Features (v0.4.0+)
_See roadmap sections for enhanced detection, integrations, and enterprise features_

## Common User Scenarios & Pain Points

### 🔍 Key Scenarios Identified:

1. **New User Experience**: Good setup, but needs clearer mode selection guidance
2. **CI/CD Integration**: Working but needs ready-made templates
3. **Development Workflow**: Basic functionality, needs watch mode and IDE plugins
4. **Team Collaboration**: Limited sharing capabilities, needs config files
5. **False Positive Management**: Basic controls, needs persistent allowlists

_Solutions for these scenarios are addressed in the version roadmap sections._


## How to Contribute

1. Check the [Issues](https://github.com/antimon-security/antimon/issues) for tasks
2. Fork the repository
3. Create a feature branch
4. Submit a pull request
5. Join our discussions

## Feedback

We welcome feedback and suggestions! Please open an issue or start a discussion to share your ideas for improving antimon.


