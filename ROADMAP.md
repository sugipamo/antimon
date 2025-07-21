# antimon Development Roadmap

## Current Status (2025-07-21)

🎉 **Version 0.2.2 has been successfully completed!** 

### Recent Achievements:
- ✅ **Version 0.2.0**: Transformed into a proper Python package with comprehensive testing
- ✅ **Version 0.2.1**: Fixed detector functions and improved documentation  
- ✅ **Version 0.2.2**: Fixed critical user experience issues
- ✅ **Version 0.2.3**: Enhanced UX with colors, test command, and better errors
- ✅ **Version 0.2.4**: Security fixes for Read/Bash tools
- ✅ **Version 0.2.5**: Code quality improvements (refactoring, type hints)

### Quality Check Summary (2025-07-21)
- ✅ **pytest**: All 52 tests passing with 87% code coverage
- ✅ **Project structure**: Clean working directory, proper .gitignore configuration
- ✅ **src-check score**: 88.4/100 (🟡 Good)

## Project Vision

Transform antimon from a standalone script into a robust, extensible Python package that can be easily integrated into various AI coding assistant workflows and CI/CD pipelines.

## Version 0.1.0 (Initial Release) ✓
- [x] Basic hook functionality for Claude Code
- [x] Core detection patterns (files, APIs, Docker, localhost)
- [x] Claude-based anti-pattern detection
- [x] JSON input processing
- [x] Error output formatting

## Version 0.2.0 (Package Structure) ✅ COMPLETED (2025-07-21)
- [x] Convert to proper Python package structure
  - [x] `src/antimon/` directory structure
  - [x] `__init__.py` with public API
  - [x] Separate modules for each detector
  - [x] `cli.py` for command-line interface
- [x] Add `pyproject.toml` with proper metadata
- [x] Create entry point for `antimon` command
- [x] Add comprehensive docstrings
- [x] Type hints for all functions
- [x] Basic unit tests
- [x] Fixed LLM API detection for import statements
- [x] Code quality checks (ruff, mypy, black)
- [x] Updated .gitignore for Python projects

### Version 0.2.1 (Bug Fixes & Improvements) ✅ COMPLETED (2025-07-21)
- [x] Fix detector functions to check both 'content' and 'new_string' fields
- [x] Add tests for Edit/MultiEdit tool support
- [x] Update README with better examples and documentation

### Remaining Code Quality Items from src-check 🔍
- [ ] **Print statements in core.py**: Currently using print() for user-facing output (65+ occurrences). This is intentional for CLI tool output, but consider structured logging for debugging
- [ ] **Reduce coupling**: High external call count in core.py, detectors.py, and color_utils.py
- [ ] **Unused imports cleanup**: Several unused imports (some intentionally re-exported for public API)
- [ ] **Security concern in color_utils.py**: os.system() call for Windows ANSI enablement







### Version 0.2.6 (Next Up) 🚀

#### ユーザー体験の改善
- [ ] **初回使用時のガイド改善**: インストール後のメッセージ、quickstartコマンド、Claude Code連携の自動設定
- [ ] **エラーメッセージの実用性向上**: コンテキスト表示、具体的な修正提案、FAQリンク
- [ ] **設定ファイルなしでのカスタマイズ**: --ignore-pattern、--allow-file、環境変数サポート
- [ ] **実際の使用フローの改善**: ブロック時の対処法表示、--explain-last-error機能


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

## Version 0.6.0 (Performance & Reliability)
- [ ] Async detection for better performance
- [ ] Caching mechanism for repeated checks
- [ ] Batch processing support
- [ ] Memory-efficient large file handling
- [ ] Retry mechanism for Claude API calls
- [ ] Offline mode with cached patterns
- [ ] Progress indicators for long operations

