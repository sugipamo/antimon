# antimon Development Roadmap

## Project Vision

Transform antimon from a standalone script into a robust, extensible Python package that can be easily integrated into various AI coding assistant workflows and CI/CD pipelines.

## Version 0.1.0 (Initial Release) ✓
- [x] Basic hook functionality for Claude Code
- [x] Core detection patterns (files, APIs, Docker, localhost)
- [x] Claude-based anti-pattern detection
- [x] JSON input processing
- [x] Error output formatting

## Version 0.2.0 (Package Structure) ✓
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

### Next Steps
- [x] Add pytest configuration and run tests
- [ ] Create GitHub Actions workflow for CI
- [x] Add development dependencies (pytest, black, mypy, ruff)
- [ ] Implement proper error handling and logging
- [ ] Add example usage scripts
- [ ] Update typing imports to use Python 3.9+ style (dict instead of Dict)
- [ ] Replace print statements with proper logging
- [ ] Add LICENSE file
- [ ] Add copyright headers to source files

### User Experience Improvements (ユーザー体験の改善)
- [ ] **Verbose mode enhancement**: 現在の-vオプションが機能していない。検出プロセスの詳細を表示
- [ ] **Success feedback**: 検出されなかった場合に「No security issues detected」等の成功メッセージを表示
- [ ] **Detection summary**: 複数の問題が検出された場合、終了時にサマリーを表示
- [ ] **Color output**: 端末でのカラー出力対応（エラーは赤、成功は緑など）
- [ ] **Progress indicator**: 大きなファイルや複数ファイルの検証時の進捗表示
- [ ] **Exit code documentation**: README.mdに終了コードの意味を明記
- [ ] **Quickstart guide**: インストール後すぐに試せるクイックスタートガイドの追加
- [ ] **Examples directory**: 様々なユースケースのサンプルを含むexamplesディレクトリ
- [ ] **JSON schema**: 入力JSONフォーマットのスキーマ定義とバリデーション
- [ ] **Error recovery suggestions**: エラー時に次のアクションを提案（例：「JSON形式を確認してください」）
- [ ] **Dry-run mode**: 実際の検証を行わず、何がチェックされるかを表示するモード
- [ ] **Quiet mode**: エラーのみを表示し、成功時は何も出力しないモード
- [ ] **Machine-readable output**: CI/CD統合のためのJSON/YAML形式の出力オプション

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
| 0.2.0 | 2025 Q3 | Package structure |
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