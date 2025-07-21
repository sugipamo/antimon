# antimon Development Roadmap

## Current Status (2025-07-21)

🎉 **Version 0.2.0 has been successfully completed!** The project has been transformed into a proper Python package with comprehensive testing, documentation, and code quality checks. All tests are passing (20/20) and the code quality score is 93.8/100.

## Project Vision

Transform antimon from a standalone script into a robust, extensible Python package that can be easily integrated into various AI coding assistant workflows and CI/CD pipelines.

## Version 0.1.0 (Initial Release) ✓
- [x] Basic hook functionality for Claude Code
- [x] Core detection patterns (files, APIs, Docker, localhost)
- [x] Claude-based anti-pattern detection
- [x] JSON input processing
- [x] Error output formatting

## Version 0.2.0 (Package Structure) ✅ COMPLETED
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

### Version 0.2.1 (Bug Fixes & Improvements)
- [x] Fix detector functions to check both 'content' and 'new_string' fields
- [x] Add tests for Edit/MultiEdit tool support
- [ ] Update README with better examples and documentation

### User Experience Improvements (ユーザー体験の改善)

#### 即時対応が必要な項目 (High Priority)
- [x] **Success feedback**: 検出されなかった場合に「No security issues detected」等の成功メッセージを表示（実装済み）
- [x] **Verbose mode fix**: -vオプションが正常に動作するように修正（実装済み、ただし非verboseモード時との差別化が必要）
- [ ] **Help text improvement**: --helpで表示される説明をより具体的に（使用例の追加）
- [ ] **Error message clarity**: エラーメッセージに対処法を含める（例：「JSON parsing error: Expected property name... → Try: echo '{valid json}' | antimon」）
- [ ] **Exit code behavior**: 非コード編集ツール（Read, Bashなど）の場合の明確なフィードバック

#### ログ出力の改善 (Logging Improvements)
- [ ] **Log format simplification**: タイムスタンプをシンプルに（現在：2025-07-21 10:14:33 → 10:14:33）
- [ ] **Log level visibility**: DEBUGログとINFO/WARNINGログの視覚的差別化
- [ ] **Structured logging**: 検出結果を構造化して表示（検出器名、ファイルパス、行番号など）
- [ ] **Summary at end**: 全検出器の実行結果サマリー（例：「6 detectors run, 1 issue found」）
- [ ] **Quiet mode**: エラーのみを表示し、成功時は何も出力しないモード（--quiet/-q）

#### インストールと初回使用 (Installation & First Use)
- [ ] **Installation verification**: インストール後の動作確認コマンド（antimon --version、antimon --test）
- [ ] **Quick test command**: サンプルデータで即座に動作確認できるコマンド（antimon --demo）
- [ ] **README examples**: コピペで試せる実例を3-5個追加
- [ ] **Common errors section**: よくあるエラーと解決方法のセクション

#### 検出結果の理解しやすさ (Detection Result Clarity)
- [ ] **Detection context**: なぜ危険なのかの簡潔な説明（例：「/etc/passwd: System password file (read can expose user info)」）
- [ ] **Severity levels**: 検出の深刻度表示（Critical/High/Medium/Low）
- [ ] **Fix suggestions**: 検出された問題の修正方法の提案
- [ ] **Whitelist instructions**: 誤検出の場合の除外方法の案内

#### 開発者向け機能 (Developer Features)
- [ ] **Dry-run mode**: 実際の検証を行わず、何がチェックされるかを表示するモード
- [ ] **JSON output mode**: CI/CD統合のためのJSON形式出力（--output-format json）
- [ ] **Hook test mode**: フック設定のテストモード（実際のAIツールなしで動作確認）
- [ ] **Debug output**: 内部処理の詳細を出力するデバッグモード（--debug）

#### ドキュメントの充実 (Documentation Enhancement)
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
- [ ] Per-project configuration (`antimon.toml`)
- [ ] Global configuration (`~/.config/antimon/antimon.toml`)
- [ ] Environment variable overrides
- [ ] Configuration file validation and schema

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
- [ ] Reporting formats:
  - [ ] SARIF (Static Analysis Results Interchange Format)
  - [ ] JUnit XML
  - [ ] HTML reports
  - [ ] Markdown reports

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
- [ ] **Rule explanation**: なぜその検出が危険なのかを説明する機能
- [ ] **Fix suggestions**: 検出された問題に対する修正提案
- [ ] **Learning mode**: 誤検出を学習し、プロジェクト固有のルールを生成

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