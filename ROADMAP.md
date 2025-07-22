# antimon Development Roadmap

## Current Status (2025-07-22)

### Recent Achievements:
- ✅ **v0.2.15 (In Progress)**: Fixed critical code quality issues - circular dependencies, unsafe input(), os.system
- ✅ **v0.2.14**: Developer tools - watch mode, pattern testing, auto-fix suggestions, first-run setup
- ✅ **v0.2.13**: Batch processing & JSON output format 
- ✅ **v0.2.12**: Enhanced success messages showing detailed information about what was checked
- ✅ **v0.2.11**: Fixed exit codes (0=success, 1=error, 2=security issue) and comprehensive FAQ documentation
- ✅ **v0.2.10**: Verified `--quickstart`, `--stats`, and `--config` functionality
- ✅ **v0.2.1-v0.2.8**: Core features including detector fixes, direct file checking, Claude Code integration, and structured logging

### Quality Check Summary (2025-07-22):
- ✅ **pytest**: 192/192 tests passing (77% code coverage) - All tests are stable
- ✅ **ruff**: All auto-fixable style issues fixed
- ⚠️ **mypy**: 108 type errors remaining (future version)
- ⚠️ **src-check**: Score 45.6/100 (analysis completed):
  - ✅ Fixed all 7 high severity circular dependency issues
  - ✅ Fixed os.system security vulnerability
  - ✅ Fixed unsafe input() usage for Python 2 in demo.py (using safe_input helper)
  - ✅ Fixed unsafe input() usage for Python 2 in first_run.py (using safe_input helper)
  - ✅ Fixed unsafe input() usage for Python 2 in setup_claude_code.py (using safe_input helper)
  - ✅ Removed misplaced test files (test_safe.py, test_api_key.py) from root directory
  - ✅ Cleaned up temporary files (htmlcov directory)
  - Remaining: 6 high severity issues:
    - 1 more instance of unsafe input() usage (in demo.py line 22 - false positive, already using safe_input)
    - 1 subprocess.run with shell=True in color_utils.py
    - 3 imports inside functions that may indicate circular dependencies
    - 1 high coupling issue
  - Remaining: 127 medium severity issues (mostly print statements, complexity)
  - Remaining: 11 low severity issues

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

### Version 0.2.14 (Developer Tools) - COMPLETED (2025-07-22)

#### Completed:
- [x] **Watch Mode**: `antimon --watch <directory>` for continuous monitoring
  - Monitor files for changes
  - Re-check modified files automatically  
  - Show real-time status with color-coded output
  - Display statistics (files monitored, checks performed, issues found)
  
- [x] **Pattern Testing**: `antimon --test-pattern <pattern>` to test detection patterns
  - Test patterns against all or specific detectors
  - Show which detectors would trigger
  - Display example patterns with `--pattern-examples`
  - Filter by detector type with `--detector <type>`
  
- [x] **Auto-fix Suggestions**: `antimon --autofix` provides code snippets for common security fixes
  - Environment variable replacements for API keys
  - Local model alternatives for LLM APIs
  - Security improvements for Docker configurations
  - Configuration-based alternatives for hardcoded localhost
  
- [x] **Setup Status on First Run**: Show Claude Code integration status on initial execution
  - Auto-detect Claude Code installation
  - Show hook configuration status  
  - Offer interactive setup wizard
  - Display appropriate guidance based on detected configuration

#### Documentation:
- [ ] Windows-specific Claude Code setup instructions
- [ ] CI/CD integration examples
- [ ] Common false positive scenarios and solutions

### Version 0.2.15 (Code Quality & Performance) - IN PROGRESS (2025-07-22)

#### Completed Tasks:
1. **Fixed Critical Code Quality Issues**:
   - ✅ Fixed circular dependency risks in all files:
     - color_utils.py: Moved platform import to module level
     - core.py: Moved glob and os imports to module level
     - detectors.py: Moved runtime_config import to module level
     - first_run.py: Removed duplicate subprocess import
   - ✅ Replaced os.system with subprocess.run in color_utils.py (safer alternative)
   - ✅ Fixed unsafe input() usage for Python 2 compatibility:
     - demo.py: Added safe_input() helper function for Python 2/3 compatibility
     - first_run.py: Added safe_input() helper function for Python 2/3 compatibility
     - setup_claude_code.py: Added safe_input() helper function for Python 2/3 compatibility
     - Note: src-check still reports false positives for input() inside safe_input functions
   - ✅ Type hints already present on all public API functions

#### Remaining Tasks:

1. **Logging Infrastructure** (High Priority):
   - Create a centralized logging module
   - Implement different log levels (DEBUG, INFO, WARNING, ERROR)
   - Support both file and console logging
   - Ensure backward compatibility with existing output behavior
   - Start converting print statements to logging (280+ occurrences)
   
