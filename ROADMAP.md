# antimon Development Roadmap

## Current Status (2025-07-21)

🎉 **Version 0.2.6 has been successfully completed!** 

### Recent Achievements:
- ✅ **Version 0.2.0**: Transformed into a proper Python package with comprehensive testing
- ✅ **Version 0.2.1**: Fixed detector functions and improved documentation  
- ✅ **Version 0.2.2**: Fixed critical user experience issues
- ✅ **Version 0.2.3**: Enhanced UX with colors, test command, and better errors
- ✅ **Version 0.2.4**: Security fixes for Read/Bash tools
- ✅ **Version 0.2.5**: Code quality improvements (refactoring, type hints)
- ✅ **Version 0.2.6**: User experience improvements (first-run guide, better errors, runtime config)

### Quality Check Summary (2025-07-21)
- ✅ **pytest**: All 83 tests passing with 84% code coverage
- ✅ **Project structure**: Clean working directory, proper .gitignore configuration
- ✅ **src-check score**: 71.0/100 (🟡 Good - some improvements needed)
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

### Remaining Code Quality Items from src-check 🔍
- [ ] **Print statements**: Currently using print() for user-facing output (200+ occurrences across multiple files). This is intentional for CLI tool output, but consider structured logging for debugging
- [ ] **Reduce coupling**: High external call count in core.py, detectors.py, color_utils.py, error_context.py, first_run.py, and last_error.py
- [ ] **Unused imports cleanup**: Several unused imports in __init__.py (some intentionally re-exported for public API)
- [ ] **Security concern in color_utils.py**: os.system() call for Windows ANSI enablement (line 71)
- [ ] **Import inside functions**: Circular dependency concerns in color_utils.py, first_run.py, and last_error.py
- [ ] **Type hint improvements**: Missing or incomplete type hints in several functions
- [ ] **Documentation improvements**: Missing parameter and return documentation in many functions
- [ ] **Performance improvements**: String concatenation in loops (use list.append() + ''.join() instead)


### Version 0.2.6 ✅ COMPLETED (2025-07-21)

#### ユーザー体験の改善
- [x] **初回使用時のガイド改善**: インストール後のメッセージ、--quickstartコマンド、Claude Code連携の自動検出
- [x] **エラーメッセージの実用性向上**: コンテキスト表示、具体的な修正提案、FAQリンク
- [x] **設定ファイルなしでのカスタマイズ**: --ignore-pattern、--allow-file、--disable-detector、環境変数サポート
- [x] **実際の使用フローの改善**: ブロック時の対処法表示、--explain-last-error機能、--help-errors

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
#### その他のユーザビリティ改善
- [ ] **学習曲線の緩和**:
  - [ ] 初回実行時の対話的なチュートリアルモード
  - [ ] よくある使用例のアニメーション表示（asciinemaスタイル）
  - [ ] 段階的な機能紹介（基本→応用）
- [ ] **フィードバックループの改善**:
  - [ ] ユーザーの選択を学習して次回から適用
  - [ ] 「この検出は役立ちましたか？」の簡易フィードバック
- [ ] **統合テストモード**:
  - [ ] プロジェクト全体をスキャンして潜在的な問題を事前に確認
  - [ ] CI/CD前の事前チェックコマンド
  - [ ] 修正提案の一括適用オプション
- [ ] **コンテキスト認識の強化**:
  - [ ] テストファイルでの誤検出を自動的に緩和
  - [ ] プロジェクトタイプ（Web、CLI、ライブラリ等）の自動認識
  - [ ] 言語・フレームワーク固有のベストプラクティス適用
- [ ] **対話的修正モード**: 検出時に修正案を提示し、選択可能に
- [ ] **バッチ処理サポート**: 複数ファイルの一括チェック機能
- [ ] **CI/CD統合の簡易化**: GitHub Actions、GitLab CI用のテンプレート提供
- [ ] **プログレスバー表示**: 大規模プロジェクトでの進捗表示
- [ ] **インタラクティブチュートリアル**: antimon --tutorial コマンド
- [ ] **ベストプラクティスガイド**: 一般的なユースケースの解決方法
- [ ] **トラブルシューティングの自動診断**: --diagnose コマンド
- [ ] **コミュニティフォーラムへの統合**: エラー時に関連する議論へのリンク

#### 最優先の改善項目（2025-07-21 ユーザー評価より） 🚨
- [ ] **`--allow-file` オプションの修正** 🔴 HIGH PRIORITY
  - [ ] 現在、ファイルパスの許可が期待通りに動作しない問題の修正
  - [ ] 許可したファイルでも他の検出器（API key等）は動作するよう改善
  - [ ] グロブパターンのサポート（例: `--allow-file "~/project/*.env"`）
