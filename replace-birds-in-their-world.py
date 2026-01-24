#!/usr/bin/env python3
"""Replace all Birds in Their World images."""

import os
import shutil
import re
from pathlib import Path

def parse_filename(filename):
    """Parse species-location-title.jpg format."""
    # Remove extension and trailing numbers
    name = filename.replace('.jpg', '').replace('.JPG', '')
    name = re.sub(r'\d+$', '', name)  # Remove trailing numbers like 2, 3, etc.

    # Manual parsing for each species
    filename_map = {
        'american-goldfinch-leaser-lake-hanfging-on':
            ('American Goldfinch', 'Leaser Lake', 'Hanging On'),
        'american-herring-gull-sunrise-reflection':
            ('American Herring Gull', 'Sunrise', 'Reflection'),
        'american-oystercatcher-barnegat-state-park-over-the-dune':
            ('American Oystercatcher', 'Barnegat State Park', 'Over the Dune'),
        'american-robin-leaser-lake-spring-emergence':
            ('American Robin', 'Leaser Lake', 'Spring Emergence'),
        'bald-eagles-rose-valley-lake-One-Feeds-One-Waits-on-the-frozen-lake':
            ('Bald Eagles', 'Rose Valley Lake', 'One Feeds, One Waits on the Frozen Lake'),
        'black-and-white-warbler-PA-state-gamelands-black-and-white-singer':
            ('Black-and-white Warbler', 'PA State Gamelands', 'Black and White Singer'),
        'brant-barnegat-lighthouse-state-park-between-and-sea':
            ('Brant', 'Barnegat Lighthouse State Park', 'Between Land and Sea'),
        'clapper-rail-forsythe-wildlife-preserve-Marsh-Passage':
            ('Clapper Rail', 'Forsythe Wildlife Preserve', 'Marsh Passage'),
        'common-raven-acadia-national-park-On-the-Edge-of the-Fog':
            ('Common Raven', 'Acadia National Park', 'On the Edge of the Fog'),
        'dark-eyed-junco-leaser-lake-evergreen-pause':
            ('Dark-eyed Junco', 'Leaser Lake', 'Evergreen Pause'),
        'dickcissel-northern-ohio-grassland-above-the-meadow':
            ('Dickcissel', 'Northern Ohio Grassland', 'Above the Meadow'),
        'eastern-meadowlark-amish-pond-morning watch':
            ('Eastern Meadowlark', 'Amish Pond', 'Morning Watch'),
        'great-egret-rio-grande-river-Still-Watch':
            ('Great Egret', 'Rio Grande River', 'Still Watch'),
        'horned-lark-luzerne-county-farm-winter-survival':
            ('Horned Lark', 'Luzerne County Farm', 'Winter Survival'),
        'indigo-bunting-leaser-lake-Unassuming-Beauty':
            ('Indigo Bunting', 'Leaser Lake', 'Unassuming Beauty'),
        'least-tern-barnegat-lighthouse-state-park-first-catch':
            ('Least Tern', 'Barnegat Lighthouse State Park', 'First Catch'),
        'little-blue-heron-rio-grande-valley-afternoon-pause':
            ('Little Blue Heron', 'Rio Grande Valley', 'Afternoon Pause'),
        'northern-harrier-susquehanna-riverlands-hunter-in-the-snow':
            ('Northern Harrier', 'Susquehanna Riverlands', 'Hunter in the Snow'),
        'northern-house-wren-leaser-lake-rooftop-perch':
            ('Northern House Wren', 'Leaser Lake', 'Rooftop Perch'),
        'orchard-oriole-leaser-lake-hidden-in-green':
            ('Orchard Oriole', 'Leaser Lake', 'Hidden in Green'),
        'piping-plover-barnegat-lighthouse-state-park-in-pursuit':
            ('Piping Plover', 'Barnegat Lighthouse State Park', 'In Pursuit'),
        'prairie-warbler-beltzville-state-park-among-the-blossoms':
            ('Prairie Warbler', 'Beltzville State Park', 'Among the Blossoms'),
        'red-headed-woodpecker-magee-marsh-between-the-trunks':
            ('Red-headed Woodpecker', 'Magee Marsh', 'Between the Trunks'),
        'red-winged-blackbird-amish-pond-balancing-act':
            ('Red-winged Blackbird', 'Amish Pond', 'Balancing Act'),
        'red-winged-blackbird-amish-pond-Marsh-Sentinel':
            ('Red-winged Blackbird', 'Amish Pond', 'Marsh Sentinel'),
        'short-eared-owl-rodino-farm-hidden-hunter':
            ('Short-eared Owl', 'Rodino Farm', 'Hidden Hunter'),
        'snow-buntings-plymouth-flats-Winter-Perch':
            ('Snow Buntings', 'Plymouth Flats', 'Winter Perch'),
        'spotted-sandpiper-leaser-lake-low-in-the-grass':
            ('Spotted Sandpiper', 'Leaser Lake', 'Low in the Grass'),
        'spotted-sandpiper-susquehanna-wetlands-log-lookout':
            ('Spotted Sandpiper', 'Susquehanna Wetlands', 'Log Lookout'),
        'swamp-sparrow-leaser-lake-picking-at-the-cattails':
            ('Swamp Sparrow', 'Leaser Lake', 'Picking at the Cattails'),
        'western-cattle-egret-rio-grande-river-an-unlikely-trio':
            ('Western Cattle Egret', 'Rio Grande River', 'An Unlikely Trio'),
        'white-throated-sparrow-susquehanna-wetlands-among-the-winterberries':
            ('White-throated Sparrow', 'Susquehanna Wetlands', 'Among the Winterberries'),
        'wood-ducks-forsythe-wildlife-preserve-through-the-reeds':
            ('Wood Ducks', 'Forsythe Wildlife Preserve', 'Through the Reeds'),
        'yellow-rumoed-warbler-leaser-lake-hidden-in-the-pines':
            ('Yellow-rumped Warbler', 'Leaser Lake', 'Hidden in the Pines'),
    }

    if name in filename_map:
        return filename_map[name]

    return "Unknown Species", "Unknown Location", "Untitled"

# Clear existing images and create fresh directory
dest_dir = Path('images/birds-in-their-world')
if dest_dir.exists():
    for img in dest_dir.glob('*.jpg'):
        img.unlink()
    print("✓ Cleared existing images")

dest_dir.mkdir(parents=True, exist_ok=True)

# Copy all images from source
src_dir = Path.home() / 'Desktop' / 'birds-in-their-world'
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

# Update the CSS to make images 25% smaller (75% of original size)
# Find the .world-image style and update width
old_image_style = '''        .world-image {
            width: 100%;
            height: auto;'''

new_image_style = '''        .world-image {
            width: 75%;
            height: auto;
            margin: 0 auto;'''

html = html.replace(old_image_style, new_image_style)

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

    print(f"\n✓ Updated birds-in-their-world.html with {len(gallery_items)} images at 75% size!")
else:
    print("\n✗ Could not find gallery section markers in HTML")
