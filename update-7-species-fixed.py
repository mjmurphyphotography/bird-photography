#!/usr/bin/env python3
"""Update 7 species pages with descriptions, fun facts, and images - FIXED VERSION."""

import os
import shutil
import re
from pathlib import Path

# Species data with descriptions, fun facts, and metadata
SPECIES_DATA = {
    'acorn-woodpecker': {
        'common_name': 'Acorn Woodpecker',
        'scientific_name': 'Melanerpes formicivorus',
        'ebird_code': 'acowoo',
        'description': "A striking black-and-white woodpecker with a bold red crown, the Acorn Woodpecker is best known for its social behavior and clever food storage habits. It thrives in oak woodlands where acorns are plentiful.",
        'fun_facts': [
            "Masters of storage: They drill thousands of holes to store acorns in 'granary trees.'",
            "Highly social: Families live in cooperative groups and help raise young together.",
            "Memory experts: They remember the locations of vast numbers of stored acorns.",
            "Busy year-round: Granary maintenance never really stops."
        ]
    },
    'altamira-oriole': {
        'common_name': 'Altamira Oriole',
        'scientific_name': 'Icterus gularis',
        'ebird_code': 'altori',
        'description': "Large, bold, and unmistakable, the Altamira Oriole features bright orange underparts contrasted with black wings and back. Its rich, whistled song carries through tropical woodlands and river corridors.",
        'fun_facts': [
            "Largest U.S. oriole: It's the biggest oriole species found in the United States.",
            "Impressive nests: Builds long, hanging pouch nests that sway in the breeze.",
            "Powerful voice: Its song is loud, slow, and flute-like.",
            "Border specialty: Found mostly in southern Texas near the Rio Grande."
        ]
    },
    'american-redstart': {
        'common_name': 'American Redstart',
        'scientific_name': 'Setophaga ruticilla',
        'ebird_code': 'amered',
        'description': "Small, energetic, and constantly in motion, the American Redstart flashes bright orange (male) or yellow (female) patches as it flits through trees catching insects.",
        'fun_facts': [
            "Flash-and-chase: Uses wing and tail flashes to startle insects into flight.",
            "Nonstop motion: Rarely stays still for long.",
            "Long traveler: Migrates between North America and Central or South America.",
            "Bold for its size: Despite being small, it's very territorial."
        ]
    },
    'american-tree-sparrow': {
        'common_name': 'American Tree Sparrow',
        'scientific_name': 'Spizelloides arborea',
        'ebird_code': 'ametsp',
        'description': "A winter visitor with warm brown tones, a rusty cap, and a small dark spot on its chest, the American Tree Sparrow brings life to open fields and brushy edges during colder months.",
        'fun_facts': [
            "Cold-weather sparrow: Breeds in the far north and winters in the U.S.",
            "Seed specialist: Feeds heavily on seeds during winter.",
            "Sweet song: Delivers a clear, musical tune despite its subtle appearance.",
            "Ground forager: Often feeds by hopping along the ground."
        ]
    },
    'belted-kingfisher': {
        'common_name': 'Belted Kingfisher',
        'scientific_name': 'Megaceryle alcyon',
        'ebird_code': 'belkin',
        'description': "Stocky and unmistakable, the Belted Kingfisher patrols waterways before plunging headfirst to catch fish. Its rattling call is often heard before the bird is seen.",
        'fun_facts': [
            "Fishing dives: Hunts by hovering, then diving straight into the water.",
            "Reverse fashion: Females are more colorful than males.",
            "Tunnel nester: Digs nesting burrows into sandy banks.",
            "Territorial: Fiercely defends favorite fishing spots."
        ]
    },
    'anhinga': {
        'common_name': 'Anhinga',
        'scientific_name': 'Anhinga anhinga',
        'ebird_code': 'anhing',
        'description': "Often seen drying its wings in the sun, the Anhinga is a sleek waterbird with a long neck and dagger-like bill, earning it the nickname snakebird.",
        'fun_facts': [
            "Wet feathers: Lacks waterproofing, helping it dive more easily.",
            "Spear fisher: Stabs fish underwater instead of scooping them.",
            "Sun worshipper: Frequently spreads wings to dry after swimming.",
            "Stealth swimmer: Often swims with only its neck visible above water."
        ]
    },
    'american-avocet': {
        'common_name': 'American Avocet',
        'scientific_name': 'Recurvirostra americana',
        'ebird_code': 'ameavo',
        'description': "Elegant and eye-catching, the American Avocet is a tall shorebird with long blue-gray legs and a graceful, upturned bill. During breeding season, its rusty-orange head adds extra flair.",
        'fun_facts': [
            "Sweeping feeder: Uses side-to-side motions to stir up food in shallow water.",
            "Seasonal makeover: Plumage changes dramatically between breeding and non-breeding seasons.",
            "Social birds: Often feed and rest in flocks.",
            "Strong defenders: Will boldly chase predators away from nesting areas."
        ]
    }
}

def extract_state_from_filename(filename):
    """Extract state name from filename."""
    # Remove extension and numbers
    base = filename.replace('.jpg', '').replace('.JPG', '')
    # Remove trailing numbers
    state = re.sub(r'\d+$', '', base)
    # Capitalize properly
    return state.capitalize()

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

    print(f"  Copied {len(images)} images for {species_slug}")

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

def update_species_page(species_slug):
    """Update a species page with new content."""
    data = SPECIES_DATA[species_slug]

    print(f"\nUpdating {data['common_name']}...")

    # Get images
    images = get_images_for_species(species_slug)
    if not images:
        print(f"  Warning: No images found for {species_slug}")
        return

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
    html = html.replace('<h2>About This Species</h2>',
                       f'<h2>About This Species</h2>')
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

# Update all 7 species
for species_slug in SPECIES_DATA.keys():
    update_species_page(species_slug)

print("\n✓ Updated all 7 species pages")
