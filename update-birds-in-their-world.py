#!/usr/bin/env python3
"""Update Birds in Their World page with all images."""

import os
import shutil
import re
from pathlib import Path

def parse_filename(filename):
    """Parse species-location-title.jpg format."""
    # Remove extension
    name = filename.replace('.jpg', '').replace('.JPG', '')

    # Manual parsing for each specific file
    filename_map = {
        'american-oystercatcher-barnegat-state-park-over-the-dune':
            ('American Oystercatcher', 'Barnegat State Park', 'Over the Dune'),
        'bald-eagles-rose-valley-lake-One-Feeds-One-Waits-on-the-frozen-lake':
            ('Bald Eagles', 'Rose Valley Lake', 'One Feeds, One Waits on the Frozen Lake'),
        'brant-barnegat-lighthouse-state-park-between-and-sea':
            ('Brant', 'Barnegat Lighthouse State Park', 'Between Land and Sea'),
        'eastern-meadowlark-amish-pond-morning watch':
            ('Eastern Meadowlark', 'Amish Pond', 'Morning Watch'),
        'indigo-bunting-leaser-lake-Unassuming-Beauty':
            ('Indigo Bunting', 'Leaser Lake', 'Unassuming Beauty'),
        'least-tern-barnegat-lighthouse-state-park-first-catch':
            ('Least Tern', 'Barnegat Lighthouse State Park', 'First Catch'),
        'northern-house-wren-leaser-lake-rooftop-perch':
            ('Northern House Wren', 'Leaser Lake', 'Rooftop Perch'),
        'orchard-oriole-leaser-lake-hidden-in-green':
            ('Orchard Oriole', 'Leaser Lake', 'Hidden in Green'),
        'piping-plover-barnegat-lighthouse-state-park-in-persute':
            ('Piping Plover', 'Barnegat Lighthouse State Park', 'In Pursuit'),
        'red-winged-blackbird-amish-pond-Marsh-Sentinel':
            ('Red-winged Blackbird', 'Amish Pond', 'Marsh Sentinel'),
        'snow-buntings-plymouth-flats-Winter-Perch':
            ('Snow Buntings', 'Plymouth Flats', 'Winter Perch'),
        'song-sparrow-francis-slocum-state-park-hidden-in-the reeds':
            ('Song Sparrow', 'Francis Slocum State Park', 'Hidden in the Reeds'),
        'western-cattle-egret-rio-grande-river-an-unlikely-trio':
            ('Western Cattle Egret', 'Rio Grande River', 'An Unlikely Trio'),
        'white-throated-sparrow-susquehanna-wetlands-among-the-winterberries':
            ('White-throated Sparrow', 'Susquehanna Wetlands', 'Among the Winterberries'),
        'yellow-rumoed-warbler-leaser-lake-hidden-in-the-pines':
            ('Yellow-rumped Warbler', 'Leaser Lake', 'Hidden in the Pines'),
    }

    if name in filename_map:
        return filename_map[name]

    return "Unknown Species", "Unknown Location", "Untitled"

# Create directory
Path('images/birds-in-their-world').mkdir(parents=True, exist_ok=True)

# Copy all images
src_dir = Path.home() / 'Desktop' / 'birds-in-their-world'
dest_dir = Path('images/birds-in-their-world')

images = sorted(src_dir.glob('*.jpg'))
print(f"Found {len(images)} images")

gallery_items = []
for img_path in images:
    if img_path.name.startswith('.'):
        continue

    # Copy image
    dest_path = dest_dir / img_path.name
    shutil.copy2(img_path, dest_path)
    print(f"✓ Copied: {img_path.name}")

    species, location, title = parse_filename(img_path.name)
    print(f"   → {species} | {location} | {title}")

    gallery_items.append({
        'filename': img_path.name,
        'species': species,
        'location': location,
        'title': title
    })

print(f"\n✓ Copied {len(gallery_items)} images")

# Build gallery HTML
gallery_html = []
for item in gallery_items:
    gallery_html.append(f'''            <div class="world-item">
                <img src="images/birds-in-their-world/{item['filename']}"
                     alt="{item['species']} - {item['title']}"
                     class="world-image"
                     loading="lazy">
                <div class="world-caption">
                    <div class="world-species">{item['species']}</div>
                    <div class="world-location">{item['location']}</div>
                    <div class="world-title">{item['title']}</div>
                </div>
            </div>''')

gallery_section = '\n'.join(gallery_html)

# Read current HTML
with open('birds-in-their-world.html', 'r') as f:
    html = f.read()

# Find and replace the gallery section
start_marker = '<div class="world-gallery">'
end_marker = '</div>\n    </section>'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker, start_idx)

if start_idx != -1 and end_idx != -1:
    new_gallery = f'''{start_marker}
{gallery_section}
        {end_marker}'''

    html = html[:start_idx] + new_gallery + html[end_idx + len(end_marker):]

    with open('birds-in-their-world.html', 'w') as f:
        f.write(html)

    print(f"\n✓ Updated birds-in-their-world.html with {len(gallery_items)} images!")
else:
    print("\n✗ Could not find gallery section markers in HTML")
