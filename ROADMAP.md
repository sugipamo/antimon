# antimon Development Roadmap

## Current Status (2025-07-21)

🎉 **Version 0.2.0 has been successfully completed!** The project has been transformed into a proper Python package with comprehensive testing, documentation, and code quality checks. All tests are passing (20/20) and the code quality score is 93.9/100.

### Quality Check Summary (2025-07-21)
- ✅ **pytest**: All 20 tests passing with 50% code coverage
- ✅ **Project structure**: Clean working directory, proper .gitignore configuration
- ✅ **src-check score**: 93.9/100 (🟢 Excellent)
  - Architecture: 92.0/100
  - Code quality: 94.0/100
  - Compliance: 95.0/100
  - Documentation: 90.0/100
  - Performance: 98.0/100
  - Testing: 94.0/100
  - Type safety: 94.0/100

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

### User Experience Improvements (ユーザー体験の改善)

#### 即時対応が必要な項目 (High Priority) ✅ COMPLETED
- [x] **Success feedback**: 検出されなかった場合に「No security issues detected」等の成功メッセージを表示
- [x] **Verbose mode fix**: -vオプションが正常に動作するように修正
- [x] **Help text improvement**: --helpで表示される説明をより具体的に（使用例の追加）
- [x] **Error message clarity**: エラーメッセージに対処法を含める
- [x] **Exit code behavior**: 非コード編集ツール（Read, Bashなど）の場合の明確なフィードバック

### Code Quality Improvements from src-check (2025-07-21) 🔍
- [ ] **Replace print statements with logging in core.py**: Currently using print() for output, should use proper logging
- [ ] **Reduce coupling in core.py and detectors.py**: High external call count
- [ ] **Add docstrings to test classes**: All test files missing docstrings
- [ ] **Optimize string concatenation in detectors.py**: Use list.append() and join() instead of += in loops


### Version 0.2.2 (Next Priority Tasks) 🚀
次に実装予定のタスク（2025-07-21 更新）:

#### 1. ログ出力の改善 🔧
- [ ] **Quiet mode (-q/--quiet)**: エラーのみを表示し、成功時は何も出力しないモード
- [ ] **Summary at end**: 全検出器の実行結果サマリー（例：「6 detectors run, 1 issue found」）
- [ ] **Structured logging**: 検出結果を構造化して表示（検出器名、ファイルパス、行番号など）
- [ ] **Log format simplification**: タイムスタンプをシンプルに（現在：2025-07-21 10:14:33 → 10:14:33）
- [ ] **Log level visibility**: DEBUGログとINFO/WARNINGログの視覚的差別化

#### 2. インストールと初回使用の体験向上 📦
- [ ] **Installation verification**: インストール後の動作確認コマンド（antimon --version、antimon --test）
- [ ] **Quick test command**: サンプルデータで即座に動作確認できるコマンド（antimon --demo）
- [ ] **README examples**: コピペで試せる実例を3-5個追加
- [ ] **Common errors section**: よくあるエラーと解決方法のセクション

#### 3. 開発者向け機能 👨‍💻
- [ ] **JSON output mode**: CI/CD統合のためのJSON形式出力（--output-format json）
- [ ] **Debug output**: 内部処理の詳細を出力するデバッグモード（--debug）
- [ ] **Dry-run mode**: 実際の検証を行わず、何がチェックされるかを表示するモード
- [ ] **Hook test mode**: フック設定のテストモード（実際のAIツールなしで動作確認）

#### 4. 検出結果の理解しやすさ 📊
- [ ] **Detection context**: なぜ危険なのかの簡潔な説明
- [ ] **Severity levels**: 検出の深刻度表示（Critical/High/Medium/Low）
- [ ] **Fix suggestions**: 検出された問題の修正方法の提案
- [ ] **Whitelist instructions**: 誤検出の場合の除外方法の案内

#### 5. テストの改善（t-wada推奨形式） 🧪
- [ ] **Test docstrings**: テストクラスにdocstringを追加して目的を明確化
- [ ] **Parameterized tests**: 類似のテストケースを@pytest.mark.parametrizeで効率化
- [ ] **Edge case tests**: 空の入力、不正な形式、境界値のテストを追加

#### 6. ドキュメントの充実 📚
- [ ] **Troubleshooting guide**: よくある問題と解決方法
- [ ] **Integration examples**: Claude Code以外のツールとの統合例
- [ ] **Configuration guide**: 将来の設定ファイル機能の使い方（v0.3.0向け）
- [ ] **API documentation**: Pythonモジュールとして使用する際のAPIドキュメント


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

## Version 1.0.0 (Production Ready)
- [ ] Comprehensive documentation
- [ ] 100% test coverage
- [ ] Performance benchmarks
- [ ] Security audit
- [ ] Stable API guarantee
- [ ] Enterprise features:
  - [ ] LDAP/SSO integration
  - [ ] Audit logging
  - [ ] Role-based access control
  - [ ] Multi-tenancy support

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
| 0.2.2 | 2025 Q3 | User experience & logging |
| 0.3.0 | 2025 Q4 | Configuration |
| 0.4.0 | 2026 Q1 | Enhanced detection |
| 0.5.0 | 2026 Q2 | Integrations |
| 0.6.0 | 2026 Q3 | Performance |
| 0.7.0 | 2026 Q4 | Advanced features |
| 1.0.0 | 2027 Q1 | Production ready |

## How to Contribute

1. Check the [Issues](https://github.com/yourusername/antimon/issues) for tasks
2. Fork the repository
3. Create a feature branch
4. Submit a pull request
5. Join our discussions

## Feedback

We welcome feedback and suggestions! Please open an issue or start a discussion to share your ideas for improving antimon.