#!/usr/bin/env python3
"""Update species.html landing page to include all species from species-thumbs folder."""

import os
import re

def filename_to_display_name(filename):
    """Convert filename to proper display name."""
    # Remove .jpg extension
    name = filename.replace('.jpg', '')

    # Split by hyphens and capitalize each word
    words = name.split('-')

    # Handle special cases
    display_name = []
    for i, word in enumerate(words):
        # Special handling for specific cases
        if word.lower() == 'and':
            display_name.append('and')
        elif word.lower() in ['a', 'the']:
            display_name.append(word.lower())
        else:
            display_name.append(word.capitalize())

    return ' '.join(display_name)

# Get all species thumbnails
thumbs_dir = 'images/species-thumbs'
species_files = sorted([f for f in os.listdir(thumbs_dir) if f.endswith('.jpg')])

print(f"Found {len(species_files)} species thumbnails")

# Generate gallery HTML
gallery_html = []
for species_file in species_files:
    species_slug = species_file.replace('.jpg', '')
    species_name = filename_to_display_name(species_file)

    # Fix known naming issues
    if species_slug == 'scarlot-tanager':
        species_name = 'Scarlet Tanager'
        species_slug = 'scarlet-tanager'

    gallery_item = f'''            <a href="{species_slug}.html" class="gallery-item">
                <img src="images/species-thumbs/{species_file}" alt="{species_name}">
                <div class="gallery-overlay">
                    <h3>{species_name}</h3>
                    <p>Click to view gallery</p>
                </div>
            </a>'''

    gallery_html.append(gallery_item)

# Read current species.html
with open('species.html', 'r') as f:
    content = f.read()

# Find and replace the gallery section
gallery_start = content.find('        <div class="gallery">')
gallery_end = content.find('        </div>\n    </section>', gallery_start)

if gallery_start == -1 or gallery_end == -1:
    print("Error: Could not find gallery section")
    exit(1)

# Rebuild the page with new gallery
new_content = (
    content[:gallery_start + len('        <div class="gallery">')] + '\n' +
    '\n'.join(gallery_html) + '\n' +
    content[gallery_end:]
)

# Write updated content
with open('species.html', 'w') as f:
    f.write(new_content)

print(f"✓ Updated species.html with {len(species_files)} species")
