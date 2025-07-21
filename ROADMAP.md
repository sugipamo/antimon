# antimon Development Roadmap

## Current Status (2025-07-21)

🎉 **Version 0.2.2 has been successfully completed!** 

### Recent Achievements:
- ✅ **Version 0.2.0**: Transformed into a proper Python package with comprehensive testing
- ✅ **Version 0.2.1**: Fixed detector functions and improved documentation  
- ✅ **Version 0.2.2**: Fixed critical user experience issues identified from testing
  - Exit codes now work correctly (0/1/2)
  - Output behavior matches README examples
  - Quiet mode properly shows security issues
  - Added validation for missing required fields
  - Test coverage improved to 87% (31 tests passing)

### Quality Check Summary (2025-07-21)
- ✅ **pytest**: All 52 tests passing with 78% code coverage (improved from 76%)
- ✅ **Project structure**: Clean working directory, proper .gitignore configuration (htmlcov and venv directories properly ignored)
- ✅ **src-check score**: 87.5/100 (🟡 Good)
  - Architecture: 85.0/100
  - Code quality: 88.0/100
  - Compliance: 94.0/100
  - Documentation: 88.0/100
  - Performance: 96.0/100
  - Security: 95.0/100
  - Testing: 92.0/100
  - Type safety: 92.0/100

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

### Code Quality Improvements from src-check (2025-07-21) 🔍
- [ ] **Print statements in core.py**: Currently using print() for user-facing output (65+ occurrences). This is intentional for CLI tool output, but consider structured logging for debugging
- [ ] **Reduce coupling in core.py, detectors.py, and color_utils.py**: High external call count (153, 51, and 52 respectively, max recommended: 15). Note: This is partly due to the nature of security detection requiring many patterns
- [ ] **Complex function refactoring**: process_stdin function has complexity of 42 (max recommended: 10). Consider breaking into smaller functions
- [x] **Add docstrings to test classes**: ✅ Added comprehensive docstrings to all test classes (2025-07-21)
- [ ] **Add docstrings to test functions**: Individual test functions still need docstrings (30+ test functions missing docstrings across test_cli.py, test_core.py, test_detectors.py)
- [ ] **Type hints improvement**: Missing return type hints for test functions and generic type parameters for dict types
- [ ] **Unused imports cleanup**: Several unused imports in __init__.py (intentionally re-exported for public API), test_cli.py, and self_test.py
- [x] **Optimize string concatenation in detectors.py**: ✅ Replaced string concatenation with list.join() pattern (2025-07-21)
- [ ] **Security concern in color_utils.py**: os.system() call detected (line 61) - Review for safer alternatives
- [ ] **Performance issues in color_utils.py**: Loop-invariant len() calls and string concatenation in loops (lines 143, 146)


### Version 0.2.2 ✅ COMPLETED (2025-07-21)

#### 完了したタスク ✅ (2025-07-21)
- [x] **テストクラスへのdocstring追加**: 全テストクラスに包括的なdocstringを追加し、テストの目的を明確化
- [x] **文字列連結の最適化**: detectors.pyでPERF003違反を修正し、パフォーマンスを改善
- [x] **Exit Code の修正**: 実際にはすでに正しく実装されていたことを確認（exit code 2 for security, 1 for errors, 0 for success）
- [x] **出力動作の統一**: READMEの例と一致するよう、安全な場合は無出力に修正
- [x] **Quiet Mode の改善**: `-q`オプション使用時もセキュリティ問題の詳細を表示するよう修正
- [x] **必須フィールドの検証**: Write/Editツールで必須フィールドが欠けている場合のエラー処理を追加
- [x] **包括的なCLIテストの追加**: 全ての修正に対するテストを追加し、テストカバレッジを87%に向上

### Version 0.2.3 ✅ COMPLETED (2025-07-21)

