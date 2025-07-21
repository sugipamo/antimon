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

### Quality Check Summary (2025-07-21)
- ✅ **pytest**: All 119 tests passing with 76% code coverage (improved from 82% with more comprehensive testing)
- ✅ **Project structure**: Clean working directory, proper .gitignore configuration
- ⚠️ **src-check score**: 48.8/100 (decreased from 53.5/100, requires urgent attention)
  - Main issues: High use of print statements instead of logging (378 instances), high coupling in several modules, missing type hints
  - Security concerns: Use of os.system() and input() functions detected
  - Architecture: Circular dependencies and god classes detected
  - To be addressed in Version 0.3.0 alongside configuration support
- ✅ **User Experience**: Major UX improvements completed in v0.2.8
  - Direct file/content checking without JSON
  - Claude Code automatic setup wizard
  - Non-interactive demo mode

## Project Vision

Transform antimon from a standalone script into a robust, extensible Python package that can be easily integrated into various AI coding assistant workflows and CI/CD pipelines.


## Version 0.2.1 - 0.2.7 ✅ COMPLETED
- [x] Fix detector functions to check both 'content' and 'new_string' fields
- [x] Add tests for Edit/MultiEdit tool support
- [x] Update README with better examples and documentation
- [x] Fixed `--allow-file` option with glob pattern support
- [x] Enhanced error messages with specific context
- [x] Added `--status`, `--dry-run`, and `--explain-last-error` commands
- [x] Created structured logging foundation
- [x] Improved first-run experience with setup wizard


### Version 0.2.8 (User Experience Enhancement) ✅ COMPLETED (2025-07-21)

#### 最優先改善項目 🔴 CRITICAL - ALL COMPLETED ✅
1. **JSON入力不要の直接チェック機能**
   - [x] `--check-file <path>` - 実ファイルを直接チェック
   - [x] `--check-content "code here"` - コンテンツを直接チェック
   - [x] テストカバレッジの追加（12個の新規テスト）

2. **Claude Code統合の簡単設定**
   - [x] `--setup-claude-code` コマンドの実装
   - [x] 自動的に適切な設定を行い、確認方法も表示
   - [x] `--status`コマンドでClaude Code統合状態を表示

3. **動作確認機能の充実**
   - [x] 非対話的デモモード (`--demo --non-interactive`)
   - [x] 10個のデモケースを自動実行
   - [x] 実行結果と期待値の比較表示

### Version 0.2.9 (User Experience Polish) 🎯 HIGH PRIORITY

#### ドキュメント・ヘルプの改善
1. **GitHub URLの修正**
   - [ ] README.md内の全ての"yourusername"を実際のリポジトリURLに変更
   - [ ] Issue報告先URLの更新
   - [ ] 貢献ガイドラインへのリンク追加

2. **dry-runモードのドキュメント化**
   - [ ] README.mdに`--dry-run`オプションの説明を追加
   - [ ] 使用例とユースケースの明記
   - [ ] Quick Startセクションへの追加

3. **成功時のフィードバック強化**
   - [ ] 通常モード成功時に簡潔な成功メッセージ（`✅ Check passed`）を表示
   - [ ] `--stats`オプションで詳細な統計情報表示
   - [ ] 複数ファイルチェック時の進捗表示

#### エラーハンドリングの改善
1. **Claude Code未インストール時の対応**
   - [ ] `--setup-claude-code`実行時のClaude Code存在チェック強化
   - [ ] インストール方法の詳細な案内表示
   - [ ] 代替の設定方法（手動設定）の提示

2. **設定ファイル未実装の明確化**
   - [ ] antimon.toml使用時により分かりやすいメッセージ
   - [ ] 現在利用可能な代替手段の提案
   - [ ] v0.3.0でのリリース予定機能の説明

#### 初心者向けの改善
1. **インタラクティブモードの強化**
   - [ ] 初回実行時の対話的チュートリアル
   - [ ] よくある使用パターンのサンプル提示
   - [ ] 設定のステップバイステップガイド

2. **エラーメッセージの段階的表示**
   - [ ] 簡潔なエラーメッセージ（デフォルト）
   - [ ] `--explain`で詳細な説明
   - [ ] `--tutorial`でエラー解決のチュートリアル

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

### Code Quality Improvements (Score: 48.8/100) ⚠️ URGENT
- [ ] **セキュリティ**: os.system()とinput()の使用を修正（7箇所のinput()、1箇所のos.system()）
- [ ] **ロギング**: 残り378個のprint文をlogger呼び出しに移行
- [ ] **アーキテクチャ**: 循環依存の解決（6箇所）とモジュール結合度の削減（高結合モジュール多数）
- [ ] **コード品質**: 複雑度の高い関数の簡素化（31箇所）と型ヒントの追加
- [ ] **パフォーマンス**: ループ内での非効率な文字列連結の修正（PERF003違反多数）

## Long-term Goals

- **Developer Experience**: IDE plugins, debugging tools, plugin API, i18n support
- **Community**: GitHub organization, contribution guidelines, pattern sharing
- **Ecosystem**: Editor plugins (VS Code, IntelliJ, Vim), CI/CD integrations
- **Research**: AI-powered suggestions, automated fixes, pattern learning


## Next Steps

🎯 **Version 0.2.9** (User Experience Polish) - See Version 0.2.9 section for detailed tasks
🎯 **Version 0.3.0** (Configuration) - See Version 0.3.0 section for detailed tasks

## Release Schedule

| Version | Target Date | Focus Area |
|---------|------------|------------|
| 0.2.7 | 2025 Q3 | Critical bug fixes & improvements (Complete) |
| 0.2.8 | 2025 Q3 | User Experience Enhancement - Direct checking & Claude Code setup (Complete) |
| 0.2.9 | 2025 Q3 | User Experience Polish - Documentation, error handling, beginner support |
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


