#!/usr/bin/env python3
"""Remove duplicate lightbox structure from head section of state pages."""

import re
import os

# List of state page files
state_files = [
    'birds-in-their-world-arizona.html',
    'birds-in-their-world-california.html',
    'birds-in-their-world-delaware.html',
    'birds-in-their-world-florida.html',
    'birds-in-their-world-maine.html',
    'birds-in-their-world-new-jersey.html',
    'birds-in-their-world-new-york.html',
    'birds-in-their-world-ohio.html',
    'birds-in-their-world-pennsylvania.html',
    'birds-in-their-world-texas.html'
]

base_path = '/Users/michaelmurphy1/Desktop/bird-photography'

for filename in state_files:
    filepath = os.path.join(base_path, filename)

    if not os.path.exists(filepath):
        print(f"⚠️  File not found: {filename}")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match the lightbox HTML in the head section
    # It appears after the Google Analytics script and before the next <script> tag
    pattern = r'</script>    <!-- Lightbox -->\s*<div id="lightbox" class="lightbox"[^>]*>.*?</div>\s*\n\s*\n\s*<script>'

    # Replace with just the script tags (removing the lightbox HTML between them)
    replacement = r'</script>\n\n    <script>'

    # Count matches before replacement
    matches = len(re.findall(pattern, content, re.DOTALL))

    if matches > 0:
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Fixed {filename}")
    else:
        print(f"ℹ️  No lightbox in head found in {filename}")

print("\n✅ All state pages processed!")
print("  • Removed duplicate lightbox HTML from head section")
print("  • Kept proper lightbox HTML in body section")
