#!/usr/bin/env python3
"""Update species.html landing page to include all species from species-thumbs folder."""

import os
import re

def filename_to_display_name(filename):
    """Convert filename to proper display name."""
    # Remove .jpg extension
    name = filename.replace('.jpg', '')

    # Dictionary of species that need hyphens preserved in their display names
    hyphenated_species = {
        'black-and-white-warbler': 'Black-and-white Warbler',
        'black-capped-chickadee': 'Black-capped Chickadee',
        'black-crested-titmouse': 'Black-crested Titmouse',
        'black-throated-green-warbler': 'Black-throated Green Warbler',
        'black-throated-sparrow': 'Black-throated Sparrow',
        'blue-gray-gnatcatcher': 'Blue-gray Gnatcatcher',
        'broad-billed-hummingbird': 'Broad-billed Hummingbird',
        'chestnut-sided-warbler': 'Chestnut-sided Warbler',
        'dark-eyed-junco': 'Dark-eyed Junco',
        'double-crested-cormorant': 'Double-crested Cormorant',
        'eastern-wood-pewee': 'Eastern Wood-Pewee',
        'golden-crowned-kinglet': 'Golden-crowned Kinglet',
        'golden-fronted-woodpecker': 'Golden-fronted Woodpecker',
        'red-bellied-woodpecker': 'Red-bellied Woodpecker',
        'red-headed-woodpecker': 'Red-headed Woodpecker',
        'red-tailed-hawk': 'Red-tailed Hawk',
        'red-winged-blackbird': 'Red-winged Blackbird',
        'ruby-crowned-kinglet': 'Ruby-crowned Kinglet',
        'white-breasted-nuthatch': 'White-breasted Nuthatch',
        'white-throated-sparrow': 'White-throated Sparrow',
        'yellow-eyed-junco': 'Yellow-eyed Junco',
        'yellow-rumped-warbler': 'Yellow-rumped Warbler',
        'yellow-throated-warbler': 'Yellow-throated Warbler',
    }

    # Check if this species needs special hyphenation
    if name in hyphenated_species:
        return hyphenated_species[name]

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
