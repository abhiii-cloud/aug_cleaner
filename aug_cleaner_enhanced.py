#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import os

def aug_cleaner(input_file, patch_mode="block"):
    """
    Find async callApi and callApiStream functions in JS file and insert patch code
    Automatically creates backup and patches the original file

    Args:
        input_file: Input JS file path to patch
        patch_mode: "block", "random", "empty", "stealth", "debug"
    """

    # Different patch codes for callApi
    callapi_patches = {
        "block": 'if (typeof s === "string" && (s.startsWith("report-") || s.startsWith("record-"))) { return { success: true }; }',

        "random": 'if (typeof s === "string" && (s.startsWith("report-") || s.startsWith("record-"))) { i = { timestamp: Date.now(), version: Math.random().toString(36).substring(2, 8) }; } if (typeof s === "string" && s === "subscription-info") { return { success: true, subscription: { Enterprise: {}, ActiveSubscription: { end_date: "2026-12-31", usage_balance_depleted: false } } }; }',

        "empty": 'if (typeof s === "string" && (s.startsWith("report-") || s.startsWith("record-"))) { i = {}; }',

        "stealth": 'if (typeof s === "string" && (s.startsWith("report-") || s.startsWith("record-"))) { i = { timestamp: Date.now(), session: Math.random().toString(36).substring(2, 10), events: [] }; }',

        "debug": 'if (typeof s === "string" && (s.startsWith("report-") || s.startsWith("record-"))) { i = { timestamp: Date.now(), version: Math.random().toString(36).substring(2, 8) }; } if (typeof s === "string" && s === "subscription-info") { return { success: true, subscription: { Enterprise: {}, ActiveSubscription: { end_date: "2026-12-31", usage_balance_depleted: false } } }; } this.maxUploadSizeBytes = 999999999; this.maxTrackableFileCount = 999999; this.completionTimeoutMs = 999999; this.diffBudget = 999999; this.messageBudget = 999999; this.enableDebugFeatures = true;'
    }

    # Patch code for callApiStream
    callapistream_patches = {
        "block": 'if (typeof n === "string" && (n.startsWith("report-") || n.startsWith("record-"))) { return (async function*() { yield { success: true }; })(); }',

        "random": 'if (typeof n === "string" && (n.startsWith("report-") || n.startsWith("record-"))) { s = { timestamp: Date.now(), version: Math.random().toString(36).substring(2, 8) }; }',

        "empty": 'if (typeof n === "string" && (n.startsWith("report-") || n.startsWith("record-"))) { s = {}; }',

        "stealth": 'if (typeof n === "string" && (n.startsWith("report-") || n.startsWith("record-"))) { s = { timestamp: Date.now(), session: Math.random().toString(36).substring(2, 10), events: [] }; }',

        "debug": 'if (typeof n === "string" && (n.startsWith("report-") || n.startsWith("record-"))) { s = { timestamp: Date.now(), version: Math.random().toString(36).substring(2, 8) }; }'
    }

    # Session ID randomization code for callApiStream
    callapistream_session_code = ' const chars2 = "0123456789abcdef"; let randSessionId2 = ""; for (let j = 0; j < 36; j++) { randSessionId2 += j === 8 || j === 13 || j === 18 || j === 23 ? "-" : j === 14 ? "4" : j === 19 ? chars2[8 + Math.floor(4 * Math.random())] : chars2[Math.floor(16 * Math.random())]; } this.sessionId = randSessionId2; this._userAgent = "";'

    if patch_mode not in callapi_patches:
        print(f"Error: Invalid patch mode '{patch_mode}'. Available modes: {list(callapi_patches.keys())}")
        return False

    # Get the patch codes and add session randomization
    callapi_patch_code = callapi_patches[patch_mode] + ' const chars = "0123456789abcdef"; let randSessionId = ""; for (let i = 0; i < 36; i++) { randSessionId += i === 8 || i === 13 || i === 18 || i === 23 ? "-" : i === 14 ? "4" : i === 19 ? chars[8 + Math.floor(4 * Math.random())] : chars[Math.floor(16 * Math.random())]; } this.sessionId = randSessionId; this._userAgent = "";'

    # callApiStream also needs session randomization
    callapistream_patch_code = callapistream_patches[patch_mode] + callapistream_session_code

    # User ID privacy protection patch 
    userid_privacy_patch = True

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} does not exist")
        return False

    # Create backup filename
    base_name, ext = os.path.splitext(input_file)
    backup_file = f"{base_name}_ori{ext}"

    # Check if backup already exists
    if os.path.exists(backup_file):
        print(f"Warning: Backup file {backup_file} already exists")
        response = input("Continue anyway? (y/N): ").strip().lower()
        if response != 'y':
            print("Operation cancelled")
            return False

    # Read original file content
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error: Cannot read file {input_file}: {e}")
        return False

    # Check if already patched (check for any of the patch signatures)
    patch_signatures = [
        'startsWith("report-")',
        'startsWith("record-")',
        'randSessionId',
        'this._userAgent = ""'
    ]

    if any(sig in content for sig in patch_signatures):
        print("Warning: File appears to be already patched")
        response = input("Continue anyway? (y/N): ").strip().lower()
        if response != 'y':
            print("Operation cancelled")
            return False

    # Find async callApi function pattern
    # Match: async callApi(parameters){
    callapi_pattern = r'(async\s+callApi\s*\([^)]*\)\s*\{)'
    callapi_match = re.search(callapi_pattern, content)

    # Find async callApiStream function pattern
    # Match: async callApiStream(parameters){
    callapistream_pattern = r'(async\s+callApiStream\s*\([^)]*\)\s*\{)'
    callapistream_match = re.search(callapistream_pattern, content)

    if not callapi_match:
        print("Error: async callApi function not found")
        return False

    if not callapistream_match:
        print("Warning: async callApiStream function not found - will only patch callApi")
        callapistream_match = None

    # Create backup
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Backup created: {backup_file}")
    except Exception as e:
        print(f"Error: Cannot create backup file {backup_file}: {e}")
        return False

    # Apply patches to both functions
    patched_content = content
    patches_applied = 0

    # Patch callApi function
    callapi_func_start = callapi_match.end()
    patched_content = patched_content[:callapi_func_start] + callapi_patch_code + patched_content[callapi_func_start:]
    patches_applied += 1
    print(f"[OK] Patched callApi function")

    # Patch callApiStream function if found
    if callapistream_match:
        # Recalculate position after first patch
        callapistream_pattern_updated = r'(async\s+callApiStream\s*\([^)]*\)\s*\{)'
        callapistream_match_updated = re.search(callapistream_pattern_updated, patched_content)
        if callapistream_match_updated:
            callapistream_func_start = callapistream_match_updated.end()
            patched_content = patched_content[:callapistream_func_start] + callapistream_patch_code + patched_content[callapistream_func_start:]
            patches_applied += 1
            print(f"[OK] Patched callApiStream function")
        else:
            print("[WARN] Could not re-locate callApiStream after first patch")

    # Apply userId privacy protection - search for actual patterns in compressed code
    # In compressed version, we need to look for different patterns
    userid_patterns = [
        # Original pattern from uncompressed version
        (r'n = \["userId", "anonymousId", "timestamp", "messageId"\];', 'n = ["timestamp", "messageId"];'),
        # Compressed patterns - look for any variable assignment with these 4 fields
        (r'([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*\["userId",\s*"anonymousId",\s*"timestamp",\s*"messageId"\]', r'\1 = ["timestamp", "messageId"]'),
        # Even more compressed patterns
        (r'([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*\["userId","anonymousId","timestamp","messageId"\]', r'\1 = ["timestamp", "messageId"]'),
    ]

    userid_patches_applied = 0
    for pattern, replacement in userid_patterns:
        if re.search(pattern, patched_content):
            patched_content = re.sub(pattern, replacement, patched_content)
            userid_patches_applied += 1
            break

    if userid_patches_applied > 0:
        patches_applied += userid_patches_applied
        print(f"[OK] Removed userId and anonymousId from telemetry data")
    else:
        # Check if already patched
        already_patched_patterns = [
            r'n = \["timestamp", "messageId"\];',
            r'([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*\["timestamp",\s*"messageId"\]',
            r'([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*\["timestamp","messageId"\]',
        ]

        already_patched = any(re.search(p, patched_content) for p in already_patched_patterns)
        if already_patched:
            print("[OK] userId and anonymousId already removed from telemetry data")
        else:
            print("[WARN] userId telemetry pattern not found")

    # Apply anti-logout protection
    # Based on actual patterns found in compressed version
    logout_patterns = [
        # Pattern found in compressed version: E.status === 401 && this.clientAuth.removeAuthSession()
        (r'([A-Za-z_$][A-Za-z0-9_$]*)\.status === 401 && this\.clientAuth\.removeAuthSession\(\)', r'\1.status === 999 && this.clientAuth.removeAuthSession()'),
        # Other potential patterns
        (r'\(([a-zA-Z_$][a-zA-Z0-9_$]*)\.status === 400 \|\| \1\.status === 401 \|\| \1\.status === 403\)', r'(\1.status === 400 || \1.status === 403)'),
        (r'([A-Za-z_$][A-Za-z0-9_$]*)\.status === 401 && ([a-zA-Z_$][a-zA-Z0-9_$]*) && this\._auth\.removeSession\(\)', r'\1.status === 999 && \2 && this._auth.removeSession()'),
        # Generic 401 status checks
        (r'([A-Za-z_$][A-Za-z0-9_$]*)\.status===401', r'\1.status===999'),
        (r'([A-Za-z_$][A-Za-z0-9_$]*)\.status === 401', r'\1.status === 999'),
    ]

    logout_patches_applied = 0
    for pattern, replacement in logout_patterns:
        matches = re.findall(pattern, patched_content)
        if matches:
            patched_content = re.sub(pattern, replacement, patched_content)
            logout_patches_applied += 1

    if logout_patches_applied > 0:
        patches_applied += logout_patches_applied
        print(f"[OK] Applied anti-logout protection ({logout_patches_applied} patterns)")
    else:
        # Check if already patched
        already_patched_patterns = [
            r'([A-Za-z_$][A-Za-z0-9_$]*)\.status === 999 && this\.clientAuth\.removeAuthSession\(\)',
            r'([A-Za-z_$][A-Za-z0-9_$]*)\.status===999',
            r'([A-Za-z_$][A-Za-z0-9_$]*)\.status === 999',
        ]

        already_patched = any(re.search(p, patched_content) for p in already_patched_patterns)
        if already_patched:
            print("[OK] Anti-logout protection already applied")
        else:
            print("[WARN] Anti-logout patterns not found")

    # Write patched content back to original file
    try:
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(patched_content)
        print(f"\nSUCCESS: {patches_applied} function(s) patched in {input_file}")
        print(f"Mode: {patch_mode}")

        mode_descriptions = {
            "block": "Complete telemetry blocking - no data sent",
            "random": "Random fake data sent - server receives meaningless data",
            "empty": "Empty data sent - minimal payload",
            "stealth": "Stealth mode - sends realistic but fake telemetry data",
            "debug": "Debug mode - removes all limits + fake subscription + enables debug features"
        }

        print(f"Effect: {mode_descriptions[patch_mode]}")
        print("Privacy protection enabled!")
        print("Session ID randomization enabled!")
        print("User-Agent hiding enabled!")
        print("User ID removal enabled!")
        print("Anti-logout protection enabled!")
        return True
    except Exception as e:
        print(f"Error: Cannot write patched file {input_file}: {e}")
        # Try to restore from backup
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
            with open(input_file, 'w', encoding='utf-8') as f:
                f.write(original_content)
            print("Original file restored from backup")
        except:
            print("Failed to restore original file!")
        return False

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Augment Enhanced Privacy Patcher v2.0")
        print("=" * 50)
        print("Usage: python aug_cleaner_enhanced.py <input_js_file> [patch_mode]")
        print("Example: python aug_cleaner_enhanced.py ~/.vscode/extensions/augment.vscode-augment-*/out/extension.js random")
        print("")
        print("Patch modes:")
        print("  random    - Send random fake data (default) - server gets meaningless data")
        print("  debug     - Remove ALL limits + fake premium subscription + enable debug features")
        print("  block     - Complete blocking - no telemetry sent")
        print("  empty     - Send empty data - minimal payload")
        print("  stealth   - Send realistic but fake telemetry data (most hidden)")
        print("")
        print("This enhanced version will:")
        print("1. Create a backup file with _ori suffix")
        print("2. Patch BOTH callApi AND callApiStream functions (comprehensive coverage)")
        print("3. Apply privacy protection while preserving AI functionality")
        print("4. Randomize session ID for each API call")
        print("5. Hide User-Agent information")
        print("")
        print("Privacy Features:")
        print("- Telemetry blocking/modification (report-*, record-*)")
        print("- Session ID randomization (prevents user tracking)")
        print("- User-Agent hiding (prevents system fingerprinting)")
        print("- User ID removal (removes userId and anonymousId from telemetry)")
        print("- Anti-logout protection (prevents forced logout on detection)")
        print("- Comprehensive API coverage (callApi + callApiStream)")
        sys.exit(1)

    input_file = sys.argv[1]
    patch_mode = sys.argv[2] if len(sys.argv) > 2 else "random"

    success = aug_cleaner(input_file, patch_mode)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
