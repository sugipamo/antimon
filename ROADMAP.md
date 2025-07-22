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

### Quality Check Summary (2025-07-22)
- ✅ **pytest**: 119/119 tests passing! (75% code coverage)
  - Fixed: UnboundLocalError in core.py:472 - properly initialized 'config' variable
  - All tests are now passing
- ⚠️ **Code quality tools**: Improvements made, some issues remain
  - ruff: 59 errors remaining (475 fixed automatically)
  - mypy: 82 type errors (to be addressed)
  - src-check: Score 62.2/100 🟠 (56 issues: 10 high, 43 medium, 3 low)
    - Main issues: High coupling, unused imports, print statements instead of logging
    - Security concerns: Usage of input() and os.system()
    - Architecture score: 58/100 (needs improvement)

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


## ✅ Critical Fixes Completed (Version 0.2.9-hotfix)

### 1. **Fix failing tests** ✅ COMPLETED
- [x] Fixed UnboundLocalError in core.py:472 - properly initialized 'config' variable
- [x] Fixed direct file/content checking functionality
- [x] All 119 tests now pass!

### 2. **Code Quality** 🟠 IN PROGRESS
- [x] Run `ruff check --fix src/` (475 auto-fixable issues fixed)
- [ ] Fix remaining ruff issues (59 manual fixes)
- [ ] Add missing type annotations (82 mypy errors)




### Version 0.2.9 (User Experience Polish) ✅ MOSTLY COMPLETED

#### Completed Features:
- [x] GitHub URL fixes in README
- [x] dry-run mode documentation  
- [x] Success feedback messages
- [x] Claude Code installation guidance
- [x] Configuration file clarification
- [x] `--explain-last-error` command with detailed explanations
- [x] `--help-errors` command for troubleshooting guidance
- [x] Non-interactive demo mode with 10 clear examples
- [x] Enhanced error messages with specific fix suggestions

#### Remaining Tasks (moved to v0.2.10):
- [ ] Multiple file check progress display
- [ ] Interactive tutorial mode
- [ ] Step-by-step configuration guide  
- [ ] Staged error messages (simple → detailed → tutorial)
- [ ] First-run experience improvements
- [ ] FAQ integration in error messages

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


## User Experience Feedback (2025-07-22)

### 📝 ユーザー視点からの改善要望

#### 1. **初期導入時のユーザビリティ** (Priority: High)
- ✅ `--help`コマンドは充実しており、オプションの説明が明確
- ✅ Non-interactive demoは10個の具体例があり非常に分かりやすい
- ⚠️ **改善点**: 初回実行時のクイックスタートガイドへの誘導
  - 初めて実行した際に「--quickstart」オプションの存在を知らせる
  - または初回実行時に自動的にクイックスタートを表示

#### 2. **エラーメッセージの分かりやすさ** (Priority: High)
- ✅ セキュリティ検出時のメッセージは詳細で、具体的な修正方法も提示
- ✅ `--explain-last-error`で詳細な説明が見られる
- ✅ Dry-runモードでの出力が分かりやすい
- ⚠️ **改善点**: エラー時の次のアクションをより明確に
  - 例: "このエラーを回避するには --allow-file オプションを使用してください"

#### 3. **ログ出力の有用性** (Priority: Medium)
- ✅ 検出内容は明確で、リスクと修正方法が表示される
- ⚠️ **改善点**: 
  - 成功時のフィードバックをもう少し詳しく（何を検査したか）
  - `--verbose`モードでの出力例をヘルプに追加
  - 複数ファイル検査時の進捗表示

#### 4. **問題発生時のトラブルシューティング** (Priority: High)
- ✅ `--help-errors`コマンドで基本的な対処法は分かる
- ✅ `--explain-last-error`で詳細な説明が得られる
- ⚠️ **改善点**:
  - よくある質問（FAQ）へのリンクをエラーメッセージに含める
  - 誤検知の報告方法をより目立つように表示
  - Claude Code未インストール時の具体的なインストール手順

#### 5. **Claude Codeとの統合設定** (Priority: Medium)
- ✅ `--setup-claude-code`オプションが用意されている
- ⚠️ **改善点**:
  - Claude Code未インストール時により詳しいガイドを表示
  - 設定完了後の動作確認方法を明示
  - 設定のバックアップ/復元方法の説明

## Project Maintenance Notes (2025-07-22)

### Current Project Health:
- ✅ All tests passing (119/119) with 75% coverage
- ✅ No build/dist directories present (clean repository)
- ✅ Project structure follows Python best practices
- ⚠️ Cache directories present but normal for development:
  - `.pytest_cache`, `.mypy_cache`, `.ruff_cache` (can be cleaned if needed)
  - `__pycache__` directories (automatically managed by Python)

### Recommended Improvements:
1. **Code Quality** (Priority: High)
   - Fix unused imports in `__init__.py` (main src-check issue)
   - Replace print statements with proper logging
   - Reduce coupling between modules (architecture score: 58/100)
   - Fix ruff whitespace issues (mostly W293 - blank lines with whitespace)
   
2. **Security** (Priority: Medium)
   - Review usage of `input()` and `os.system()` for security implications
   - Consider using subprocess.run() instead of os.system()
   - Note: These are used in demo/interactive features, which is acceptable

3. **Type Safety** (Priority: Medium)
   - Add missing type annotations (82 mypy errors)
   - Enable stricter mypy configuration once fixed
   - Most errors are missing type parameters for generics (dict → Dict[str, Any])

### Project Compatibility Considerations:
Given that antimon is a security validation tool:
- The use of `input()` in demo/interactive modes is appropriate
- Some src-check warnings about security functions are false positives due to the nature of the project
- The architecture score (58/100) reflects the tool's need to inspect various data formats
- Print statements in CLI output are intentional for user feedback

## Next Steps

🎯 **Immediate** (2025-07-22) - User Experience Improvements:
   - 初回実行時のクイックスタートガイド自動表示
   - エラーメッセージに具体的な回避オプションを追加
   - 成功時の詳細フィードバック実装
   - Claude Code未インストール時の詳細なインストールガイド

🎯 **Code Quality** (2025-07-22) - Technical Improvements:
   - Fix remaining 59 ruff issues
   - Address 82 mypy type errors
   - Improve src-check score from 62.2/100 to at least 80/100

🎯 **Version 0.2.10** (Beginner-friendly features) - Next implementation:
   - Interactive tutorial mode（対話的チュートリアル）
   - Batch file checking with progress display（進捗表示付き複数ファイル検査）
   - Staged error messages（段階的エラーメッセージ）
   - FAQ integration in error messages（エラーメッセージへのFAQ統合）
   - Verbose mode examples in help（verboseモードの使用例追加）

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


