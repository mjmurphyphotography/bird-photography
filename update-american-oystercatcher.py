#!/usr/bin/env python3
"""Update American Oystercatcher species page with description, fun facts, and images."""

import os
import shutil
import re
from pathlib import Path

# Species data
SPECIES_DATA = {
    'common_name': 'American Oystercatcher',
    'scientific_name': 'Haematopus palliatus',
    'ebird_code': 'ameoys',
    'description': "This bold coastal shorebird stands out with its black-and-white body, long pink legs, and thick orange bill perfectly designed for prying open shellfish.",
    'fun_facts': [
        "Specialized bill: Strong enough to crack open oysters and clams.",
        "Long-lived: Can live for several decades.",
        "Vocal alarms: Loud calls warn others of danger.",
        "Beach loyalists: Often return to the same nesting areas year after year."
    ]
}

def extract_state_from_filename(filename):
    """Extract state name from filename."""
    # Remove extension and numbers
    base = filename.replace('.jpg', '').replace('.JPG', '')
    # Remove trailing numbers
    state = re.sub(r'\d+$', '', base)
    # Handle hyphenated states like "new-jersey" -> "New Jersey"
    words = state.split('-')
    return ' '.join(word.capitalize() for word in words)

def get_images_for_species(species_slug):
    """Get list of images for a species from source directory."""
    source_dir = Path.home() / 'Desktop' / 'species-pages' / species_slug
    if not source_dir.exists():
        return []

    images = []
    for img_file in sorted(source_dir.glob('*.jpg')) + sorted(source_dir.glob('*.JPG')):
        state = extract_state_from_filename(img_file.name)
        images.append({
            'filename': img_file.name,
            'state': state,
            'source_path': img_file
        })
    return images

def copy_species_images(species_slug, images):
    """Copy images to species directories."""
    # Create directories if they don't exist
    species_dir = Path('images/species') / species_slug
    thumbs_dir = species_dir / 'thumbs'
    species_dir.mkdir(parents=True, exist_ok=True)
    thumbs_dir.mkdir(exist_ok=True)

    for img in images:
        # Copy to both full and thumbs directories
        dest_full = species_dir / img['filename']
        dest_thumb = thumbs_dir / img['filename']

        shutil.copy2(img['source_path'], dest_full)
        shutil.copy2(img['source_path'], dest_thumb)

    print(f"  Copied {len(images)} images")

def generate_gallery_items(species_slug, images):
    """Generate HTML for gallery items."""
    items = []
    for img in images:
        item = f'''            <div class="gallery-item">
                <img src="images/species/{species_slug}/thumbs/{img['filename']}" alt="{img['state']}">
                <div class="gallery-caption">{img['state']}</div>
            </div>'''
        items.append(item)
    return '\n'.join(items)

def generate_fun_facts_list(fun_facts):
    """Generate HTML for fun facts list."""
    items = []
    for fact in fun_facts:
        # Parse "Title: Description" format
        if ':' in fact:
            title, desc = fact.split(':', 1)
            items.append(f'                    <li><strong>{title}:</strong>{desc}</li>')
        else:
            items.append(f'                    <li>{fact}</li>')
    return '\n'.join(items)

def update_species_page():
    """Update American Oystercatcher species page."""
    species_slug = 'american-oystercatcher'
    data = SPECIES_DATA

    print(f"\nUpdating {data['common_name']}...")

    # Get images
    images = get_images_for_species(species_slug)
    if not images:
        print(f"  Warning: No images found for {species_slug}")
        return

    print(f"  Found {len(images)} images")

    # Copy images to proper directories
    copy_species_images(species_slug, images)

    # Read the carolina-wren.html template
    with open('carolina-wren.html', 'r') as f:
        html = f.read()

    # Replace title
    html = html.replace('<title>Carolina Wren - Species Gallery</title>',
                       f'<title>{data["common_name"]} - Species Gallery</title>')

    # Replace header
    html = html.replace('<h1>Carolina Wren</h1>', f'<h1>{data["common_name"]}</h1>')
    html = html.replace('<p class="scientific-name">Thryothorus ludovicianus</p>',
                       f'<p class="scientific-name">{data["scientific_name"]}</p>')
    html = html.replace('https://ebird.org/species/carwre',
                       f'https://ebird.org/species/{data["ebird_code"]}')

    # Replace About section
    old_desc = 'The Carolina Wren is a small but bold songbird with a warm rusty-brown back and buff-colored underparts. Its signature white eyebrow stripe and upright tail give it a distinctive appearance. Despite its size, this wren delivers loud, ringing songs that echo through backyards and woodlands year-round.'
    html = html.replace(old_desc, data['description'])

    # Replace Fun Facts
    old_facts = '''                    <li><strong>Powerful voice:</strong> One of the loudest birds for its size, singing throughout the year.</li>
                    <li><strong>Creative nester:</strong> Known for building nests in unusual places like mailboxes, flower pots, and boots.</li>
                    <li><strong>Year-round resident:</strong> Non-migratory in most of its range, staying put through all seasons.</li>
                    <li><strong>Pair bonding:</strong> Mates often stay together year-round and sing duets.</li>
                    <li><strong>Curious explorer:</strong> Actively investigates nooks and crannies searching for insects and spiders.</li>'''
    new_facts = generate_fun_facts_list(data['fun_facts'])
    html = html.replace(old_facts, new_facts)

    # Replace gallery
    old_gallery_start = html.find('<div class="gallery">')
    old_gallery_end = html.find('</div>\n\n        <!-- Location Appearances Section -->', old_gallery_start)
    if old_gallery_start != -1 and old_gallery_end != -1:
        new_gallery = '<div class="gallery">\n' + generate_gallery_items(species_slug, images) + '\n        '
        html = html[:old_gallery_start] + new_gallery + html[old_gallery_end:]

    # Write the updated HTML
    with open(f'{species_slug}.html', 'w') as f:
        f.write(html)

    print(f"  ✓ Updated {species_slug}.html with {len(images)} images")

update_species_page()
print("\n✓ Updated American Oystercatcher page")
