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
  - Main issues: High use of print statements instead of logging, high coupling in several modules, missing type hints in some places
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

#### 最優先改善項目 (2025-07-21 更新)

##### 0. 緊急修正項目 🔴 CRITICAL
- [ ] **重複ログ出力の修正**: 同じメッセージが2回表示される問題を修正
- [ ] **テストケースの修正**: 失敗している2つのテストを新しいメッセージフォーマットに合わせて修正
- [ ] **ログ出力の改善**: タイムスタンプは--verboseモードのみで表示

##### 1. 使用方法の明確化 🔴 CRITICAL
- [x] **動作確認コマンドの充実 (部分的)** ✅
- [x] **設定状態の可視化** ✅ (2025-07-21)
  - [x] `antimon --status` で現在の設定、有効な検出器、除外パターンを一覧表示
  - [x] Claude Codeとの連携状態の確認機能
- [ ] **残りの機能**:
  - [ ] 非対話的デモモード (`--demo --non-interactive`) - CI/CDでも使用可能
  - [ ] 実ファイルテスト機能 (`--check-file <path>`) - 実際のファイルでブロック判定を事前確認
  - [ ] テストコマンドの修正 - 失敗している2つのテストケースを修正
  - [ ] 最近の検出履歴の表示

##### 2. 操作の直感性向上 🟡 HIGH
- [x] **簡潔なエラー表示** ✅ (2025-07-21)
  - [x] `--dry-run` オプションで検出のプレビューモード（実際のブロックなし）
  - [x] エラーメッセージの階層化（簡潔→詳細）
- [ ] **残りの機能**:
  - [ ] `--brief` オプションで簡潔なエラー表示モード
  - [ ] 詳細は `--explain-last-error` で確認する設計の改善
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

##### 6. ユーザビリティ改善項目 🟡 HIGH
- [ ] **初回利用時の体験改善**: 動作確認フローとクイックスタートガイドの改善
- [ ] **エラーメッセージの最適化**: --briefモードでワンライナー、--verboseで技術的詳細
- [ ] **設定の永続化**: プロジェクトごとの設定ファイル（.antimon/config）とグローバル設定
- [ ] **実行コンテキストの認識**: CI/CD環境での自動出力調整、TTY検出による対話モード切替

##### 7. その他の利便性向上 🟢 LOW
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
- [x] **ロギング**: AntimonLoggerクラス作成済み (部分的完了)
  - [ ] 残り378個のprint文をlogger呼び出しに移行
- [ ] **セキュリティ**: os.system()とinput()の使用を修正
- [ ] **アーキテクチャ**: 循環依存の解決とモジュール結合度の削減
- [ ] **コード品質**: 複雑度の高い関数の簡素化と型ヒントの追加

## Long-term Goals

- **Developer Experience**: IDE plugins, debugging tools, plugin API, i18n support
- **Community**: GitHub organization, contribution guidelines, pattern sharing
- **Ecosystem**: Editor plugins (VS Code, IntelliJ, Vim), CI/CD integrations
- **Research**: AI-powered suggestions, automated fixes, pattern learning


## Next Steps

### 🚨 緊急対応 (1-2日)
1. **重複ログ出力の修正** - 同じメッセージが2回表示される問題
2. **テストケースの修正** - `antimon --test`ですべてパスするように
3. **出力の簡潔化** - デフォルトでタイムスタンプを非表示に

### ⚠️ コード品質改善 (1週間)
1. **セキュリティ修正** - os.system()とinput()の使用を修正
2. **ロギング移行完了** - 残り378個のprint文を移行
3. **アーキテクチャ改善** - 循環依存の解決と複雑度の削減

### 🎯 中期目標 (2週間)
1. **設定ファイルサポート** - .antimonrcでプロジェクト設定を永続化
2. **対話的な誤検出対処** - 「今後許可する？」の選択肢
3. **`--check-file`コマンド** - 実ファイルの事前チェック
4. **検出履歴と統計** - 検出傾向の分析機能



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


