# antimon Development Roadmap

## Current Status (2025-07-21)

🎉 **Version 0.2.7 Major Features Completed!** 

### Recent Achievements:
- ✅ **Version 0.2.0**: Transformed into a proper Python package with comprehensive testing
- ✅ **Version 0.2.1**: Fixed detector functions and improved documentation  
- ✅ **Version 0.2.2**: Fixed critical user experience issues
- ✅ **Version 0.2.3**: Enhanced UX with colors, test command, and better errors
- ✅ **Version 0.2.4**: Security fixes for Read/Bash tools
- ✅ **Version 0.2.5**: Code quality improvements (refactoring, type hints)
- ✅ **Version 0.2.6**: User experience improvements (first-run guide, better errors, runtime config)
- ✅ **Version 0.2.7 (Partial)**: Critical improvements based on user feedback
  - ✅ Fixed `--allow-file` option to only skip filename detection while keeping other detectors active
  - ✅ Enhanced error messages with specific context and actionable suggestions
  - ✅ Improved detection transparency with detailed explanations in `--explain-last-error`

### Quality Check Summary (2025-07-21)
- ✅ **pytest**: All 98 tests passing with 82% code coverage  
- ✅ **Project structure**: Clean working directory, proper .gitignore configuration (cache files exist but are properly ignored)
- ✅ **src-check score**: 59.3/100 (🟠 Moderate - improvements needed)
  - Main issues: High use of print statements instead of logging, high coupling in several modules, missing type hints in some places
- ✅ **User Experience Review**: Comprehensive evaluation completed with actionable improvements identified

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

### Version 0.2.7 (In Progress) 🚀

#### 完了済みタスク ✅
- [x] **インストール体験の改善（部分的）**: 
  - [x] インストール完了後の自動セットアップウィザード ✅ (2025-07-21)
    - 実装内容: インタラクティブなセットアップウィザードを追加
    - `--setup` コマンドでいつでも実行可能
    - Claude Codeの自動検出と設定
    - セットアップの検証機能付き

#### 残りのタスク 📋

##### 1. グロブパターンサポート for `--allow-file` ✅ COMPLETED (2025-07-21)
- [x] ワイルドカードサポート（`*.env`, `config/*.json`）
- [x] 再帰的パターン（`**/*.secret`）
- [x] パスの正規化と展開
- [x] テストケースの追加
  - 実装内容: fnmatchとカスタム正規表現を使用してグロブパターンマッチングを実装
  - `is_file_allowed`メソッドを追加してグロブパターンサポートを提供
  - エンドツーエンドテストで動作確認済み

##### 2. 残りの実装項目
- [ ] プラットフォーム別の詳細なインストールガイド
- [ ] 依存関係の自動チェックと解決提案

### Version 0.2.8 (User Experience Enhancement) 🎯

#### ユーザー評価から判明した最優先改善項目 (2025-07-21 更新)

##### 1. 使用方法の明確化 🔴 CRITICAL
- [x] **動作確認コマンドの充実 (部分的)** ✅
- [ ] **残りの機能**:
  - [ ] 非対話的デモモード (`--demo --non-interactive`) - CI/CDでも使用可能
  - [ ] 実ファイルテスト機能 (`--check-file <path>`) - 実際のファイルでブロック判定を事前確認
  - [ ] テストコマンドの修正 - 失敗している2つのテストケースを修正
- [ ] **設定状態の可視化**:
  - [ ] `antimon --status` で現在の設定、有効な検出器、除外パターンを一覧表示
  - [ ] Claude Codeとの連携状態の確認機能
  - [ ] 最近の検出履歴の表示

##### 2. 操作の直感性向上 🟡 HIGH
- [ ] **簡潔なエラー表示**:
  - [ ] `--brief` オプションで簡潔なエラー表示モード
  - [ ] エラーメッセージの階層化（要約→詳細）
  - [ ] 詳細は `--explain-last-error` で確認する設計
- [ ] **誤検出時のワンステップ対処**:
  - [ ] 検出時に「このパターンを今後無視する？[Y/n]」の対話的選択
  - [ ] 選択結果をプロジェクト設定（.antimon/config）に自動保存
  - [ ] 除外設定の簡単な取り消し機能
- [ ] **コンテキスト対応の検出**:
  - [ ] テストファイル（*_test.py, test_*.py）での自動的な検出緩和
  - [ ] ドキュメント内のコード例での誤検出防止
  - [ ] 開発環境と本番環境の自動識別