- [ ] **エラーメッセージの具体性向上** 🟡 MEDIUM PRIORITY
  - [ ] 検出パターンをより具体的に表示（例：「.envファイル」ではなく「環境変数ファイル」）
  - [ ] 修正方法の実例をコンテキストに応じて表示
  - [ ] 関連するドキュメントへの直接リンク
  - [ ] 「なぜ危険か」の詳細説明オプション
- [ ] **検出の透明性向上** 🟡 MEDIUM PRIORITY
  - [ ] マッチしたパターンの詳細表示
  - [ ] 検出ロジックの可視化
  - [ ] 誤検出と正当な検出の区別を明確化

#### パフォーマンスと信頼性の改善
- [ ] **キャッシング機構**: 繰り返しチェックのためのキャッシュ実装
- [ ] **非同期検出**: より良いパフォーマンスのための非同期処理
- [ ] **大規模ファイル対応**: メモリ効率的な大規模ファイル処理
- [ ] **エラーリカバリー**: 検出器エラー時の優雅な処理

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


## Long-term Goals

### Long-term User Experience Goals
- [ ] **ワンクリックセットアップ**: 主要なAIアシスタントとの自動連携設定
- [ ] **リアルタイムフィードバック**: コード編集中のリアルタイム警告表示
- [ ] **スマートサジェスト**: 検出パターンに基づく安全な代替案の自動提案
- [ ] **学習型誤検出防止**: プロジェクト固有のパターンを学習して誤検出を削減
- [ ] **統計ダッシュボード**: セキュリティ改善の進捗を可視化
- [ ] **チーム共有設定**: チーム全体で設定を共有・同期
- [ ] **コンテキスト適応型メッセージング**: 初心者/上級者向けメッセージレベル
- [ ] **ゼロ摩擦統合**: エディタ拡張機能での視覚的フィードバック
- [ ] **教育的アプローチ**: セキュリティベストプラクティスの段階的学習

### Developer Experience
- [ ] **IDE Integration Guide**: 各IDEでの設定方法の詳細ドキュメント
- [ ] **Hook debugging mode**: フックの動作をデバッグするための詳細ログモード
- [ ] **Performance profiling**: 大規模プロジェクトでのパフォーマンス計測とボトルネック表示
- [ ] **Rule customization**: カスタムルールの作成と管理機能
- [ ] **API for extensions**: サードパーティ拡張のためのプラグインAPI

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
| 0.2.7 | 2025 Q3 | Performance improvements |
| 0.3.0 | 2025 Q4 | Configuration |
| 0.4.0 | 2026 Q1 | Enhanced detection |
| 0.5.0 | 2026 Q2 | Integrations |
| 1.0.0 | 2027 Q3 | Production ready |




## ユーザージャーニーと改善ポイント（User Journey & Pain Points）

### 現在のユーザー体験フロー

1. **インストール時**
   - ✅ pip/uvでの簡単なインストール
   - ✅ 初回実行時のウェルカムメッセージ
   - ✅ インタラクティブセットアップ（--setup）
   - ❌ インストール直後の動作確認が不明確

2. **初期設定時**
   - ✅ Claude Codeとの自動連携
   - ✅ --testコマンドでの動作確認
   - ❌ 他のツールとの連携方法が不明
   - ❌ プロジェクト固有の設定方法が複雑

3. **日常使用時**
   - ✅ 明確なエラーメッセージ
   - ✅ カラフルな出力
   - ❌ 誤検出時の対処が面倒
   - ❌ 許可オプションが期待通り動作しない

4. **トラブル発生時**
   - ✅ --explain-last-errorでの詳細確認
   - ✅ --help-errorsでのガイダンス
   - ❌ 実際の解決までの道のりが長い
   - ❌ コミュニティサポートへのアクセスが不明

### 理想のユーザー体験

1. **ゼロフリクション導入**
   - インストール後、自動的に最適な設定を提案
   - プロジェクトタイプを認識して適切なルールセットを適用

2. **インテリジェントな検出**
   - コンテキストを理解した上での検出
   - テストファイルと本番コードの区別
   - プロジェクトの慣習を学習

3. **即座の問題解決**
   - ワンクリックで誤検出を報告・除外
   - 具体的な修正案の提示
   - 類似ケースの自動認識

4. **継続的な改善**
   - 使用統計に基づく検出精度の向上
   - コミュニティからのフィードバックの自動反映
   - パーソナライズされた体験

## How to Contribute

1. Check the [Issues](https://github.com/yourusername/antimon/issues) for tasks
2. Fork the repository
3. Create a feature branch
4. Submit a pull request
5. Join our discussions

## Feedback

We welcome feedback and suggestions! Please open an issue or start a discussion to share your ideas for improving antimon.

