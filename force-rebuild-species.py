#!/usr/bin/env python3
"""
Force rebuild all species pages using the working Carolina Wren template
"""

import os
import glob

# Species metadata
SPECIES_DATA = {
    'american-herring-gull': {
        'name': 'American Herring Gull',
        'scientific': 'Larus smithsonianus',
        'ebird': 'amhegu',
        'about': 'The American Herring Gull is a large, adaptable seabird commonly found along coastlines, beaches, and harbors. With its pale gray back, white head, and powerful presence, it often dominates coastal scenes. Highly intelligent and opportunistic, this gull thrives in both wild and human-altered environments.',
        'facts': [
            ('<strong>Slow to mature:</strong>', 'It takes several years to reach full adult plumage.'),
            ('<strong>Highly adaptable:</strong>', 'Found from remote shorelines to busy coastal cities.'),
            ('<strong>Problem solvers:</strong>', 'Known for using clever techniques to access food.'),
            ('<strong>Strong fliers:</strong>', 'Comfortable soaring long distances along the coast.'),
            ('<strong>Vocal communicators:</strong>', 'Use a wide range of calls to signal alarm or claim space.')
        ]
    },
    'american-robin': {
        'name': 'American Robin',
        'scientific': 'Turdus migratorius',
        'ebird': 'amerob',
        'about': 'The American Robin is one of North America\'s most recognizable songbirds, known for its bright orange-red breast and cheerful song. Often seen hopping across lawns searching for earthworms, it\'s a familiar sign of spring across much of the continent. Despite its name, it\'s actually a thrush, not closely related to the European Robin.',
        'facts': [
            ('<strong>Early bird:</strong>', 'Often one of the first birds to sing at dawn.'),
            ('<strong>Worm hunter:</strong>', 'Uses sight rather than sound to locate earthworms.'),
            ('<strong>Multiple broods:</strong>', 'Can raise two or three broods in a single season.'),
            ('<strong>Berry lover:</strong>', 'Diet shifts to fruits and berries in fall and winter.'),
            ('<strong>Suburban adapter:</strong>', 'Thrives in parks, yards, and urban green spaces.')
        ]
    },
    'bald-eagle': {
        'name': 'Bald Eagle',
        'scientific': 'Haliaeetus leucocephalus',
        'ebird': 'baleag',
        'about': 'The Bald Eagle, America\'s national bird, is a powerful raptor with a distinctive white head and tail contrasting against its dark brown body. Once endangered, it has made a remarkable recovery and is now commonly seen near rivers, lakes, and coastlines. These impressive birds can have wingspans exceeding 7 feet and are skilled hunters and scavengers.',
        'facts': [
            ('<strong>Not actually bald:</strong>', 'The name comes from an old meaning of "bald" meaning white-headed.'),
            ('<strong>Massive nests:</strong>', 'Builds some of the largest nests of any bird species, reusing them for years.'),
            ('<strong>Powerful vision:</strong>', 'Can see fish in water from several hundred feet in the air.'),
            ('<strong>Long-lived:</strong>', 'Can live 20-30 years in the wild, even longer in captivity.'),
            ('<strong>Conservation success:</strong>', 'Recovered from near extinction thanks to protection efforts.')
        ]
    },
    'black-and-white-warbler': {
        'name': 'Black-and-white Warbler',
        'scientific': 'Mniotilta varia',
        'ebird': 'bawwar',
        'about': 'The Black-and-white Warbler is a small songbird with bold striped plumage that makes it easy to identify. Unlike most warblers, it forages by creeping along tree trunks and branches like a nuthatch, probing bark crevices for insects. Its unique behavior and striking pattern make it a favorite among birdwatchers.',
        'facts': [
            ('<strong>Tree creeper:</strong>', 'Forages on tree bark like a nuthatch, unlike most warblers.'),
            ('<strong>Bold pattern:</strong>', 'Heavily striped in black and white from head to tail.'),
            ('<strong>Early migrant:</strong>', 'One of the first warblers to arrive in spring and leave in fall.'),
            ('<strong>Long-distance traveler:</strong>', 'Migrates between North America and Central/South America.'),
            ('<strong>Specialized niche:</strong>', 'Fills a unique ecological role among warblers.')
        ]
    },
    'black-capped-chickadee': {
        'name': 'Black-capped Chickadee',
        'scientific': 'Poecile atricapillus',
        'ebird': 'bkcchi',
        'about': 'The Black-capped Chickadee is a tiny, energetic bird with a bold personality. Its black cap and bib contrast sharply with soft gray and white feathers, making it easy to recognize. Curious and fearless, it often approaches closely and is a favorite among backyard birders.',
        'facts': [
            ('<strong>Name caller:</strong>', 'Its \'chick-a-dee-dee-dee\' call signals alert or excitement.'),
            ('<strong>Cold-weather tough:</strong>', 'Can survive freezing nights by lowering body temperature.'),
            ('<strong>Food stasher:</strong>', 'Hides seeds to retrieve later.'),
            ('<strong>Friendly nature:</strong>', 'Often the first bird to visit feeders.'),
            ('<strong>Strong memory:</strong>', 'Can remember hundreds of food cache locations.')
        ]
    },
    'black-throated-green-warbler': {
        'name': 'Black-throated Green Warbler',
        'scientific': 'Setophaga virens',
        'ebird': 'btnwar',
        'about': 'The Black-throated Green Warbler is a small, crisp-looking warbler often found in coniferous forests and mixed woodlands. Its bright yellow face and bold black throat make it stand out among foliage. Though small, it carries a loud, persistent song during the breeding season.',
        'facts': [
            ('<strong>Forest specialist:</strong>', 'Favors evergreen and mixed forests.'),
            ('<strong>High singer:</strong>', 'Often sings from mid to upper tree levels.'),
            ('<strong>Clear markings:</strong>', 'One of the easier warblers to identify visually.'),
            ('<strong>Long migrant:</strong>', 'Travels between North America and Central America.'),
            ('<strong>Persistent voice:</strong>', 'Repeats its song frequently throughout the day.')
        ]
    },
    'blue-gray-gnatcatcher': {
        'name': 'Blue-gray Gnatcatcher',
        'scientific': 'Polioptila caerulea',
        'ebird': 'buggna',
        'about': 'The Blue-gray Gnatcatcher is a tiny, restless songbird that seems to float through trees with constant motion. Its soft blue-gray coloring, long tail edged in white, and quick, darting movements give it a delicate, energetic presence. Often heard before it\'s seen, this bird adds life and motion to woodlands during spring and summer.',
        'facts': [
            ('<strong>Always moving:</strong>', 'Rarely sits still, constantly flicking its tail as it forages.'),
            ('<strong>Insect hunter:</strong>', 'Feeds almost entirely on small insects, often catching them midair.'),
            ('<strong>Spider-silk architect:</strong>', 'Builds a tiny nest bound together with spider silk and camouflaged with lichen.'),
            ('<strong>Early arrival:</strong>', 'One of the first migrants to return in spring.'),
            ('<strong>Big attitude:</strong>', 'Despite its size, it aggressively defends its nesting territory.')
        ]
    },
    'blue-jay': {
        'name': 'Blue Jay',
        'scientific': 'Cyanocitta cristata',
        'ebird': 'blujay',
        'about': 'The Blue Jay is a bold, intelligent bird with striking blue, white, and black plumage. Common in woodlands and suburban areas, it\'s as known for its loud calls as for its clever behavior. Jays often act as sentinels, alerting other birds to potential danger.',
        'facts': [
            ('<strong>Mimic talent:</strong>', 'Can imitate hawk calls to clear feeders.'),
            ('<strong>Acorn planter:</strong>', 'Helps forests grow by caching and forgetting seeds.'),
            ('<strong>Family-oriented:</strong>', 'Often travels in small family groups.'),
            ('<strong>Strong memory:</strong>', 'Remembers food locations well.'),
            ('<strong>Vocal leader:</strong>', 'One of the loudest and most expressive songbirds.')
        ]
    },
    'canada-goose': {
        'name': 'Canada Goose',
        'scientific': 'Branta canadensis',
        'ebird': 'cangoo',
        'about': 'The Canada Goose is a large waterfowl with a distinctive black head and neck, white chinstrap, and brown body. Once primarily migratory, many populations now remain year-round in parks, golf courses, and wetlands. Their loud honking and V-shaped flight formations are iconic sights and sounds of North American skies.',
        'facts': [
            ('<strong>Lifelong pairs:</strong>', 'Mates often stay together for life.'),
            ('<strong>V-formation fliers:</strong>', 'Take turns leading the flock to conserve energy.'),
            ('<strong>Protective parents:</strong>', 'Both parents fiercely defend their goslings.'),
            ('<strong>Adaptable residents:</strong>', 'Many have stopped migrating and live year-round in urban areas.'),
            ('<strong>Vocal communicators:</strong>', 'Use at least 13 different calls to communicate.')
        ]
    }
}

