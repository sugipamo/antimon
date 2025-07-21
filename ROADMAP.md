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

### 🔍 ユーザー体験テストの結果（2025-07-21 追加）

実際のユーザー視点でantimonを使用したところ、以下の重要な問題が判明しました：

#### 🔴 緊急対応が必要な問題
1. **Exit Codeの不具合**: セキュリティ問題を検出してもexit code 0を返す（CI/CDでの自動化が機能しない）
2. **セキュリティホール**: ReadとBashツールが検証をスキップ（機密ファイルアクセスや危険なコマンド実行を見逃す）
3. **出力の不一致**: READMEの例と実際の出力が異なる（ユーザーの混乱を招く）

#### 🟡 使いやすさの問題
1. **Quietモードの不具合**: `-q`でセキュリティ問題の詳細が表示されない
2. **エラーメッセージが技術的すぎる**: 正規表現パターンが表示されて理解困難
3. **バージョン表示の不一致**: READMEとコマンドで異なるバージョンが表示される
4. **設定フラグの混乱**: `--config`が未実装なのに受け付けてしまう

#### 🟢 良い点
- 多様なセキュリティ問題を適切に検出
- パスとラバーサル攻撃への対応
- 大量コンテンツでも高速動作
- JSONエラーの分かりやすい表示

### Quality Check Summary (2025-07-21)
- ✅ **pytest**: All 31 tests passing with 76% code coverage
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

### User Experience Improvements (ユーザー体験の改善)

#### 即時対応が必要な項目 (High Priority) ✅ COMPLETED
- [x] **Success feedback**: 検出されなかった場合に「No security issues detected」等の成功メッセージを表示
- [x] **Verbose mode fix**: -vオプションが正常に動作するように修正
- [x] **Help text improvement**: --helpで表示される説明をより具体的に（使用例の追加）
- [x] **Error message clarity**: エラーメッセージに対処法を含める
- [x] **Exit code behavior**: 非コード編集ツール（Read, Bashなど）の場合の明確なフィードバック

### Code Quality Improvements from src-check (2025-07-21) 🔍
- [ ] **Print statements in core.py**: Currently using print() for user-facing output (65+ occurrences). This is intentional for CLI tool output, but consider structured logging for debugging
- [ ] **Reduce coupling in core.py, detectors.py, and color_utils.py**: High external call count (125, 41, and 52 respectively, max recommended: 15). Note: This is partly due to the nature of security detection requiring many patterns
- [ ] **Complex function refactoring**: process_stdin function has complexity of 35 (max recommended: 10). Consider breaking into smaller functions
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

### Version 0.2.4 (Next Up) 🚀
次に実装予定のタスク（セキュリティホールの修正）:

#### 今後の開発方針 (2025-07-21)
Version 0.2.3でユーザー体験の基本的な改善が完了しました。次のVersion 0.2.4では、ユーザーテストで判明した重要なセキュリティホールの修正に焦点を当てます。特に、ReadとBashツールが現在「安全」として扱われている問題は、antimonの本来の目的である「セキュリティ検証」を損なう可能性があるため、早急な対応が必要です。

#### 🚨 セキュリティ上の懸念事項（ユーザーテストで判明）
- [ ] **ReadとBashツールの安全性**: 現在これらは「安全」として扱われ、検証をスキップしている
  - [ ] Readツールで`/etc/passwd`などの機密ファイルアクセスを検出すべき
  - [ ] Bashツールで危険なコマンド実行を検出すべき
  - [ ] セキュリティホールとなる可能性があるため、早急な対応が必要

#




#### 5. テストの改善（t-wada推奨形式） 🧪
- [x] **Test docstrings**: テストクラスにdocstringを追加して目的を明確化 ✅ COMPLETED (2025-07-21)
- [ ] **Parameterized tests**: 類似のテストケースを@pytest.mark.parametrizeで効率化
- [ ] **Edge case tests**: 空の入力、不正な形式、境界値のテストを追加



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
| 0.2.4 | 2025 Q3 | Security fixes (Read/Bash tools) |
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

## ユーザー視点での必要な改善点 (User Experience Improvements) - 2025-07-21追加

### 実際の使用体験からの課題と改善提案

#### 1. 初回使用時の戸惑いを解消
**現状の問題点**:
- 安全な操作で何も表示されない場合、ツールが動作したか不明
- インストール後の動作確認方法が不明確
- 成功時のフィードバックが完全に無音

**改善提案**:
- [ ] `--test` オプションを追加し、サンプルデータで動作確認可能に
- [ ] インストール直後に `antimon --test` で全検出器の動作を確認
- [x] `--feedback` オプションで成功時も「✓ No issues detected」を表示 ✅ (v0.2.2でデフォルト動作に)
- [ ] Quick Startセクションに動作確認手順を明記

#### 2. セキュリティホールの解消 🚨
**重大な問題**: 
- ReadとBashツールが検証対象外となっており、危険な操作が素通りする
- 例: `rm -rf /`、`/etc/shadow`の読み取り、`curl | bash`等が検出されない

