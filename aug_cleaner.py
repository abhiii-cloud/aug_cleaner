#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import os

def aug_cleaner(input_file, patch_mode="block"):
    """
    Find async callApi function in JS file and insert patch code
    Automatically creates backup and patches the original file

    Args:
        input_file: Input JS file path to patch
        patch_mode: "block" , "random" , "empty" 
    """

    # Different patch codes
    patches = {
        "block": 'if (typeof s === "string" && (s.startsWith("report-") || s.startsWith("record-"))) { return { success: true }; }',

        "random": 'if (typeof s === "string" && (s.startsWith("report-") || s.startsWith("record-"))) { i = { timestamp: Date.now(), version: Math.random().toString(36).substring(2, 8) }; }',

        "empty": 'if (typeof s === "string" && (s.startsWith("report-") || s.startsWith("record-"))) { i = {}; }',

        "stealth": 'if (typeof s === "string" && (s.startsWith("report-") || s.startsWith("record-"))) { i = { timestamp: Date.now(), session: Math.random().toString(36).substring(2, 10), events: [] }; }',

        "debug": 'if (typeof s === "string" && (s.startsWith("report-") || s.startsWith("record-"))) { i = { timestamp: Date.now(), version: Math.random().toString(36).substring(2, 8) }; } if (typeof s === "string" && s === "subscription-info") { return { success: true, subscription: { Enterprise: {}, ActiveSubscription: { end_date: "2026-12-31", usage_balance_depleted: false } } }; } this.maxUploadSizeBytes = 999999999; this.maxTrackableFileCount = 999999; this.completionTimeoutMs = 999999; this.diffBudget = 999999; this.messageBudget = 999999; this.enableDebugFeatures = true;'
    }

    if patch_mode not in patches:
        print(f"Error: Invalid patch mode '{patch_mode}'. Available modes: {list(patches.keys())}")
        return False

    # Get the patch code and add session randomization
    patch_code = patches[patch_mode] + ' const chars = "0123456789abcdef"; let randSessionId = ""; for (let i = 0; i < 36; i++) { randSessionId += i === 8 || i === 13 || i === 18 || i === 23 ? "-" : i === 14 ? "4" : i === 19 ? chars[8 + Math.floor(4 * Math.random())] : chars[Math.floor(16 * Math.random())]; } this.sessionId = randSessionId; this._userAgent = "";'

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
    pattern = r'(async\s+callApi\s*\([^)]*\)\s*\{)'

    match = re.search(pattern, content)
    if not match:
        print("Error: async callApi function not found")
        return False

    # Create backup
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Backup created: {backup_file}")
    except Exception as e:
        print(f"Error: Cannot create backup file {backup_file}: {e}")
        return False

    # Find function start position
    func_start = match.end()

    # Insert patch code after function start
    patched_content = content[:func_start] + patch_code + content[func_start:]

    # Write patched content back to original file
    try:
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(patched_content)
        print(f"Success: Patch applied to {input_file}")
        print(f"Mode: {patch_mode}")
        
        mode_descriptions = {
            "block": "Complete telemetry blocking - no data sent",
            "random": "Random fake data sent - server receives meaningless data",
            "empty": "Empty data sent - minimal payload",
            "stealth": "Stealth mode - sends realistic but fake telemetry data",
            "debug": "Debug mode - fake subscription + unlimited limits + enhanced features"
        }
        
        print(f"Effect: {mode_descriptions[patch_mode]}")
        print("Privacy protection enabled!")
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
        print("Usage: python aug_cleaner.py <input_js_file> [patch_mode]")
        print("Example: python aug_cleaner.py ~/.vscode/extensions/augment.vscode-augment-*/out/extension.js random")
        print("")
        print("Patch modes:")
        print("  random  - Send random fake data (default) - server gets meaningless data")
        print("  block   - Complete blocking - no telemetry sent")
        print("  empty   - Send empty data - minimal payload")
        print("  stealth - Send realistic but fake telemetry data (most hidden)")
        print("  debug   - Debug mode - fake subscription + unlimited limits + enhanced features")
        print("")
        print("This will:")
        print("1. Create a backup file with _ori suffix")
        print("2. Patch the original file directly")
        print("3. Apply privacy protection while preserving AI functionality")
        sys.exit(1)

    input_file = sys.argv[1]
    patch_mode = sys.argv[2] if len(sys.argv) > 2 else "random"

    success = aug_cleaner(input_file, patch_mode)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
