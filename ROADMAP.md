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

### Version 0.2.12 (User Experience) - COMPLETED (2025-07-22)

#### Completed:
- [x] Success message improvements (show what was checked)
- [x] Fixed duplicate output bug in verbose mode
- [x] Implemented --version flag properly
- [x] Enhanced --stats flag with meaningful statistics
- [x] Fixed JSON error handling
- [x] Standardized output streams
- [x] Fixed quickstart message behavior

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

## Next Immediate Tasks

### Version 0.2.13 (Batch Processing & JSON):
1. **Batch File Checking**: `antimon --check-files "src/**/*.py"` with progress indicators
2. **JSON Output Format**: `--output-format json` for CI/CD integration
3. **Brief Mode**: `--brief` for concise security reports
4. **Exit Code Documentation**: Show meaning in error messages
5. **Watch Mode**: `antimon --watch <directory>` for continuous monitoring
6. **Pattern Testing**: `antimon --test-pattern <pattern>` to test detection patterns
7. **Auto-fix Suggestions**: Provide code snippets for common security fixes
8. **Error Recovery Hints**: Always show `--explain-last-error` hint on security detections
9. **Setup Status on First Run**: Show Claude Code integration status on initial execution

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

### 📝 Additional User Experience Findings (2025-07-22)

From hands-on testing with real scenarios, additional insights have been identified:

#### 1. **初回利用時の情報提供**
- 現状: `--status`で必要な情報は確認できるが、初回利用時にClaude Codeとの連携状態が分かりにくい
- 改善案: 初回実行時に簡単なセットアップ状態を表示（Claude Code連携、有効なdetector等）

#### 2. **エラー時の回復方法の明確化**
- 現状: `--explain-last-error`は詳細で素晴らしいが、存在を知らないと使えない
- 改善案: エラー発生時に「詳細は`antimon --explain-last-error`で確認」を常に表示

#### 3. **日本語対応（国際化）**
- 現状: 英語のみ対応
- 改善案: エラーメッセージとヘルプの多言語対応（特に日本語）

#### 4. **設定ファイルのサンプル提供**
- 現状: v0.3.0で設定ファイル対応予定だが、どのような設定が可能か不明
- 改善案: `--generate-config`で設定ファイルのテンプレート生成機能

#### 5. **プロジェクト固有の除外設定**
- 現状: `--allow-file`や`--ignore-pattern`はコマンドライン引数のみ
- 改善案: `.antimonignore`ファイルでプロジェクト固有の設定を永続化

#### 6. **CI/CD環境での利用ガイド**
- 現状: README.mdに基本的な例はあるが、実践的なCI/CDテンプレートがない
- 改善案: GitHub Actions、GitLab CI、Jenkins等の設定テンプレート提供

#### 7. **チーム開発での共有設定**
- 現状: 各開発者が個別に設定する必要がある
- 改善案: プロジェクトルートの`antimon.toml`で共有設定、個人設定の上書き機能

#### 8. **検出パターンの透明性**
- 現状: どのようなパターンで検出されるか内部実装を見ないと分からない
- 改善案: `--list-patterns`で現在有効な検出パターンを表示

#### 9. **誤検知の報告フロー**
- 現状: GitHubのissueで報告するよう案内されているが、フォーマットが不明
- 改善案: `--report-false-positive`で必要な情報を収集してissueテンプレートを生成

#### 10. **統計情報の活用**
- 現状: `--stats`で統計情報が見られるが、履歴が残らない
- 改善案: 検出履歴をローカルに保存し、傾向分析やレポート生成機能

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

### 🎯 Solutions by Priority



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


