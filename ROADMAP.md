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
- ✅ **pytest**: All 107 tests passing with 82% code coverage  
- ✅ **Project structure**: Clean working directory, proper .gitignore configuration (cache files exist but are properly ignored)
- ⚠️ **src-check score**: 53.5/100 (🔴 Decreased from 59.3/100 - requires attention)
  - Main issues: High use of print statements instead of logging (378 print statements found), high coupling in several modules, missing type hints in some places
  - New issues detected: Dangerous functions (os.system, input), circular dependencies, high complexity functions
- ✅ **User Experience Review**: Comprehensive evaluation completed with actionable improvements identified

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


### Version 0.2.8 (User Experience Enhancement) 🎯

#### 最優先改善項目 🔴 CRITICAL
1. **JSON入力不要の直接チェック機能**
   - [ ] `--check-file <path>` - 実ファイルを直接チェック
   - [ ] `--check-content "code here"` - コンテンツを直接チェック
   - [ ] 対話的な入力モード（JSONを意識させない）

2. **Claude Code統合の簡単設定**
   - [ ] `--setup-claude-code` コマンドの実装
   - [ ] 自動的に適切な設定を行い、確認方法も表示

3. **動作確認機能の充実**
   - [ ] 非対話的デモモード (`--demo --non-interactive`)
   - [ ] 最近の検出履歴の表示
   - [ ] verboseモードのログ重複修正

#### ユーザビリティ改善 🟡 HIGH
1. **エラー時の明確な次のアクション**
   - [ ] `--faq` コマンドで一般的な問題と解決策を表示
   - [ ] エラー発生時に「次に何をすべきか」を番号付きリストで表示
   - [ ] `antimon --diagnose` で環境、設定、権限などを総合チェック

2. **誤検出時のワンステップ対処**
   - [ ] 検出時に「このパターンを今後無視する？[Y/n]」の対話的選択
   - [ ] 選択結果をプロジェクト設定（.antimon/config）に自動保存
   - [ ] テストファイル（*_test.py）での自動的な検出緩和

3. **成功時のフィードバック**
   - [ ] `--verbose` 時は「✓ Operation allowed」のような肯定的フィードバック
   - [ ] `--quiet` モードでの完全な無音動作
   - [ ] 統計情報表示（「3 operations checked, all allowed」など）

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

### Code Quality Improvements (Score: 53.5/100) ⚠️
- [ ] **セキュリティ**: os.system()とinput()の使用を修正
- [ ] **ロギング**: 残り378個のprint文をlogger呼び出しに移行
- [ ] **アーキテクチャ**: 循環依存の解決とモジュール結合度の削減
- [ ] **コード品質**: 複雑度の高い関数の簡素化と型ヒントの追加

## Long-term Goals

- **Developer Experience**: IDE plugins, debugging tools, plugin API, i18n support
- **Community**: GitHub organization, contribution guidelines, pattern sharing
- **Ecosystem**: Editor plugins (VS Code, IntelliJ, Vim), CI/CD integrations
- **Research**: AI-powered suggestions, automated fixes, pattern learning


## Next Steps

### 🎯 Version 0.2.8 Priority (In Progress)
- Focus on items listed in Version 0.2.8 section above
- Priority: Direct file checking without JSON, Claude Code integration

### 🎯 Version 0.3.0 Next (Configuration)
- See Version 0.3.0 section for detailed tasks



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


