#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import os

def aug_cleaner(input_file, output_file=None):
    """
    Find async callApi function in JS file and insert patch code

    Args:
        input_file: Input JS file path
        output_file: Output JS file path, if None will add _patched to original filename
    """
    
    # Patch code
    patch_code = 'if (typeof s === "string" && (s.startsWith("report-") || s.startsWith("record-"))) { return { success: true }; } const chars = "0123456789abcdef"; let randSessionId = ""; for (let i = 0; i < 36; i++) { randSessionId += i === 8 || i === 13 || i === 18 || i === 23 ? "-" : i === 14 ? "4" : i === 19 ? chars[8 + Math.floor(4 * Math.random())] : chars[Math.floor(16 * Math.random())]; } this.sessionId = randSessionId; this._userAgent = "";'
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} does not exist")
        return False
    
    # Read original file content
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error: Cannot read file {input_file}: {e}")
        return False
    
    # Find async callApi function pattern
    # Match: async callApi(parameters){
    pattern = r'(async\s+callApi\s*\([^)]*\)\s*\{)'

    match = re.search(pattern, content)
    if not match:
        print("Error: async callApi function not found")
        return False

    # Find function start position
    func_start = match.end()

    # Insert patch code after function start
    patched_content = content[:func_start] + patch_code + content[func_start:]

    # Determine output filename
    if output_file is None:
        base_name, ext = os.path.splitext(input_file)
        output_file = f"{base_name}_patched{ext}"

    # Write new file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(patched_content)
        print(f"Success: Patch applied, new file saved as {output_file}")
        return True
    except Exception as e:
        print(f"Error: Cannot write file {output_file}: {e}")
        return False

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python aug_cleaner.py <input_js_file> [output_js_file]")
        print("Example: python aug_cleaner.py extension.js")
        print("Example: python aug_cleaner.py extension.js extension_patched.js")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    success = aug_cleaner(input_file, output_file)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