**改善提案**:
- [ ] **Bashツール検証の追加**:
  - 破壊的コマンド（`rm -rf /`、`dd if=/dev/zero`等）
  - 権限昇格（`sudo`、`su`、`chmod 777`等）  
  - 外部スクリプト実行（`curl | bash`、`wget | sh`等）
  - システムファイル操作（`/etc/*`、`/sys/*`への書き込み）
- [ ] **Readツール検証の追加**:
  - システムファイル（`/etc/shadow`、`/etc/passwd`等）
  - 秘密鍵（`~/.ssh/id_*`、`*.pem`、`*.key`等）
  - 認証情報（`~/.aws/credentials`、`.env`等）
- [ ] **グローバル除外リストの実装**

#### 3. エラーメッセージの親切さ向上
**現状の問題点**:
- 正規表現パターンが表示されて技術者以外には理解困難
- 対処法が抽象的で具体的な行動が不明
- 誤検出時の回避方法が不明確

**改善提案**:
- [ ] **メッセージの階層化**:
  - 通常: 人間向けの簡潔な説明のみ
  - `-v`: 技術的詳細（正規表現、検出ロジック）を追加表示
  - `--explain <issue>`: 特定の問題の詳細説明と対処法
- [ ] **具体的な対処法の提示**:
  - 「APIキーは.envファイルに移動し、環境変数で参照」
  - 「機密ファイルへのアクセスは設定ファイル経由に変更」
  - コード例を含む修正案の提示
- [ ] **誤検出対応の明確化**:
  - `--generate-whitelist` で除外設定を自動生成
  - よくある誤検出パターンのドキュメント化

#### 4. 出力形式の一貫性と可読性
**現状の問題点**:
- ログメッセージとエラーメッセージが混在
- タイムスタンプが冗長（通常使用では不要）
- CI/CDでの解析が困難

**改善提案**:
- [ ] **構造化された出力**:
  - ヘッダー: 検証対象の要約
  - ボディ: 検出された問題（重要度順）
  - フッター: 統計情報と次のアクション
- [ ] **カラー出力サポート**:
  - エラー: 赤
  - 警告: 黄
  - 成功: 緑
  - `--no-color` オプションでCI/CD対応
- [ ] **複数の出力形式**:
  - `--format human` (デフォルト): 人間向け
  - `--format json`: CI/CD連携用
  - `--format github`: GitHub Actions用
  - `--format junit`: JUnit XML形式

#### 5. 開発者体験の向上
**現状の問題点**:
- Pythonモジュールとしての使用例が少ない
- カスタム検出器の追加方法が不明
- 大量ファイルチェック時のパフォーマンス問題

**改善提案**:
- [ ] **APIドキュメントの充実**:
  - 各検出器の仕様と拡張方法
  - カスタム検出器の実装例
  - 非同期処理のサポート
- [ ] **パフォーマンス最適化**:
  - 並列処理による高速化
  - キャッシュ機構の実装
  - プログレスバーの表示
- [ ] **統合ガイドの作成**:
  - VS Code拡張機能の作成方法
  - GitHub Actionsでの使用例
  - pre-commitフックの設定例

#### 6. 日本語圏ユーザーへの配慮
**現状の問題点**:
- エラーメッセージが英語のみ
- 日本語ファイル名での動作が未検証
- 日本特有のセキュリティパターンが未対応

**改善提案**:
- [ ] **多言語対応の基盤**:
  - `--lang ja` オプションの実装
  - gettext形式でのメッセージ管理
  - 言語別のヘルプドキュメント
- [ ] **日本語環境での動作保証**:
  - マルチバイト文字のファイルパス対応
  - 各種エンコーディング（UTF-8、Shift-JIS等）のサポート
  - 日本語コメントでの誤検出防止
- [ ] **日本特有のパターン追加**:
  - マイナンバー検出
  - 日本の金融機関APIパターン
  - 日本のクラウドサービス認証情報

### 実装優先順位

1. **緊急（Version 0.2.4）**: セキュリティホールの修正
2. **重要（Version 0.2.5）**: 基本的なUX改善
3. **推奨（Version 0.3.0）**: 設定とカスタマイズ
4. **将来（Version 0.4.0+）**: 高度な機能と統合

## ユーザー体験レビューから見えた追加改善点 (2025-07-21 追加)

### 新規ユーザーのオンボーディング体験

#### 1. インストール後の不安解消
**現状の問題**:
- インストール完了後、正しく動作しているか確認する手段が分かりづらい
- Quick Startの例は分かりやすいが、実際のユースケースとの繋がりが弱い
- 成功時に無出力なので、初回使用時に「本当に動いているのか？」と不安になる

**改善提案**:
- [ ] **インストール成功メッセージ**: `pip install antimon`後に次のステップを表示
- [ ] **初回実行ガイド**: `antimon --first-run`で対話的な使い方チュートリアル
- [ ] **実践的なQuick Start**: よくあるシナリオ（CI/CD設定、pre-commit等）の例を追加
- [ ] **成功確認機能**: `--check-setup`でClaude Code連携を含む全体の動作確認