#### 完了したタスク ✅ (2025-07-21)
- [x] **--version オプションの確認**: バージョン0.2.2が正しく表示されることを確認
- [x] **--test コマンドの実装**: インストール後の動作確認用セルフテスト機能を追加（8つのテストケース）
- [x] **カラー出力のサポート**: エラー・警告・成功メッセージの視認性を向上
  - [x] ANSIカラーコードによる色分け（エラー：赤、警告：黄、成功：緑、情報：青）
  - [x] --no-colorオプションでCI/CD環境に対応
  - [x] Windows 10+でのカラーサポート
- [x] **検出結果の具体性向上**: 
  - [x] 行番号表示機能（Line 4: api_key = "sk-123..." のような形式）
  - [x] マッチしたコードのハイライト表示
- [x] **エラーメッセージの簡潔化**: 
  - [x] 通常モードでは正規表現パターンを非表示
  - [x] -vオプション使用時のみ技術的詳細を表示

### Version 0.2.4 ✅ COMPLETED (2025-07-21)

#### 実装完了したタスク ✅
- [x] **ReadとBashツールのセキュリティホール修正**: セキュリティ検証の抜け穴を塞ぎました
  - [x] `detect_read_sensitive_files`関数を実装し、機密ファイルへのアクセスを検出
  - [x] `detect_bash_dangerous_commands`関数を実装し、危険なコマンドを検出
  - [x] core.pyを更新してRead/Bashツールの検証を有効化
  - [x] 包括的なテストケースを追加（14個の新しいテスト）
  - [x] すべてのテストがパス（52個のテスト）

#### 検出可能になった脅威:
- **Readツール**: `/etc/shadow`, SSH秘密鍵, `.env`ファイル, AWSクレデンシャル等への不正アクセス
- **Bashツール**: `rm -rf /`, `curl | bash`, `sudo`権限昇格、暗号通貨マイナー等の実行防止

### Version 0.2.5 (Next Up) 🚀
次に実装予定のタスク:

#### src-check改善項目の対応
- [ ] **コード品質の向上** (src-check指摘事項)
  - [ ] テスト関数へのdocstring追加（30+関数）
  - [ ] 複雑な関数のリファクタリング（process_stdin関数のcomplexity: 35）
  - [ ] 型ヒントの改善（dict型のジェネリックパラメータ追加）
  - [ ] カラーユーティリティのパフォーマンス改善
  
#### ユーザー体験の改善
- [ ] **インストール後の体験向上**
  - [ ] `--first-run`オプションで対話的チュートリアル
  - [ ] `--check-setup`でClaude Code連携の確認
  - [ ] より実践的なQuick Startドキュメント


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
| 0.2.0 | ✅ Completed | Package structure |
| 0.2.1 | ✅ Completed | Bug fixes & README improvements |
| 0.2.2 | ✅ Completed | Critical fixes & user experience |
| 0.2.3 | ✅ Completed | Enhanced UX (colors, test command, better errors) |
| 0.2.4 | ✅ Completed | Security fixes (Read/Bash tools) |
| 0.2.5 | 2025 Q3 | Code quality & UX improvements |
| 0.3.0 | 2025 Q4 | Configuration |
| 0.4.0 | 2026 Q1 | Enhanced detection |
| 0.5.0 | 2026 Q2 | Integrations |
| 0.6.0 | 2026 Q3 | Performance |
| 0.7.0 | 2026 Q4 | Advanced features |
| 0.8.0 | 2027 Q1 | Enterprise features |
| 0.9.0 | 2027 Q2 | Performance & Scale |
| 1.0.0 | 2027 Q3 | Production ready |


## How to Contribute

1. Check the [Issues](https://github.com/yourusername/antimon/issues) for tasks
2. Fork the repository
3. Create a feature branch
4. Submit a pull request
5. Join our discussions

## Feedback

We welcome feedback and suggestions! Please open an issue or start a discussion to share your ideas for improving antimon.