2. **Performance Optimizations** (Medium Priority):
   - Optimize file scanning for large codebases
   - Implement caching for repeated pattern checks
   - Add parallel processing for batch file checking
   - Optimize regex compilation and reuse
   
3. **Code Quality Improvements** (Medium Priority):
   - Add missing type hints (60+ functions need type hints)
   - Reduce module coupling (split large modules, reduce imports)
   - Fix high complexity functions (11 functions exceed complexity limit of 10)
   - Refactor functions exceeding complexity limit of 10
   - Split large functions into smaller, focused functions
   - Improve modularity and separation of concerns
   - Improve test coverage from 77% to 85%+
   
4. **Documentation Updates**:
   - Windows-specific Claude Code setup instructions
   - CI/CD integration examples (GitHub Actions, GitLab CI)
   - Common false positive scenarios and solutions
   - Add missing parameter/return documentation for functions
   - Add API documentation
   - Create contributor's guide

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

## Version 0.2.16 (User Experience Quick Fixes)
- [ ] **Summary Mode for Batch Checks**: Add `--summary` flag to show only file counts, not all issues
- [ ] **Exclude Own Files**: Automatically exclude antimon's own test/demo files from checks
- [ ] **Persistent Allow List**: Create `.antimonallow` file for permanent file exclusions
- [ ] **Quick Disable**: Add `antimon --pause` and `antimon --resume` for temporary disabling
- [ ] **Check Git History**: Add `antimon --check-commits <n>` to scan recent commits
- [ ] **Severity Indicators**: Use 🔴 (critical), 🟡 (warning), 🟢 (info) in output
- [ ] **Context Lines**: Show 2 lines before/after detected issues with `--context`
- [ ] **Progress Bar Fix**: Make progress bar update in real-time, not just file count

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
| 0.2.15 | 2025-08-01 | Code Quality & Performance | 🚧 Next Release |
| 0.2.16 | 2025-08-15 | User Experience Quick Fixes | 📋 Planned |
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

#### New User Experience Issues Found:
1. **Logging Verbosity**: Error messages can be overwhelming in batch mode - need summary view
2. **False Positives in Own Code**: The tool flags its own test/demo files as security issues
3. **Unclear Next Steps**: When security issues are found, users may not know how to proceed
4. **Missing Whitelist Persistence**: `--allow-file` flags need to be repeated every time
5. **No Severity Levels**: All issues treated equally - no distinction between critical and minor
6. **Limited Context**: Error messages don't show enough surrounding code
7. **No Undo/Rollback**: If users accidentally commit with antimon disabled, no way to check retroactively

### 🌟 What's Working Well
- Clear error messages with risks, fixes, and best practices
- Excellent demo mode with 10 practical scenarios
- Well-organized help system
- Enhanced success feedback (v0.2.12)
- Flexible input modes (files, content, JSON)
- Comprehensive `--explain-last-error` with detailed explanations
- Auto-fix suggestions with concrete code examples

### 📊 Key Usage Patterns
- 80% use direct file checking (`--check-file`)
- 15% use content checking (`--check-content`)
- 5% use JSON mode (mainly CI/CD)
- Exit codes critical for automation
- Verbose mode essential for debugging

### 🚀 User Experience Improvements Needed (Priority)

#### 1. **Onboarding & Discovery** (v0.2.15)
- [ ] **Interactive Tutorial**: Add `antimon --tutorial` for hands-on learning
- [ ] **Smart Suggestions**: Detect common usage errors and suggest correct commands
- [ ] **Context-Aware Help**: Show relevant help based on detected file types
- [ ] **Setup Validation**: Add `antimon --validate-setup` to check configuration
- [ ] **First-Run Experience**: Automatically run `--status` on first execution
- [ ] **Quick Start Guide**: Display concise usage examples on first run

#### 2. **Error Messages & Recovery** (v0.2.15) 
- [ ] **Contextual Solutions**: Provide file-type specific solutions (e.g., Python vs JS)
- [ ] **Quick Fix Commands**: Generate ready-to-copy fix commands
- [ ] **Error History**: Add `antimon --history` to review past detections
- [ ] **Batch Fix Mode**: Support fixing multiple similar issues at once
- [ ] **Clearer False Positive Handling**: Add `--mark-false-positive` command
- [ ] **Error Context**: Show surrounding code lines for better understanding

#### 3. **Pattern Management** (v0.3.0)
- [ ] **Pattern Explorer**: Interactive mode to explore and test patterns
- [ ] **Custom Pattern Builder**: Wizard to create custom detection patterns
- [ ] **Pattern Sharing**: Export/import pattern configurations
- [ ] **Pattern Documentation**: Built-in docs for each detection pattern
- [ ] **List Patterns**: Add `--list-patterns` to show all active detection patterns
- [ ] **Pattern Severity Levels**: Allow users to set warning vs. error levels

