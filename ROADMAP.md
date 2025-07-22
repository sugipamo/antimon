# antimon Development Roadmap

## Current Status (2025-07-22)

### Recent Achievements:
- ✅ **v0.2.12 (In Progress)**: Enhanced success messages showing detailed information about what was checked
- ✅ **v0.2.11**: Fixed exit codes (0=success, 1=error, 2=security issue) and comprehensive FAQ documentation
- ✅ **v0.2.10**: Verified `--quickstart`, `--stats`, and `--config` functionality
- ✅ **v0.2.1-v0.2.8**: Core features including detector fixes, direct file checking, Claude Code integration, and structured logging

### Quality Check Summary (2025-07-22):
- ✅ **pytest**: 140/140 tests passing (74% code coverage) - All tests are stable
- ✅ **ruff**: All style issues fixed
- ⚠️ **mypy**: 81 type errors remaining (future version)
- ⚠️ **src-check**: Score 49.9/100 - Critical issues identified:
  - 10 high severity issues (circular dependencies, security concerns)
  - 93 medium severity issues (print statements, complexity, documentation)
  - 9 low severity issues

## Project Vision

Transform antimon from a standalone script into a robust, extensible Python package that can be easily integrated into various AI coding assistant workflows and CI/CD pipelines.

### Version 0.2.12 (User Experience) - COMPLETED (2025-07-22)

#### Completed:
- [x] Success message improvements (show what was checked)
- [x] Fixed duplicate output bug in verbose mode
- [x] Implemented --version flag properly
- [x] Enhanced --stats flag with meaningful statistics
- [x] Fixed JSON error handling
- [x] Standardized output streams
- [x] Fixed quickstart message behavior

### Version 0.2.13 (Batch Processing & JSON) - COMPLETED (2025-07-22)

#### Completed:
- [x] **Batch File Checking**: `antimon --check-files "src/**/*.py"` with progress indicators
- [x] **JSON Output Format**: `--output-format json` for CI/CD integration
- [x] **Brief Mode**: `--brief` for concise security reports
- [x] **Exit Code Documentation**: Show meaning in error messages (e.g., "Exit code: 2 (Security issue detected)")
- [x] **Error Recovery Hints**: Always show `--explain-last-error` hint on security detections

#### Moved to Next Version:
- [ ] **Watch Mode**: `antimon --watch <directory>` for continuous monitoring (→ v0.2.14)
- [ ] **Pattern Testing**: `antimon --test-pattern <pattern>` to test detection patterns (→ v0.2.14)
- [ ] **Auto-fix Suggestions**: Provide code snippets for common security fixes (→ v0.2.14)
- [ ] **Setup Status on First Run**: Show Claude Code integration status on initial execution (→ v0.2.14)

#### Documentation:
- [ ] Windows-specific Claude Code setup instructions
- [ ] CI/CD integration examples
- [ ] Common false positive scenarios and solutions

### Version 0.2.14 (Developer Tools) - NEXT

#### TODO:
1. **Watch Mode**: `antimon --watch <directory>` for continuous monitoring
   - Monitor files for changes
   - Re-check modified files automatically
   - Show real-time status
   
2. **Pattern Testing**: `antimon --test-pattern <pattern>` to test detection patterns
   - Test custom patterns before adding them
   - Show what would match
   - Help debug false positives
   
3. **Auto-fix Suggestions**: Provide code snippets for common security fixes
   - Generate safe alternatives for detected issues
   - Copy-paste ready solutions
   - Language-specific fixes
   
4. **Setup Status on First Run**: Show Claude Code integration status on initial execution
   - Auto-detect Claude Code installation
   - Show hook configuration status
   - Offer setup if not configured

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

## Version 1.0.0 (Production Ready)
- [ ] Comprehensive documentation & 100% test coverage
- [ ] Performance benchmarks & security audit
- [ ] Stable API guarantee with LTS commitment
- [ ] Migration guides & professional support

## User Experience Improvement Priorities

### 🎯 Based on Comprehensive User Testing (2025-07-22)

#### Phase 1: Immediate UX Improvements (v0.2.14)
- [ ] **First-run Experience Enhancement**: Show Claude Code integration status automatically on first execution
- [ ] **Error Recovery Guidance**: Always append "Run 'antimon --explain-last-error' for details" to security detection messages
- [ ] **Pattern Transparency**: Add `--list-patterns` command to show all active detection patterns
- [ ] **False Positive Reporting**: Add `--report-false-positive` to generate GitHub issue template with context

#### Phase 2: Configuration & Persistence (v0.3.0) 
- [ ] **Project Configuration**: Support `.antimonignore` file for project-specific exclusions
- [ ] **Config Generation**: Add `--generate-config` to create antimon.toml template with all options
- [ ] **Config Discovery**: Show configuration file locations in `--status` output
- [ ] **Team Sharing**: Support config inheritance (global → project → local → CLI args)

#### Phase 3: Developer Workflow (v0.4.0)
- [ ] **Watch Mode**: Implement `antimon --watch <dir>` for real-time monitoring during development
- [ ] **Pattern Testing**: Add `--test-pattern <pattern>` to validate custom detection patterns
- [ ] **IDE Status Bar**: Provide simple API endpoint for IDE extensions to show status
- [ ] **Quick Fix Snippets**: Generate copy-paste ready fixes for common issues

#### Phase 4: Enterprise & Team Features (v0.5.0)
- [ ] **CI/CD Templates**: Provide ready-to-use configs for GitHub Actions, GitLab CI, Jenkins
- [ ] **Audit Trail**: Store detection history locally with `--history` command
- [ ] **Team Dashboards**: Export detection statistics in various formats (JSON, CSV, HTML)
- [ ] **Policy Templates**: Provide industry-specific security policy templates

