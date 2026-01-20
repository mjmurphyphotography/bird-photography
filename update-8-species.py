#!/usr/bin/env python3
"""Update 8 species pages with descriptions, fun facts, and images."""

import os
import shutil
import re
from pathlib import Path

# Species data with descriptions, fun facts, and metadata
SPECIES_DATA = {
    'black-crested-titmouse': {
        'common_name': 'Black-crested Titmouse',
        'scientific_name': 'Baeolophus atricristatus',
        'ebird_code': 'bkctit',
        'description': "Lively and curious, the Black-crested Titmouse sports a pointed crest and expressive face. It's often found hopping through trees in small, noisy groups.",
        'fun_facts': [
            "Chatty bird: Constantly calls while foraging.",
            "Smart forager: Stores seeds for later use.",
            "Acrobatic: Hangs upside down while feeding.",
            "Social: Often joins mixed-species flocks."
        ]
    },
    'broad-billed-hummingbird': {
        'common_name': 'Broad-billed Hummingbird',
        'scientific_name': 'Cynanthus latirostris',
        'ebird_code': 'bblhum',
        'description': "A jewel of the Southwest, the Broad-billed Hummingbird flashes emerald green with a vivid red bill, often seen hovering at flowers in desert canyons.",
        'fun_facts': [
            "Colorful bill: One of the few hummingbirds with a bright red bill.",
            "Hover expert: Can fly forward, backward, and straight up.",
            "Flower specialist: Feeds on nectar from tubular blooms.",
            "Rapid wings: Beats wings dozens of times per second."
        ]
    },
    'baltimore-oriole': {
        'common_name': 'Baltimore Oriole',
        'scientific_name': 'Icterus galbula',
        'ebird_code': 'balori',
        'description': "Brilliant orange and black, the Baltimore Oriole brings vivid color and rich song to treetops each spring. It favors open woodlands and shade trees.",
        'fun_facts': [
            "Hanging homes: Builds long, woven pouch nests high in trees.",
            "Fruit lover: Enjoys oranges, jelly, and nectar.",
            "Long-distance traveler: Migrates to Central America for winter.",
            "Musical voice: Its flute-like song is a springtime favorite."
        ]
    },
    'brown-thrasher': {
        'common_name': 'Brown Thrasher',
        'scientific_name': 'Toxostoma rufum',
        'ebird_code': 'brnthr',
        'description': "Long-tailed and richly colored, the Brown Thrasher is a powerful singer often heard before it's seen, usually deep in shrubs and thickets.",
        'fun_facts': [
            "Song master: Can sing over 1,000 song variations.",
            "Bold eyes: Its bright yellow eyes are unmistakable.",
            "Ground hunter: Flips leaves aside to uncover insects.",
            "Protective parent: Aggressively defends nests from intruders."
        ]
    },
    'black-throated-sparrow': {
        'common_name': 'Black-throated Sparrow',
        'scientific_name': 'Amphispiza bilineata',
        'ebird_code': 'bktspa',
        'description': "A striking desert sparrow with bold facial markings, the Black-throated Sparrow thrives in arid landscapes where few birds can survive.",
        'fun_facts': [
            "Desert adapted: Can survive long periods without drinking water.",
            "Sharp contrast: Black throat and face stand out against pale gray plumage.",
            "Ground feeder: Forages mostly on the ground for seeds and insects.",
            "Sweet singer: Delivers a clear, musical song despite harsh surroundings."
        ]
    },
    'black-scoter': {
        'common_name': 'Black Scoter',
        'scientific_name': 'Melanitta americana',
        'ebird_code': 'blksco',
        'description': "A chunky sea duck, the Black Scoter is most often seen bobbing on rough coastal waters. Males appear mostly black with a bright knob at the base of the bill.",
        'fun_facts': [
            "Ocean dweller: Spends most of its life at sea.",
            "Deep diver: Dives underwater to feed on shellfish.",
            "Cold-weather bird: Common in winter along northern coasts.",
            "Fast flier: Takes off low over the water at high speed."
        ]
    },
    'brown-pelican': {
        'common_name': 'Brown Pelican',
        'scientific_name': 'Pelecanus occidentalis',
        'ebird_code': 'brnpel',
        'description': "Large and unmistakable, the Brown Pelican glides low over coastal waters before plunging dramatically to catch fish. Its oversized bill and expandable pouch make it a true fishing specialist.",
        'fun_facts': [
            "Spectacular dives: Plunges headfirst from the air into the water.",
            "Built-in net: Uses its pouch to scoop up fish and drain water.",
            "Comeback story: Once endangered, now a conservation success.",
            "Team players: Often fish cooperatively in groups."
        ]
    },
    'brown-creeper': {
        'common_name': 'Brown Creeper',
        'scientific_name': 'Certhia americana',
        'ebird_code': 'bncre',
        'description': "Small, well-camouflaged, and easy to miss, the Brown Creeper spirals up tree trunks searching for insects hidden in bark crevices. Its mottled brown pattern blends perfectly with tree bark.",
        'fun_facts': [
            "Upward climber: Always moves up trees, then flies down to start again.",
            "Tree-hugger: Rarely seen away from trunks.",
            "Camouflage king: Blends so well it often goes unnoticed.",
            "Soft voice: Its high, thin song is easy to miss."
        ]
    }
}

def extract_state_from_filename(filename):
    """Extract state name from filename, defaulting to Pennsylvania."""
    # Remove extension and numbers
    base = filename.replace('.jpg', '').replace('.JPG', '')

    # If filename starts with underscore, it's Pennsylvania (no state label)
    if base.startswith('_'):
        return 'Pennsylvania'

    # Remove trailing numbers
    state = re.sub(r'\d+$', '', base)

    # If the state part is empty or very short, assume Pennsylvania
    if not state or len(state) < 3:
        return 'Pennsylvania'

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

def update_species_page(species_slug):
    """Update a species page with new content."""
    data = SPECIES_DATA[species_slug]

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

# Update all 8 species
for species_slug in SPECIES_DATA.keys():
    update_species_page(species_slug)

print("\n✓ Updated all 8 species pages")