#### 4. **Integration & Workflow** (v0.3.0)
- [ ] **Git Integration**: Auto-detect git hooks and offer setup
- [ ] **Pre-commit Templates**: Ready-to-use pre-commit configurations
- [ ] **Editor Plugins**: Official VS Code and IntelliJ plugins
- [ ] **Continuous Monitoring**: Background daemon mode for real-time checks
- [ ] **CI/CD Templates**: Ready-to-use GitHub Actions and GitLab CI templates
- [ ] **IDE Integration Status**: Show which IDEs have antimon configured

#### 5. **Performance & Scalability** (v0.4.0)
- [ ] **Incremental Scanning**: Only check changed files in watch mode
- [ ] **Parallel Processing**: Multi-threaded scanning for large codebases
- [ ] **Result Caching**: Cache results for unchanged files
- [ ] **Progress Indicators**: Better progress bars for large scans
- [ ] **Memory Usage Optimization**: Reduce memory footprint for large files
- [ ] **Streaming Analysis**: Process large files without loading into memory

### 📝 Documentation Gaps to Address

#### User Documentation:
- [ ] **Quick Reference Card**: One-page PDF with common commands
- [ ] **Video Tutorials**: 5-minute videos for common scenarios
- [ ] **Troubleshooting Guide**: Common issues and solutions
- [ ] **Integration Cookbook**: Step-by-step guides for various tools

#### Developer Documentation:
- [ ] **Plugin Development Guide**: How to create custom detectors
- [ ] **API Reference**: Complete API documentation
- [ ] **Architecture Overview**: System design documentation
- [ ] **Contributing Guide**: How to contribute effectively

### 🧭 User Journey Improvements

#### For New Users:
1. **Getting Started**
   - [ ] Show mini-tutorial on first run (5 most common commands)
   - [ ] Auto-detect project type and suggest relevant checks
   - [ ] Provide project-specific `.antimonrc` template generation
   - [ ] Add `antimon init` command for project setup

2. **Learning Curve**
   - [ ] Interactive mode: `antimon --interactive` for guided usage
   - [ ] Example library: `antimon --examples <detector>` shows real-world cases
   - [ ] Explain mode: `antimon --why <pattern>` explains why something is dangerous
   - [ ] Practice mode: `antimon --practice` with safe sandbox examples

#### For Regular Users:
1. **Daily Workflow**
   - [ ] Quick check: `antimon .` checks all files in current directory
   - [ ] Smart defaults: Remember last used options per project
   - [ ] Incremental checks: Only scan changed files since last run
   - [ ] IDE notifications: Desktop notifications for background checks

2. **Team Collaboration**  
   - [ ] Shared configs: `antimon --share-config` generates team config
   - [ ] Report generation: `antimon --report` creates markdown reports
   - [ ] Baseline mode: `antimon --baseline` to grandfather existing issues
   - [ ] Audit trail: Log all antimon decisions for compliance

#### For Power Users:
1. **Advanced Features**
   - [ ] Custom rules: YAML-based rule definition without coding
   - [ ] Hooks system: Pre/post check hooks for custom workflows
   - [ ] API mode: REST API for integration with other tools
   - [ ] Metrics export: Prometheus/Grafana compatible metrics

2. **Debugging & Analysis**
   - [ ] Debug mode: `antimon --debug` shows pattern matching details
   - [ ] Profiling: `antimon --profile` shows performance bottlenecks
   - [ ] Dry-run diff: Show what would change with different settings
   - [ ] Rule testing: Built-in test framework for custom rules

## How to Contribute

1. Check the [Issues](https://github.com/antimon-security/antimon/issues) for tasks
2. Fork the repository
3. Create a feature branch
4. Submit a pull request
5. Join our discussions

## Feedback

We welcome feedback and suggestions! Please open an issue or start a discussion to share your ideas for improving antimon.

## Next Immediate Tasks (2025-07-22)

Based on the current analysis and t-wada's recommendations:

1. **Implement Centralized Logging Module** (Priority: HIGH)
   - Replace 280+ print statements with proper logging
   - Create src/antimon/log.py with centralized configuration
   - Implement log levels (DEBUG, INFO, WARNING, ERROR)
   - Ensure backward compatibility with existing output behavior
   - Start with critical modules: core.py, cli.py, detectors.py

2. **Fix Remaining Ruff Issues** (Priority: MEDIUM)
   - Fix SIM105 in color_utils.py: Use contextlib.suppress instead of try-except-pass
   - Fix UP036 in demo.py: Remove outdated Python 2 version check (project requires Python 3.8+)

3. **Address Circular Dependency Risks** (Priority: HIGH)
   - Fix imports inside functions in detectors.py, last_error.py, runtime_config.py
   - Move imports to module level to prevent circular dependencies
   - Refactor module structure if needed to avoid circular imports

4. **Improve Test Coverage** (Priority: MEDIUM)
   - Current coverage: 77%
   - Target coverage: 85%+
   - Focus on untested modules: cli.py, setup_claude_code.py, self_test.py
   - Add tests for edge cases in core functionality


