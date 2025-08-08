#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import os

def aug_cleaner(input_file):
    """
    Find async callApi function in JS file and insert patch code
    Automatically creates backup and patches the original file

    Args:
        input_file: Input JS file path to patch
    """

    # Patch code
    patch_code = 'if (typeof s === "string" && (s.startsWith("report-") || s.startsWith("record-"))) { return { success: true }; } const chars = "0123456789abcdef"; let randSessionId = ""; for (let i = 0; i < 36; i++) { randSessionId += i === 8 || i === 13 || i === 18 || i === 23 ? "-" : i === 14 ? "4" : i === 19 ? chars[8 + Math.floor(4 * Math.random())] : chars[Math.floor(16 * Math.random())]; } this.sessionId = randSessionId; this._userAgent = "";'

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

    # Check if already patched
    if patch_code in content:
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
        print("Privacy protection enabled - all telemetry blocked!")
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
        print("Usage: python aug_cleaner.py <input_js_file>")
        print("Example: python aug_cleaner.py ~/.vscode/extensions/augment.vscode-augment-*/out/extension.js")
        print("")
        print("This will:")
        print("1. Create a backup file with _ori suffix")
        print("2. Patch the original file directly")
        print("3. Block all telemetry while preserving AI functionality")
        sys.exit(1)

    input_file = sys.argv[1]

    success = aug_cleaner(input_file)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
