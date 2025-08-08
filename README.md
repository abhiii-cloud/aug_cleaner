# Aug Cleaner

**[简体中文](README_CN.md) | English**

A privacy-focused tool to clean telemetry and tracking from Augment Code VSCode extension while preserving full functionality.

## Overview

Aug Cleaner is a Python utility that patches JavaScript files to remove telemetry and tracking mechanisms from the Augment Code VSCode extension. This tool prioritizes user privacy by intercepting data collection while maintaining all AI features.

## Features

- **Complete Privacy Protection**: Blocks all telemetry and tracking API calls
- **Session Anonymization**: Generates random session IDs for each API call
- **User-Agent Hiding**: Removes user-agent information to prevent fingerprinting
- **Zero Performance Impact**: Direct source-level patching with no runtime overhead
- **Surgical Precision**: Only blocks tracking, preserves all AI functionality
- **Simple Usage**: One command to patch any JavaScript file

## Quick Start

### Installation

```bash
git clone https://github.com/gmh5225/aug_cleaner.git
cd aug_cleaner
```

### Usage

```bash
# Patch Augment extension file directly
python aug_cleaner.py ~/.vscode/extensions/augment.vscode-augment-*/out/extension.js
```

This will:
1. **Create backup**: Automatically creates `extension_ori.js` backup
2. **Patch original**: Modifies the original `extension.js` file directly
3. **Enable privacy**: Blocks all telemetry while preserving AI functionality

### What happens during patching

- **Backup created**: `extension_ori.js` (original file preserved)
- **File patched**: `extension.js` (modified with privacy protection)
- **Safety checks**: Warns if backup exists or file already patched

## How It Works

Aug Cleaner works by:

1. **Locating Target Function**: Finds the `async callApi()` method in JavaScript files
2. **Injecting Privacy Code**: Inserts a compact privacy protection patch
3. **Blocking Telemetry**: Intercepts all `report-*` and `record-*` API endpoints
4. **Anonymizing Sessions**: Generates random UUIDs for each API call
5. **Hiding User Info**: Clears user-agent strings

### What Gets Blocked

- `report-feature-vector` - Feature vector reporting
- `report-error` - Error reporting
- `record-session-events` - Session event recording
- `record-request-events` - Request event recording
- `record-preference-sample` - Preference sampling
- All other `report-*` and `record-*` endpoints

## Privacy Protection

### Triple Protection Layer

1. **Telemetry Blocking**
   - Intercepts all tracking API calls
   - Returns success responses to maintain functionality
   - Zero data leaves your machine

2. **Session Randomization**
   - Generates unique session ID for each API call
   - Prevents behavior correlation across sessions
   - Makes user tracking impossible

3. **User-Agent Hiding**
   - Removes system fingerprinting data
   - Prevents device identification
   - Maintains complete anonymity

## Requirements

- Python 3.6+
- No external dependencies required

## Technical Details

### Patch Code Overview

The injected code is highly optimized and compressed:

```javascript
// Intercept telemetry calls
if (typeof s === "string" && (s.startsWith("report-") || s.startsWith("record-"))) { 
  return { success: true }; 
}

// Generate random session ID
const chars = "0123456789abcdef"; 
let randSessionId = ""; 
for (let i = 0; i < 36; i++) { 
  randSessionId += i === 8 || i === 13 || i === 18 || i === 23 ? "-" : 
                   i === 14 ? "4" : 
                   i === 19 ? chars[8 + Math.floor(4 * Math.random())] : 
                   chars[Math.floor(16 * Math.random())]; 
}

// Apply privacy settings
this.sessionId = randSessionId;
this._userAgent = "";
```

### Why This Approach?

- **Surgical Precision**: Targets the single API entry point
- **100% Coverage**: All HTTP requests go through `callApi()`
- **Minimal Code**: ~15 lines vs 100+ lines of network interception
- **Zero Performance Impact**: No runtime overhead
- **Maximum Compatibility**: Doesn't interfere with other functionality

## Important Notes

- **Backup First**: Always backup original files before patching
- **Disable Auto-Update**: Turn off auto-update for Augment Code extension in VSCode to prevent patch overwriting
- **Extension Updates**: Re-apply patch after manual extension updates
- **Functionality Preserved**: All AI features continue to work normally
- **Privacy First**: No telemetry data leaves your machine

### How to Disable Auto-Update

1. Open VSCode Extensions panel (Ctrl+Shift+X)
2. Find the Augment Code extension
3. Click the gear icon on the right side of the extension
4. Select "Disable Auto Update"

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for privacy-conscious developers
- Inspired by the need for transparent AI tools
- Dedicated to user privacy and data sovereignty

---

**Disclaimer**: This tool is for educational and privacy protection purposes. Users are responsible for compliance with applicable terms of service and local laws.
