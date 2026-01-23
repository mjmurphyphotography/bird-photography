#!/usr/bin/env python3
"""Add bird photo gallery to Magee Marsh location page."""

import os
import shutil
from pathlib import Path

def filename_to_species_name(filename):
    """Convert filename to proper species name."""
    # Remove extension and trailing numbers
    name = filename.replace('.jpg', '').replace('.JPG', '')

    # Remove trailing numbers (e.g., "warbler2" -> "warbler")
    import re
    name = re.sub(r'\d+$', '', name)

    # Split by hyphens and capitalize each word
    words = name.split('-')
    return ' '.join(word.capitalize() for word in words)

# Source and destination directories
source_dir = Path("/Users/michaelmurphy1/Desktop/species-locations /magee-marsh")
dest_dir = Path("images/locations/magee-marsh")

# Create destination directory
dest_dir.mkdir(parents=True, exist_ok=True)

# Get all image files
images = sorted(source_dir.glob("*.jpg")) + sorted(source_dir.glob("*.JPG"))

print(f"Found {len(images)} images in Magee Marsh folder")

# Copy images and prepare gallery data
gallery_items = []
for img_file in images:
    # Copy to destination
    dest_file = dest_dir / img_file.name
    shutil.copy2(img_file, dest_file)

    # Get species name
    species_name = filename_to_species_name(img_file.name)

    # Create gallery HTML
    gallery_item = f'''            <div class="gallery-item">
                <img src="images/locations/magee-marsh/{img_file.name}" alt="{species_name}">
                <div class="gallery-caption">
                    <div class="species">{species_name}</div>
                </div>
            </div>'''

    gallery_items.append(gallery_item)
    print(f"  Copied: {img_file.name} -> {species_name}")

# Read the location page
with open('location-magee-marsh.html', 'r') as f:
    html = f.read()

# Replace the "coming soon" message with the gallery
old_gallery = '        <a href="locations.html" class="back-link">← Back to All Locations</a>\n        <p class="coming-soon">Gallery coming soon...</p>'

new_gallery = '''        <a href="locations.html" class="back-link">← Back to All Locations</a>
        <div class="gallery">
''' + '\n'.join(gallery_items) + '''
        </div>'''

html = html.replace(old_gallery, new_gallery)

# Write updated HTML
with open('location-magee-marsh.html', 'w') as f:
    f.write(html)

print(f"\n✓ Updated location-magee-marsh.html with {len(images)} bird photos")
