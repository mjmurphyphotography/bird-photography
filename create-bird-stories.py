#!/usr/bin/env python3
"""Create Bird Stories feature with landing page and story pages."""

import os
import shutil
from pathlib import Path

def parse_story_filename(filename):
    """Parse species-location-action.jpg format."""
    # Remove extension
    name = filename.replace('.jpg', '').replace('.JPG', '')

    # Split by hyphens
    parts = name.split('-')

    if len(parts) >= 3:
        # Find where location starts (usually after species name)
        # Species names can be multi-word like "great-blue-heron"
        # Locations can be multi-word like "montour-preserve"
        # Actions can be multi-word like "ice-fishing"

        # For this specific case: great-blue-heron-montour-peserve-ice-fishing
        species = ' '.join(parts[0:3]).title()  # Great Blue Heron
        location = ' '.join(parts[3:5]).title()  # Montour Preserve (with typo)
        action = ' '.join(parts[5:]).title()     # Ice Fishing

        # Fix known location typo
        if 'Peserve' in location:
            location = location.replace('Peserve', 'Preserve')

        return species, location, action

    return "Unknown Species", "Unknown Location", "Unknown Action"

# Create directories
Path('images/bird-stories').mkdir(parents=True, exist_ok=True)
Path('images/bird-stories/great-blue-heron').mkdir(parents=True, exist_ok=True)

# Copy landing thumbnail
landing_src = Path.home() / 'Desktop' / 'bird-stories-landing'
landing_thumb = landing_src / 'great-blue-heron-montour-peserve-ice-fishing.jpg'
if landing_thumb.exists():
    shutil.copy2(landing_thumb, 'images/bird-stories/great-blue-heron-montour-preserve-testing-ice.jpg')
    print("✓ Copied landing thumbnail")

# Copy story images
story_src = Path.home() / 'Desktop' / 'bird-stories-images' / 'great-blue-heron'
story_images = sorted(story_src.glob('*.jpg'))
for i, img in enumerate(story_images, 1):
    dest = Path('images/bird-stories/great-blue-heron') / f'testing-ice-{i}.jpg'
    shutil.copy2(img, dest)
    print(f"✓ Copied story image {i}: {img.name}")

print(f"\n✓ Set up Bird Stories images")

# Parse the thumbnail filename for display
species, location, action = parse_story_filename('great-blue-heron-montour-peserve-ice-fishing.jpg')
print(f"\nParsed story info:")
print(f"  Species: {species}")
print(f"  Location: {location}")
print(f"  Action: {action}")
