#!/usr/bin/env python3
"""Add bird photo gallery to Montour Preserve location page."""

import os
import shutil
import re
from pathlib import Path

def extract_species_name(filename):
    """Extract species name from filename."""
    # Remove extension and numbers
    name = filename.replace('.jpg', '').replace('.JPG', '')
    name = re.sub(r'\d+$', '', name)  # Remove trailing numbers
    name = name.strip()

    # Handle possessives
    if "wilson's" in name.lower():
        parts = name.split('-')
        words = []
        for part in parts:
            if part.lower() == "wilson's":
                words.append("Wilson's")
            else:
                words.append(part.capitalize())
        return ' '.join(words)

    # Fix known typos
    if 'easern' in name.lower():
        name = name.replace('easern', 'eastern')

    # Convert to title case
    words = name.split('-')
    return ' '.join(word.capitalize() for word in words)

# Copy images
src_dir = Path.home() / 'Desktop' / 'species-locations ' / 'montour-preserve'
dest_dir = Path('images/locations/montour-preserve')
dest_dir.mkdir(parents=True, exist_ok=True)

images = sorted(src_dir.glob('*.jpg'))
print(f"Found {len(images)} images")

# Copy images and build gallery HTML
gallery_items = []
for img_path in images:
    # Create clean destination filename (remove spaces, standardize)
    dest_name = img_path.name.replace(' ', '-').lower()
    dest_path = dest_dir / dest_name

    shutil.copy2(img_path, dest_path)
    print(f"✓ Copied: {img_path.name}")

    species_name = extract_species_name(img_path.name)

    gallery_items.append(f'''            <div class="gallery-item">
                <img src="images/locations/montour-preserve/{dest_name}"
                     alt="{species_name}"
                     loading="lazy">
                <div class="gallery-caption">
                    <span class="species">{species_name}</span>
                </div>
            </div>''')

# Generate gallery HTML
gallery_html = '\n'.join(gallery_items)

print(f"\n✓ Copied {len(images)} images")
print(f"\nGallery HTML ready with {len(gallery_items)} items")
print("\nNow updating location-montour-preserve.html...")

# Read the current HTML
with open('location-montour-preserve.html', 'r') as f:
    html = f.read()

# Replace the "coming soon" section with the gallery
old_section = '''        <a href="locations.html" class="back-link">← Back to All Locations</a>
        <p class="coming-soon">Gallery coming soon...</p>'''

new_section = f'''        <a href="locations.html" class="back-link">← Back to All Locations</a>
        <div class="gallery">
{gallery_html}
        </div>'''

html = html.replace(old_section, new_section)

# Write updated HTML
with open('location-montour-preserve.html', 'w') as f:
    f.write(html)

print("✓ Updated location-montour-preserve.html with gallery")