## Version 0.7.0 (Advanced Features)
- [ ] Machine learning-based pattern detection
- [ ] Context-aware analysis
- [ ] Dependency scanning integration
- [ ] License compliance checking
- [ ] Metrics and statistics dashboard
- [ ] Historical trend analysis
- [ ] Team collaboration features

## Version 0.8.0 (Enterprise Features)
- [ ] Enterprise-ready features:
  - [ ] LDAP/SSO integration
  - [ ] Audit logging
  - [ ] Role-based access control
  - [ ] Multi-tenancy support
  - [ ] Compliance reporting (SOC2, ISO27001)

## Version 0.9.0 (Performance & Scale)
- [ ] Large-scale deployment optimizations
- [ ] Distributed scanning support
- [ ] Result caching and deduplication
- [ ] Webhook integrations
- [ ] REST API for programmatic access

## Version 1.0.0 (Production Ready)
- [ ] Comprehensive documentation
- [ ] 100% test coverage
- [ ] Performance benchmarks
- [ ] Security audit
- [ ] Stable API guarantee
- [ ] Long-term support (LTS) commitment
- [ ] Migration guides from other tools
- [ ] Professional support options


## Long-term Goals

### Developer Experience
- [ ] **IDE Integration Guide**: 各IDEでの設定方法の詳細ドキュメント
- [ ] **Hook debugging mode**: フックの動作をデバッグするための詳細ログモード
- [ ] **Performance profiling**: 大規模プロジェクトでのパフォーマンス計測とボトルネック表示
- [ ] **Rule customization**: カスタムルールの作成と管理機能
- [ ] **API for extensions**: サードパーティ拡張のためのプラグインAPI
- [ ] **Learning mode**: 誤検出を学習し、プロジェクト固有のルールを生成

### Advanced User Experience
- [ ] **Interactive mode**: 検出時に「続行しますか？」の確認プロンプト
- [ ] **Context display**: 検出箇所の前後のコードを表示
- [ ] **Detection history**: 過去の検出履歴を記録
- [ ] **Real-time feedback**: リアルタイムで検証結果を表示
- [ ] **Visual indicators**: ターミナルでの色分けやアイコン
- [ ] **Smart defaults**: プロジェクトタイプに応じた設定
- [ ] **Telemetry opt-in**: 使用状況収集（ユーザー同意制）

### Internationalization
- [ ] **Japanese support**: 日本語のエラーメッセージとヘルプ
- [ ] **Locale detection**: 自動言語選択
- [ ] **Language selection**: --lang オプション
- [ ] **Localized docs**: 各言語でのドキュメント

### Community Building
- [ ] Create antimon organization on GitHub
- [ ] Establish contribution guidelines
- [ ] Set up community forum/Discord
- [ ] Regular security pattern updates
- [ ] Community-contributed detection rules

### Ecosystem Integration
- [ ] IntelliJ IDEA plugin
- [ ] Sublime Text package
- [ ] Vim/Neovim plugin
- [ ] Emacs package
- [ ] Jenkins plugin
- [ ] CircleCI orb
- [ ] Terraform provider

### Research & Innovation
- [ ] AI-powered code review suggestions
- [ ] Automated fix generation
- [ ] Cross-repository pattern learning
- [ ] Real-time collaboration features
- [ ] Quantum-resistant cryptography patterns

## Release Schedule

| Version | Target Date | Focus Area |
|---------|------------|------------|
| 0.2.6 | 2025 Q3 | User experience improvements |
| 0.3.0 | 2025 Q4 | Configuration |
| 0.4.0 | 2026 Q1 | Enhanced detection |
| 0.5.0 | 2026 Q2 | Integrations |
| 1.0.0 | 2027 Q3 | Production ready |


## How to Contribute

1. Check the [Issues](https://github.com/yourusername/antimon/issues) for tasks
2. Fork the repository
3. Create a feature branch
4. Submit a pull request
5. Join our discussions

## Feedback

We welcome feedback and suggestions! Please open an issue or start a discussion to share your ideas for improving antimon.