#### Phase 5: Internationalization (v0.6.0)
- [ ] **Japanese Support**: Full translation of error messages, help text, and documentation
- [ ] **Language Detection**: Auto-detect system locale and use appropriate language
- [ ] **Community Translations**: Framework for community-contributed translations
- [ ] **RTL Support**: Proper support for right-to-left languages

## Next Immediate Tasks

### Version 0.2.14 (Developer Tools) - Priority Tasks:
1. **Watch Mode**: `antimon --watch <directory>` for continuous monitoring
2. **Pattern Testing**: `antimon --test-pattern <pattern>` to test detection patterns
3. **Auto-fix Suggestions**: Provide code snippets for common security fixes
4. **Setup Status on First Run**: Show Claude Code integration status on initial execution

### Documentation Improvements:
1. **Windows Setup Guide**: Create detailed Windows-specific Claude Code setup instructions
2. **CI/CD Examples**: Add GitHub Actions, GitLab CI, Jenkins examples
3. **False Positive Guide**: Document common false positive scenarios and solutions

### Critical Code Quality Issues (Must address before v0.3.0):
- [ ] Fix circular dependency risks in 7 files (imports inside functions):
  - color_utils.py: line 63
  - core.py: lines 569, 570, 662, 740
  - detectors.py: lines 64, 142, 240, 322, 386, 466
  - first_run.py: line 85
- [ ] Replace os.system in color_utils.py (line 70) with safer alternative
- [ ] Fix unsafe input() usage for Python 2 compatibility:
  - demo.py: lines 236, 246, 306, 313, 322, 329, 330
  - first_run.py: line 125
- [ ] Add basic type hints to public API functions
- [ ] Start converting print statements to logging (280+ occurrences)

### Code Quality Improvements (Priority for v0.3.0+):
- [ ] Replace print statements with proper logging throughout codebase (280+ occurrences)
- [ ] Add missing type hints (60+ functions need type hints)
- [ ] Reduce module coupling (split large modules, reduce imports)
  - Refactor modules with >15 external calls:
    - cli.py: 94 external calls
    - color_utils.py: 52 external calls
    - core.py: 286 external calls
    - demo.py: 98 external calls
    - detectors.py: 78 external calls
    - error_context.py: 58 external calls
    - first_run.py: 60 external calls
- [ ] Fix high complexity functions (functions exceeding complexity limit of 10):
  - cli.py: main() - complexity 33
  - core.py: process_stdin() - complexity 46
  - core.py: _display_security_issues() - complexity 18
  - core.py: check_file_directly() - complexity 19
  - core.py: validate_hook_data() - complexity 16
  - core.py: _validate_required_fields() - complexity 14
  - core.py: check_files_batch() - complexity 16
  - core.py: check_content_directly() - complexity 15
  - detectors.py: detect_filenames() - complexity 11
  - detectors.py: detect_llm_api() - complexity 14
  - detectors.py: detect_api_key() - complexity 11
  - error_context.py: _get_suggestions() - complexity 11
- [ ] Improve test coverage from 74% to 85%+
- [ ] Address security concerns:
  - Handle input() safely for Python 2 compatibility (already listed in critical issues)

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
| 0.2.12 | Released | User Experience | ✅ Completed |
| 0.2.13 | Released | Batch Processing & JSON | ✅ Completed |
| 0.2.14 | 2025-08-15 | Developer Tools | 🚧 Next Release |
| 0.3.0 | 2025-10-01 | Configuration | 📋 Planned |
| 0.4.0 | 2026-01-15 | Enhanced detection | 📋 Planned |
| 0.5.0 | 2026-04-01 | Integrations | 📋 Planned |
| 1.0.0 | 2027-07-01 | Production ready | 🎯 Goal |



## Developer-Centric Features (v0.5.0+)

### 🛠️ Making antimon Developer-Friendly
- Shell aliases and smart defaults
- Editor integrations (VS Code, Vim, Emacs)
- Git hooks and CI/CD templates
- Security learning mode with pattern playground
- Team exception sharing and severity levels

## Testing Checklist

Before marking any feature as "completed", verify:
- Exit codes work correctly
- Documentation exists for referenced features
- Cross-platform compatibility (Linux/Windows)
- Output stream consistency (stdout/stderr)
- All documented flags work as expected
- No duplicate output in any mode

## User Experience Enhancement Plan

### 🎯 Based on Comprehensive User Testing (2025-07-22)

#### Key Findings:
1. **Onboarding**: Need auto-status display on first run and clearer Claude Code integration guidance
2. **Error Recovery**: Must append "Run 'antimon --explain-last-error' for details" to all security detections
3. **Pattern Transparency**: Users need `--list-patterns` and `--test-pattern` commands
4. **Team Collaboration**: Requires `.antimonignore` and project-level configuration support
5. **False Positive Management**: Need persistent ignore patterns and easy reporting mechanism

### 🌟 What's Working Well
- Clear error messages with risks, fixes, and best practices
- Excellent demo mode with 10 practical scenarios
- Well-organized help system
- Enhanced success feedback (v0.2.12)
- Flexible input modes (files, content, JSON)

### 📊 Key Usage Patterns
- 80% use direct file checking (`--check-file`)
- 15% use content checking (`--check-content`)
- 5% use JSON mode (mainly CI/CD)
- Exit codes critical for automation
- Verbose mode essential for debugging
## How to Contribute

1. Check the [Issues](https://github.com/antimon-security/antimon/issues) for tasks
2. Fork the repository
3. Create a feature branch
4. Submit a pull request
5. Join our discussions

## Feedback

We welcome feedback and suggestions! Please open an issue or start a discussion to share your ideas for improving antimon.


