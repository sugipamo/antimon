# antimon Development Roadmap

## Current Status (2025-07-22)

### Recent Achievements:
- ✅ **v0.2.12 (In Progress)**: Enhanced success messages showing detailed information about what was checked
- ✅ **v0.2.11**: Fixed exit codes (0=success, 1=error, 2=security issue) and comprehensive FAQ documentation
- ✅ **v0.2.10**: Verified `--quickstart`, `--stats`, and `--config` functionality
- ✅ **v0.2.1-v0.2.8**: Core features including detector fixes, direct file checking, Claude Code integration, and structured logging

### Quality Check Summary:
- ✅ **pytest**: 140/140 tests passing (74% code coverage) - All tests are stable
- ✅ **ruff**: All style issues fixed
- ⚠️ **mypy**: 81 type errors remaining (future version)
- ⚠️ **src-check**: Score 49.9/100 - See "Code Quality Improvements" section for detailed issues

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

### Version 0.2.13 (Batch Processing & JSON) - IN PROGRESS

#### Completed (2025-07-22):
- [x] **Batch File Checking**: `antimon --check-files "src/**/*.py"` with progress indicators
- [x] **JSON Output Format**: `--output-format json` for CI/CD integration

#### TODO:
- [ ] **Brief Mode**: `--brief` for concise security reports
- [ ] **Exit Code Documentation**: Show meaning in error messages
- [ ] **Watch Mode**: `antimon --watch <directory>` for continuous monitoring
- [ ] **Pattern Testing**: `antimon --test-pattern <pattern>` to test detection patterns
- [ ] **Auto-fix Suggestions**: Provide code snippets for common security fixes
- [ ] **Error Recovery Hints**: Always show `--explain-last-error` hint on security detections
- [ ] **Setup Status on First Run**: Show Claude Code integration status on initial execution

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

### Version 0.2.13 (Batch Processing & JSON) - Remaining Tasks:
3. **Brief Mode**: `--brief` for concise security reports
4. **Exit Code Documentation**: Show meaning in error messages 
5. **Error Recovery Hints**: Always show `--explain-last-error` hint on security detections

### Version 0.2.14 (Developer Tools):
1. **Watch Mode**: `antimon --watch <directory>` for continuous monitoring
2. **Pattern Testing**: `antimon --test-pattern <pattern>` to test detection patterns
3. **Auto-fix Suggestions**: Provide code snippets for common security fixes
4. **Setup Status on First Run**: Show Claude Code integration status on initial execution

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
| 0.2.12 | Released | User Experience | ✅ Completed |
| 0.2.13 | 2025-08-15 | Batch Processing & JSON | 🚧 Next Release |
| 0.3.0 | 2025-10-01 | Configuration | 📋 Planned |
| 0.4.0 | 2026-01-15 | Enhanced detection | 📋 Planned |
| 0.5.0 | 2026-04-01 | Integrations | 📋 Planned |
| 1.0.0 | 2027-07-01 | Production ready | 🎯 Goal |



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

### 🔍 Critical User Experience Observations

#### 1. **Onboarding Experience**
- **現状**: 初回実行時のガイダンスは存在するが、Claude Codeとの連携状態が不明確
- **問題点**: ユーザーは`antimon`をインストール後、実際に動作しているか確認する方法が分かりにくい
- **改善案**: 
  - 初回実行時に自動的に`--status`相当の情報を表示
  - Claude Code連携の有無と設定方法を明示
  - `--test`の実行を促すメッセージを追加

#### 2. **Error Message Clarity**
- **現状**: エラーメッセージは詳細だが、次のアクションが不明確
- **問題点**: `--explain-last-error`の存在を知らないユーザーが多い
- **改善案**:
  - すべてのセキュリティ検出メッセージに「詳細: antimon --explain-last-error」を追加
  - 誤検知の場合の対処法を1行で提示
  - よく使うオプション（`--allow-file`, `--dry-run`）を提案

#### 3. **Pattern Visibility**
- **現状**: どのようなパターンで検出されるかがブラックボックス
- **問題点**: 誤検知を避けるためにどうコードを書けばよいか分からない
- **改善案**:
  - `--list-patterns`で全検出パターンを表示
  - 各パターンに対する回避方法の例を提供
  - `--test-pattern`でカスタムパターンのテスト機能

#### 4. **Team Collaboration**
- **現状**: 個人単位での設定のみ可能
- **問題点**: チーム全体で同じ除外設定を共有できない
- **改善案**:
  - `.antimonignore`ファイルのサポート（`.gitignore`形式）
  - プロジェクトルートの`antimon.toml`での共有設定
  - 設定の優先順位: CLI引数 > ローカル設定 > プロジェクト設定 > グローバル設定

#### 5. **False Positive Management**
- **現状**: コマンドライン引数での一時的な除外のみ
- **問題点**: 毎回同じ引数を指定する必要がある
- **改善案**:
  - 検出時に「この検出を永続的に無視: antimon --add-ignore <pattern>」を表示
  - `--report-false-positive`でGitHub issueテンプレートを自動生成
  - よくある誤検知パターンのFAQを`--help-false-positives`で提供

### 🌟 What's Working Well
- **Error Messages**: Exceptionally clear with risks, fixes, and best practices
- **Demo Mode**: Excellent educational tool with 10 practical scenarios
- **Help System**: Well-organized with `--help`, `--quickstart`, `--help-errors`
- **Success Feedback**: Shows useful info (file size, checks performed) - Enhanced in v0.2.12
- **Multiple Input Modes**: Flexible with files, content, and JSON


### 📊 Key Usage Patterns
- Primary use: Direct file checking (`--check-file`)
- JSON mode rarely used outside of CI/CD
- Users expect proper exit codes for automation
- Verbose mode used for debugging false positives
- Dry-run mode helpful for testing

### 🛠️ Developer Experience Enhancements

#### 1. **Integration with Development Workflow**
- **Shell Aliases**: Provide recommended aliases in documentation
  ```bash
  alias amon='antimon --check-file'
  alias amon-watch='antimon --watch .'
  alias amon-fix='antimon --check-file --auto-fix'
  ```
- **Git Hooks**: Pre-commit hook template that runs antimon on staged files
- **Editor Integration**: VS Code extension that shows antimon status in status bar

#### 2. **Learning and Education**
- **Interactive Tutorial**: `antimon --tutorial` with step-by-step security lessons
- **Pattern Playground**: `antimon --playground` to test patterns interactively
- **Security Best Practices**: `antimon --best-practices <topic>` for language-specific guidance

#### 3. **Performance and Efficiency**
- **Incremental Checking**: Only check changed files in watch mode
- **Parallel Processing**: Use multiple cores for batch file checking
- **Caching**: Cache results for unchanged files to speed up repeated runs

#### 4. **Debugging and Troubleshooting**
- **Debug Mode**: `antimon --debug` to show detailed detector execution
- **Pattern Match Visualization**: Show exactly what matched in the code
- **Performance Profiling**: `antimon --profile` to identify slow detectors


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