#### 2. エラー時の学習機会
**現状の問題**:
- エラーメッセージは改善されたが、「なぜこれが危険なのか」の教育的側面が不足
- 修正方法は提示されるが、具体的なコード例がない
- 同じ間違いを繰り返さないための学習リソースへのリンクがない

**改善提案**:
- [ ] **教育モード**: `--explain`オプションで各検出の詳細な説明を表示
- [ ] **修正例の提示**: 検出されたコードの安全な書き換え例を表示
- [ ] **学習リソース**: OWASP等のセキュリティベストプラクティスへのリンク
- [ ] **履歴機能**: 過去の検出パターンを記録し、学習進捗を可視化

### プロフェッショナル開発者向けの機能

#### 1. CI/CDパイプラインでの使いやすさ
**現状の問題**:
- JSON形式の入力が必須で、既存のファイルを直接チェックできない
- 複数ファイルの一括チェックが煩雑
- CI/CDでの結果解析が難しい（構造化された出力がない）

**改善提案**:
- [ ] **ファイル直接チェック**: `antimon check <file>` でファイルを直接検証
- [ ] **ディレクトリスキャン**: `antimon scan .` でプロジェクト全体をチェック
- [ ] **SARIF形式出力**: GitHub Code Scanningとの統合
- [ ] **並列処理**: 大規模プロジェクトでの高速スキャン

#### 2. カスタマイズと拡張性
**現状の問題**:
- カスタム検出ルールの追加方法が不明確
- プロジェクト固有のパターンを定義できない
- 既存の検出器の調整（感度調整等）ができない

**改善提案**:
- [ ] **プラグインアーキテクチャ**: `~/.antimon/plugins/`にカスタム検出器を配置
- [ ] **ルールDSL**: YAMLやTOMLでカスタムルールを定義
- [ ] **検出器の優先度設定**: プロジェクトに応じた検出器の重要度調整
- [ ] **コンテキスト認識**: ファイルタイプやプロジェクトタイプに応じた動的ルール適用

### チーム開発での利用

#### 1. チーム全体での統一性
**現状の問題**:
- チームメンバー間で設定を共有する仕組みがない
- 誤検出の共有と対処法の蓄積ができない
- プロジェクト固有のセキュリティポリシーを定義できない

**改善提案**:
- [ ] **共有設定**: `.antimon/` ディレクトリでプロジェクト設定を管理
- [ ] **誤検出データベース**: チーム内で誤検出パターンを共有
- [ ] **ポリシーテンプレート**: 業界別・規模別のセキュリティポリシーテンプレート
- [ ] **監査ログ**: 誰が何を許可/拒否したかの記録

#### 2. 開発フローへの統合
**現状の問題**:
- VSCode等のエディタでリアルタイムフィードバックがない
- PRレビュー時の自動チェックが複雑
- 既存のセキュリティツールとの連携が不明

**改善提案**:
- [ ] **LSP実装**: エディタでのリアルタイム検証
- [ ] **GitHub App**: PR作成時の自動コメント機能
- [ ] **統合API**: 他のセキュリティツールとのデータ連携
- [ ] **ダッシュボード**: プロジェクト全体のセキュリティ状況可視化

### 非技術者ステークホルダー向け

#### 1. セキュリティレポート
**現状の問題**:
- 技術者以外が理解できる形式でのレポートがない
- セキュリティ改善の進捗が見えない
- コンプライアンス要件との対応が不明確

**改善提案**:
- [ ] **エグゼクティブサマリー**: 非技術者向けのレポート生成
- [ ] **トレンドグラフ**: セキュリティ指標の時系列変化
- [ ] **コンプライアンスマッピング**: ISO27001、SOC2等との対応表
- [ ] **リスクスコアリング**: ビジネスインパクトに基づく優先順位付け

### 日本市場特有のニーズ

#### 1. ローカライゼーション
**現状の問題**:
- エラーメッセージが英語のみで、日本の開発現場での採用障壁
- 日本特有のセキュリティ要件（マイナンバー等）への対応不足
- 日本語ドキュメントの不在

**改善提案**:
- [ ] **完全日本語化**: UI、ドキュメント、エラーメッセージの日本語対応
- [ ] **日本法規対応**: 個人情報保護法、マイナンバー法への対応
- [ ] **日本語コミュニティ**: Qiita記事、Zenn本の執筆支援
- [ ] **国内クラウド対応**: AWS東京リージョン等の考慮

### 実装ロードマップの見直し

これらの改善点を踏まえ、以下の順序での実装を提案:

1. **Version 0.2.4**: 基本的な使いやすさ改善
   - ファイル直接チェック機能
   - 成功時のフィードバック
   - より親切なエラーメッセージ

2. **Version 0.2.5**: セキュリティホール対応
   - Read/Bashツールの検証追加
   - より包括的なセキュリティパターン

3. **Version 0.3.0**: チーム開発対応
   - 共有設定機能
   - CI/CD統合の改善
   - 構造化出力フォーマット

4. **Version 0.4.0**: エンタープライズ機能
   - カスタマイズ性の向上
   - レポート機能
   - 日本語対応