# HTML template (using Carolina Wren as the base)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-EBYMJ2QKHQ"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-EBYMJ2QKHQ');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{species_name} - Bird Photography</title>
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Georgia', serif;
            line-height: 1.6;
            color: #333;
        }}

        /* Navigation */
        nav {{
            background-color: #2c3e50;
            padding: 1.25rem 0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}

        nav ul {{
            list-style: none;
            display: flex;
            justify-content: center;
            gap: 1.75rem;
        }}

        nav a {{
            color: white;
            text-decoration: none;
            font-size: 1rem;
            transition: color 0.3s;
        }}

        nav a:hover {{
            color: #3498db;
        }}

        /* Page Header */
        .species-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            padding: 4rem 2rem 2rem;
        }}

        .species-header h1 {{
            font-size: 3rem;
            margin-bottom: 0.5rem;
            font-weight: 300;
        }}

        .species-header .scientific-name {{
            font-style: italic;
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 1.5rem;
        }}

        .species-header .ebird-button {{
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            padding: 0.9rem 2rem;
            text-decoration: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: bold;
            transition: all 0.3s;
            border: 2px solid rgba(255, 255, 255, 0.5);
            margin-top: 1rem;
        }}

        .species-header .ebird-button:hover {{
            background: rgba(255, 255, 255, 0.3);
            border-color: rgba(255, 255, 255, 0.8);
            transform: translateY(-2px);
        }}

        /* Container */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 4rem 2rem;
        }}

        /* Species Info Section */
        .species-info {{
            background-color: #f8f9fa;
            padding: 3rem 2rem;
            margin-bottom: 4rem;
        }}

        .info-content {{
            max-width: 900px;
            margin: 0 auto;
        }}

        .info-section {{
            margin-bottom: 2rem;
        }}

        .info-section h2 {{
            font-size: 1.8rem;
            color: #2c3e50;
            margin-bottom: 1rem;
        }}

        .info-section p {{
            font-size: 1.1rem;
            line-height: 1.8;
            color: #555;
        }}

        .placeholder-text {{
            font-style: italic;
            color: #999;
        }}

        .info-section ul {{
            list-style: disc;
            margin-left: 2rem;
            margin-top: 1rem;
        }}

        .info-section ul li {{
            font-size: 1.1rem;
            line-height: 1.8;
            color: #555;
            margin-bottom: 0.8rem;
        }}

        .info-section ul li strong {{
            color: #2c3e50;
        }}

        /* Gallery Grid */
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 4rem;
        }}

        .gallery-item {{
            display: flex;
            flex-direction: column;
        }}

        .gallery-item img {{
            width: 100%;
            height: auto;
            display: block;
            cursor: pointer;
            transition: transform 0.3s, opacity 0.3s;
        }}

        .gallery-item img:hover {{
            transform: scale(1.02);
            opacity: 0.9;
        }}

        .gallery-caption {{
            padding: 0.6rem;
            background-color: #2c3e50;
            color: white;
            text-align: center;
            font-size: 0.95rem;
        }}

        /* Back Link */
        .back-link {{
            display: inline-block;
            margin-bottom: 2rem;
            color: #667eea;
            text-decoration: none;
            font-size: 1.1rem;
            transition: color 0.3s;
        }}

        .back-link:hover {{
            color: #764ba2;
        }}

        /* Location Appearances Section */
        .location-appearances {{
            background-color: #f8f9fa;
            padding: 2.5rem 2rem;
            margin: 3rem 0;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}

        .location-appearances h2 {{
            font-size: 1.8rem;
            color: #2c3e50;
            margin-bottom: 1.5rem;
        }}

        .location-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
        }}

        .location-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: white;
            padding: 0.75rem 1.25rem;
            border-radius: 6px;
            text-decoration: none;
            color: #2c3e50;
            font-size: 1.05rem;
            transition: all 0.3s;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        }}

        .location-badge:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.12);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}

        .location-badge .location-name {{
            font-weight: 500;
        }}

        .location-badge .photo-count {{
            background: rgba(102, 126, 234, 0.1);
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            font-size: 0.9rem;
            font-weight: 600;
            color: #667eea;
        }}

        .location-badge:hover .photo-count {{
            background: rgba(255, 255, 255, 0.3);
            color: white;
        }}

        .no-locations {{
            font-style: italic;
            color: #999;
            font-size: 1.05rem;
        }}


        /* Lightbox */
        .lightbox {{
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.95);
            opacity: 0;
            transition: opacity 0.3s ease;
        }}

        .lightbox.active {{
            display: flex;
            opacity: 1;
            justify-content: center;
            align-items: center;
        }}

        .lightbox-content {{
            position: relative;
            max-width: 90%;
            max-height: 90%;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .lightbox-image {{
            max-width: 100%;
            max-height: 85vh;
            object-fit: contain;
            border-radius: 4px;
        }}

        .lightbox-close {{
            position: absolute;
            top: 20px;
            right: 40px;
            color: white;
            font-size: 40px;
            font-weight: bold;
            cursor: pointer;
            z-index: 1001;
            background: rgba(102, 126, 234, 0.3);
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s;
            line-height: 1;
        }}

        .lightbox-close:hover {{
            background: rgba(102, 126, 234, 0.5);
            transform: rotate(90deg);
        }}

        .lightbox-nav {{
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            color: white;
            font-size: 30px;
            cursor: pointer;
            padding: 1rem 1.5rem;
            background: rgba(102, 126, 234, 0.3);
            border-radius: 8px;
            transition: all 0.3s;
            user-select: none;
        }}

        .lightbox-nav:hover {{
            background: rgba(102, 126, 234, 0.5);
        }}

        .lightbox-prev {{
            left: 40px;
        }}

        .lightbox-next {{
            right: 40px;
        }}

        .lightbox-counter {{
            color: white;
            font-size: 1rem;
            margin-top: 1rem;
            background: rgba(0, 0, 0, 0.5);
            padding: 0.5rem 1rem;
            border-radius: 20px;
        }}

        .lightbox-caption {{
            color: white;
            font-size: 1.1rem;
            margin-top: 0.5rem;
            text-align: center;
            background: rgba(0, 0, 0, 0.5);
            padding: 0.5rem 1rem;
            border-radius: 20px;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .species-header h1 {{
                font-size: 2rem;
            }}

            .species-header .ebird-button {{
                font-size: 0.9rem;
                padding: 0.8rem 1.5rem;
            }}

            .gallery {{
                grid-template-columns: 1fr;
            }}

            nav ul {{
                flex-direction: column;
                gap: 1rem;
            }}

            .lightbox-close {{
                top: 10px;
                right: 10px;
                width: 40px;
                height: 40px;
                font-size: 30px;
            }}

            .lightbox-nav {{
                font-size: 24px;
                padding: 0.75rem 1rem;
            }}

            .lightbox-prev {{
                left: 10px;
            }}

            .lightbox-next {{
                right: 10px;
            }}
        }}
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav>
        <ul>
            <li><a href="index.html">Home</a></li>
            <li><a href="species.html">Browse by Species</a></li>
            <li><a href="locations.html">Browse by Location</a></li>
            <li><a href="recently-added.html">Recently Added</a></li>
            <li><a href="best-of.html">Best Of</a></li>
            <li><a href="index.html#about">About</a></li>
            <li><a href="index.html#contact">Contact</a></li>
        </ul>
    </nav>

    <!-- Species Header -->
    <section class="species-header">
        <h1>{species_name}</h1>
        <p class="scientific-name">{scientific_name}</p>
        <a href="https://ebird.org/species/{ebird_code}" target="_blank" class="ebird-button">View Range Map on eBird</a>
    </section>

    <!-- Species Info -->
    <section class="species-info">
        <div class="info-content">
            <div class="info-section">
                <h2>About This Species</h2>
                <p>{about_text}</p>
            </div>
            <div class="info-section">
                <h2>Fun Facts</h2>
                <ul>
{fun_facts}
                </ul>
            </div>
        </div>
    </section>

    <!-- Gallery Section -->
    <section class="container">
        <a href="species.html" class="back-link">← Back to All Species</a>
        <div class="gallery">
{gallery_items}
        </div>

        <!-- Location Appearances Section -->
        <div class="location-appearances" id="locationAppearances" style="display: none;">
            <h2>See this species at these locations</h2>
            <div class="location-list" id="locationList"></div>
        </div>
    </section>

        <!-- Lightbox -->
    <div id="lightbox" class="lightbox" onclick="closeLightbox(event)">
        <span class="lightbox-close" onclick="closeLightbox(event)">&times;</span>
        <span class="lightbox-nav lightbox-prev" onclick="changeImage(-1); event.stopPropagation();">&#10094;</span>
        <div class="lightbox-content">
            <img id="lightbox-image" class="lightbox-image" src="" alt="">
            <div id="lightbox-counter" class="lightbox-counter"></div>
            <div id="lightbox-caption" class="lightbox-caption"></div>
        </div>
        <span class="lightbox-nav lightbox-next" onclick="changeImage(1); event.stopPropagation();">&#10095;</span>
    </div>

<script src="species-locations-data.js"></script>
    <script>
        // Get current species name from the page
        const speciesName = document.querySelector('.species-header h1').textContent;

        // Normalize species name to match data format (handle different capitalizations and punctuation)
        function normalizeSpeciesName(name) {{
            return name.toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
        }}

        // Find matching species in data
        function findSpeciesLocations(currentSpecies) {{
            const normalized = normalizeSpeciesName(currentSpecies);

            // Search through all species in data
            for (const [species, locations] of Object.entries(speciesLocationsData)) {{
                if (normalizeSpeciesName(species) === normalized) {{
                    return locations;
                }}
            }}
            return null;
        }}

        // Display location appearances
        const locations = findSpeciesLocations(speciesName);

        if (locations && Object.keys(locations).length > 0) {{
            const locationList = document.getElementById('locationList');
            const appearancesSection = document.getElementById('locationAppearances');

            // Sort locations by photo count (descending)
            const sortedLocations = Object.entries(locations).sort((a, b) => b[1].count - a[1].count);

            // Create location badges
            sortedLocations.forEach(([locId, locData]) => {{
                const badge = document.createElement('a');
                badge.href = locData.url;
                badge.className = 'location-badge';

                const photoWord = locData.count === 1 ? 'photo' : 'photos';

                badge.innerHTML = `
                    <span class="location-name">${{locData.name}}</span>
                    <span class="photo-count">${{locData.count}} ${{photoWord}}</span>
                `;

                locationList.appendChild(badge);
            }});

            // Show the section
            appearancesSection.style.display = 'block';
        }}

        // Lightbox functionality
        const lightbox = document.getElementById('lightbox');
        const lightboxImage = document.getElementById('lightbox-image');
        const lightboxCounter = document.getElementById('lightbox-counter');
        const lightboxCaption = document.getElementById('lightbox-caption');
        let currentIndex = 0;
        let galleryImages = [];

        // Build gallery images array
        function buildGallery() {{
            const galleryItems = document.querySelectorAll('.gallery-item');
            galleryImages = Array.from(galleryItems).map(item => {{
                const img = item.querySelector('img');
                const caption = item.querySelector('.gallery-caption');
                return {{
                    // Use thumbnail images directly for species pages
                    src: img.src,
                    caption: caption ? caption.textContent : ''
                }};
            }});

            // Add click handlers to gallery images
            galleryItems.forEach((item, index) => {{
                const img = item.querySelector('img');
                img.addEventListener('click', () => openLightbox(index));
            }});
        }}

        function openLightbox(index) {{
            currentIndex = index;
            showImage();
            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden';
        }}

        function closeLightbox(event) {{
            if (event.target.id === 'lightbox' || event.target.classList.contains('lightbox-close')) {{
                lightbox.classList.remove('active');
                document.body.style.overflow = 'auto';
            }}
        }}

        function changeImage(direction) {{
            currentIndex += direction;
            if (currentIndex >= galleryImages.length) currentIndex = 0;
            else if (currentIndex < 0) currentIndex = galleryImages.length - 1;
            showImage();
        }}

        function showImage() {{
            const image = galleryImages[currentIndex];
            lightboxImage.src = image.src;
            lightboxCounter.textContent = `${{currentIndex + 1}} / ${{galleryImages.length}}`;
            lightboxCaption.textContent = image.caption;
        }}

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {{
            if (!lightbox.classList.contains('active')) return;

            if (e.key === 'ArrowLeft') changeImage(-1);
            else if (e.key === 'ArrowRight') changeImage(1);
            else if (e.key === 'Escape') {{
                lightbox.classList.remove('active');
                document.body.style.overflow = 'auto';
            }}
        }});

        // Initialize gallery on page load
        buildGallery();
    </script>

    </body>
</html>
"""


def get_images_for_species(species_slug):
    """Get all images for a species from its thumbs folder"""
    thumbs_path = f'/Users/michaelmurphy1/Desktop/bird-photography/images/species/{species_slug}/thumbs/'
    images = sorted(glob.glob(os.path.join(thumbs_path, '*.jpg')))
    return [os.path.basename(img) for img in images]


def extract_state_from_filename(filename):
    """Extract state from filename if it's a state-named file"""
    base = filename.lower().replace('.jpg', '')

    state_names = {
        'maine': 'Maine',
        'delaware': 'Delaware',
        'ohio': 'Ohio',
        'texas': 'Texas',
        'new-jersey': 'New Jersey',
        'new-jersey2': 'New Jersey',
        'new-jersey3': 'New Jersey',
        'new-jersey4': 'New Jersey',
        'new-jersey5': 'New Jersey'
    }

    if base in state_names:
        return state_names[base]

    return 'Pennsylvania'  # Default


def generate_gallery_items(species_slug, images):
    """Generate gallery HTML for images"""
    items = []
    for img in images:
        state = extract_state_from_filename(img)
        species_display = SPECIES_DATA[species_slug]['name']

        item = f"""            <div class="gallery-item">
                <img src="images/species/{species_slug}/thumbs/{img}" alt="{species_display}">
                <div class="gallery-caption">{state}</div>
            </div>"""
        items.append(item)

    return '\n'.join(items)


def generate_fun_facts(facts):
    """Generate fun facts HTML"""
    items = []
    for strong, text in facts:
        items.append(f'                    <li>{strong} {text}</li>')
    return '\n'.join(items)


def rebuild_species_page(species_slug):
    """Rebuild a species page from scratch"""

    if species_slug not in SPECIES_DATA:
        print(f"⚠ No data for {species_slug}")
        return False

    data = SPECIES_DATA[species_slug]
    images = get_images_for_species(species_slug)

    if not images:
        print(f"⚠ No images found for {species_slug}")
        return False

    # Generate HTML content
    gallery_items = generate_gallery_items(species_slug, images)
    fun_facts = generate_fun_facts(data['facts'])

    html_content = HTML_TEMPLATE.format(
        species_name=data['name'],
        scientific_name=data['scientific'],
        ebird_code=data['ebird'],
        about_text=data['about'],
        fun_facts=fun_facts,
        gallery_items=gallery_items
    )

    # Write file
    output_path = f'/Users/michaelmurphy1/Desktop/bird-photography/{species_slug}.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✓ Rebuilt {data['name']}")
    return True


def main():
    species_to_rebuild = [
        'american-herring-gull',
        'american-robin',
        'bald-eagle',
        'black-and-white-warbler',
        'black-capped-chickadee',
        'black-throated-green-warbler',
        'blue-gray-gnatcatcher',
        'blue-jay',
        'canada-goose'
    ]

    rebuilt_count = 0

    for species_slug in species_to_rebuild:
        if rebuild_species_page(species_slug):
            rebuilt_count += 1

    print(f"\n✓ Force rebuilt {rebuilt_count}/{len(species_to_rebuild)} species pages")


if __name__ == '__main__':
    main()
