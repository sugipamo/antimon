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
- ✅ **pytest**: All 84 tests passing with 81% code coverage  
- ✅ **Project structure**: Clean working directory, proper .gitignore configuration
- ✅ **src-check score**: 68.1/100 (🟠 Moderate - some improvements needed)
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

#### ユーザビリティの改善
- [x] **インストール体験の改善**: 
  - [x] インストール完了後の自動セットアップウィザード ✅ (2025-07-21)
    - 実装内容: インタラクティブなセットアップウィザードを追加
    - `--setup` コマンドでいつでも実行可能
    - Claude Codeの自動検出と設定
    - セットアップの検証機能付き
  - [ ] プラットフォーム別の詳細なインストールガイド
  - [ ] 依存関係の自動チェックと解決提案
- [ ] **検出結果の視覚的改善**:
  - [ ] 検出箇所のコードハイライト表示
  - [ ] 問題の深刻度レベルの視覚的表示（色分け・アイコン）
  - [ ] 検出パターンの説明を日本語でも表示するオプション
- [ ] **誤検出への対処改善**:
  - [ ] 誤検出報告の簡易化（--report-false-positive コマンド）
  - [ ] プロジェクト固有の除外設定の永続化
  - [ ] 一時的な無効化の履歴管理
- [ ] **デバッグサポートの強化**:
  - [ ] --dry-run モード（実際にブロックせずに検出結果を表示）
  - [ ] 検出ロジックの詳細トレース機能
  - [ ] 過去の検出履歴の参照機能



### Next Priority Tasks for Version 0.2.7

#### グロブパターンサポート for `--allow-file` 🚀
- [ ] ワイルドカードサポート（`*.env`, `config/*.json`）
- [ ] 再帰的パターン（`**/*.secret`）
- [ ] パスの正規化と展開
- [ ] テストケースの追加

#### インストール体験の改善（残り項目）
- [ ] プラットフォーム別の詳細なインストールガイド
- [ ] 依存関係の自動チェックと解決提案

#### 検出結果の視覚的改善
- [ ] 検出箇所のコードハイライト表示
- [ ] 問題の深刻度レベルの視覚的表示（色分け・アイコン）
- [ ] 検出パターンの説明を日本語でも表示するオプション

#### 誤検出への対処改善
- [ ] 誤検出報告の簡易化（--report-false-positive コマンド）
- [ ] プロジェクト固有の除外設定の永続化
- [ ] 一時的な無効化の履歴管理

#### デバッグサポートの強化
- [ ] --dry-run モード（実際にブロックせずに検出結果を表示）
- [ ] 検出ロジックの詳細トレース機能
- [ ] 過去の検出履歴の参照機能

### Version 0.2.8 (User Experience Enhancement) 🎯

#### ユーザー評価から判明した最優先改善項目 (2025-07-21)

##### 1. 使用方法の明確化 🔴 CRITICAL
- [ ] **動作確認コマンドの充実**:
  - [ ] `antimon --demo` で様々なパターンの検出例を対話的に表示
  - [ ] 検出される/されないケースの明確な例示
  - [ ] ユーザーの実際のコードで試せるサンドボックスモード
- [ ] **設定状態の可視化**:
  - [ ] `antimon --status` で現在の設定、有効な検出器、除外パターンを一覧表示
  - [ ] Claude Codeとの連携状態の確認機能
  - [ ] 最近の検出履歴の表示

##### 2. 操作の直感性向上 🟡 HIGH
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
- [ ] **対話的トラブルシューティング**:
  - [ ] エラー発生時に「次に何をすべきか」を番号付きリストで表示
  - [ ] 選択した番号に応じて自動的にコマンド実行や設定変更
  - [ ] よくあるエラーパターンのFAQへの自動マッチング
- [ ] **自己診断機能**:
  - [ ] `antimon --diagnose` で環境、設定、権限などを総合チェック
  - [ ] 問題が見つかった場合の具体的な解決コマンドの提示
  - [ ] 診断結果のレポート生成（サポート時に共有可能）

##### 5. 期待値との差異の解消 🟡 MEDIUM
- [ ] **動作の予測可能性向上**:
  - [ ] --dry-run モードでの事前確認機能
  - [ ] 検出ルールの一覧表示と各ルールの詳細説明
  - [ ] 「なぜこれが検出されたか」の詳細トレース表示
- [ ] **設定の透明性**:
  - [ ] 現在有効な全設定の出所を表示（デフォルト/環境変数/設定ファイル/コマンドライン）
  - [ ] 設定の優先順位の明確な説明
  - [ ] 設定変更のプレビュー機能

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

### Code Quality Improvements (from src-check)
- [ ] Consider structured logging for debugging (200+ print statements currently)
- [ ] Reduce coupling in core modules
- [ ] Clean up unused imports
- [ ] Address os.system() security concern in color_utils.py:71
- [ ] Resolve circular dependency concerns
- [ ] Complete type hints and documentation
- [ ] Optimize string concatenation performance

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

## Release Schedule

| Version | Target Date | Focus Area |
|---------|------------|------------|
| 0.2.7 | 2025 Q3 | Critical bug fixes & improvements (Partial Complete) |
| 0.2.8 | 2025 Q3 | User Experience Enhancement |
| 0.3.0 | 2025 Q4 | Configuration |
| 0.4.0 | 2026 Q1 | Enhanced detection |
| 0.5.0 | 2026 Q2 | Integrations |
| 1.0.0 | 2027 Q3 | Production ready |




## User Journey & Pain Points

### Current User Experience (2025-07-21)

**Installation**: Simple pip/uv install, welcome message, interactive setup, but unclear initial verification and detection patterns

**Initial Setup**: Auto Claude Code integration, test commands work, but complex project configuration and unclear verification

**Daily Use**: Clear errors, colorful output, detailed explanations, but cumbersome false positive handling and undocumented debug mode

**Troubleshooting**: Detailed error info, helpful guidance, but long resolution paths and no detection history

### Key Challenges from User Feedback

1. **Usage Clarity**: Unclear practical usage, detection pattern overview, project-specific configuration
2. **Operational Complexity**: Repetitive long options, unclear persistence, no batch checking
3. **Log Output**: Abstract detection reasons, insufficient debug info, no CI/CD format
4. **Error Resolution**: Unclear next steps, trial-and-error troubleshooting, ambiguous issue sources

### Ideal User Experience

- **Zero-friction setup**: Auto-suggest optimal config, recognize project type
- **Intelligent detection**: Context awareness, test vs production code, learn project conventions
- **Instant resolution**: One-click false positive handling, concrete fixes, auto-recognize similar cases
- **Continuous improvement**: Usage-based accuracy, community feedback integration, personalized experience

## How to Contribute

1. Check the [Issues](https://github.com/yourusername/antimon/issues) for tasks
2. Fork the repository
3. Create a feature branch
4. Submit a pull request
5. Join our discussions

## Feedback

We welcome feedback and suggestions! Please open an issue or start a discussion to share your ideas for improving antimon.