##### 3. ログ出力の有用性向上 🟡 HIGH
- [ ] **構造化されたログ出力**:
  - [ ] JSON形式でのログ出力オプション（--format json）
  - [ ] 検出理由、リスクレベル、修正提案を構造化して表示
  - [ ] CI/CDツールとの統合を考慮したマシンリーダブルな出力
- [ ] **デバッグ情報の階層化**:
  - [ ] -v で基本情報、-vv で詳細、-vvv で完全トレース
  - [ ] 特定の検出器のみのデバッグ情報表示オプション
  - [ ] パフォーマンス計測情報の表示

##### 4. エラー時の明確な次のアクション 🟡 HIGH
- [ ] **FAQ/トラブルシューティングガイド**:
  - [ ] `--faq` コマンドで一般的な問題と解決策を表示
  - [ ] よくある誤検出パターンと対処法のドキュメント
  - [ ] エラーコードベースの解決策提示
- [ ] **対話的トラブルシューティング**:
  - [ ] エラー発生時に「次に何をすべきか」を番号付きリストで表示
  - [ ] 選択した番号に応じて自動的にコマンド実行や設定変更
  - [ ] よくあるエラーパターンのFAQへの自動マッチング
- [ ] **自己診断機能**:
  - [ ] `antimon --diagnose` で環境、設定、権限などを総合チェック
  - [ ] 問題が見つかった場合の具体的な解決コマンドの提示
  - [ ] 診断結果のレポート生成（サポート時に共有可能）

##### 5. 期待値との差異の解消 🟡 MEDIUM
- [ ] **設定テンプレート機能**:
  - [ ] `--generate-config` で設定ファイルのテンプレート生成
  - [ ] プロジェクトタイプ別の推奨設定（Web開発、データ分析、インフラなど）
  - [ ] 設定ファイルのバリデーション機能
- [ ] **動作の予測可能性向上**:
  - [ ] --dry-run モードでの事前確認機能
  - [ ] 検出ルールの一覧表示と各ルールの詳細説明
  - [ ] 「なぜこれが検出されたか」の詳細トレース表示
- [ ] **設定の透明性**:
  - [ ] 現在有効な全設定の出所を表示（デフォルト/環境変数/設定ファイル/コマンドライン）
  - [ ] 設定の優先順位の明確な説明
  - [ ] 設定変更のプレビュー機能

##### 6. その他の利便性向上 🟢 LOW
- [ ] **統計情報機能**:
  - [ ] `--stats` で検出統計を表示（どの検出器が最も頻繁に動作しているか）
  - [ ] プロジェクトごとの検出傾向分析
- [ ] **バッチ検証モード**:
  - [ ] 複数のファイルを一括でチェック
  - [ ] プロジェクト全体のセキュリティ監査に使用
  - [ ] 結果のエクスポート機能（CSV、JSON形式）

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

### Code Quality Improvements (from src-check - Score: 59.3/100)
- [ ] **High Priority**: Replace 200+ print statements with structured logging
- [ ] **High Priority**: Reduce coupling in core modules (core.py: 165, color_utils.py: 53, detectors.py: 78 external calls)
- [ ] **Security**: Address os.system() usage in color_utils.py:71
- [ ] **Architecture**: Resolve circular dependency warnings
- [ ] Clean up unused imports and complete missing type hints
- [ ] Optimize string concatenation in loops
- [ ] Reduce function complexity

## Long-term Goals

### Developer Experience
- [ ] IDE integration guides, hook debugging mode, performance profiling
- [ ] Custom rule creation, plugin API for extensions
- [ ] Internationalization (Japanese support, locale detection, localized docs)

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

## Next Steps (2025-07-21)

Based on the progress so far, the following tasks are recommended for the next work session:

### Immediate Priority (Version 0.2.8 continuation)
1. **Implement `antimon --status` command** - Show current configuration, enabled detectors, and exclusion patterns
2. **Add structured logging output** - Replace print statements with proper logging (addresses code quality issue)
3. **Implement dry-run mode** - Allow users to preview what would be detected without blocking

### Medium Priority
1. **Create interactive troubleshooting (`antimon --diagnose`)** - Self-diagnosis for environment and configuration issues
2. **Add JSON output format** - Machine-readable output for CI/CD integration
3. **Implement detection history** - Track and display recent detections



## Release Schedule

| Version | Target Date | Focus Area |
|---------|------------|------------|
| 0.2.7 | 2025 Q3 | Critical bug fixes & improvements (Complete) |
| 0.2.8 | 2025 Q3 | User Experience Enhancement (In Progress) |
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


