# Updating Featured Homepage Photos

This guide explains how to update the featured photos that appear in the homepage slideshow.

## Quick Start

The homepage slideshow displays photos from the `images/featured/` folder. To update the featured photos each month:

### Option 1: Using the Update Script (Easiest)

1. **Add your new photos** to the folder on your Desktop:
   ```
   ~/Desktop/homepage-featured/
   ```

2. **Run the update script** from the repository directory:
   ```bash
   cd ~/Desktop/bird-photography
   ./update-featured.sh
   ```

3. **Commit and push** the changes:
   ```bash
   git add images/featured/
   git commit -m "Update featured homepage photos for January 2026"
   git push
   ```

That's it! Your homepage slideshow will automatically update with the new photos.

---

## Manual Update (Alternative Method)

If you prefer to update manually without the script:

### Step 1: Prepare Your Photos
1. Select 6-8 of your best photos for the month
2. Copy them to: `~/Desktop/homepage-featured/`

### Step 2: Run the Update Script
```bash
cd ~/Desktop/bird-photography
./update-featured.sh
```

The script will:
- Clear old featured photos
- Copy new photos from `~/Desktop/homepage-featured`
- Prepare them for the website

### Step 3: Commit and Push

```bash
cd ~/Desktop/bird-photography
git add images/featured/
git commit -m "Update featured homepage photos for January 2026"
git push
```

Your homepage slideshow will automatically update with the new photos within 1-2 minutes!

## How the Slideshow Works

The homepage slideshow automatically displays all images in the `images/featured/` folder. The slideshow:
- Auto-rotates every 4 seconds
- Displays images in alphabetical order by filename
- Shows smooth fade transitions between photos
- Works on desktop, tablet, and mobile devices

## Tips for Best Results

1. **Image Quality**: Use high-resolution photos (at least 1920x1080px)
2. **File Format**: JPG, JPEG, or PNG formats are supported
3. **File Naming**: Use descriptive filenames like `location-date-species.jpg`
4. **Number of Photos**: Recommended 6-10 photos for optimal slideshow experience
5. **Image Size**: Keep files under 2MB each for fast loading

## Folder Structure

```
bird-photography/
├── images/
│   ├── featured/          # Photos shown in homepage slideshow
│   ├── full/              # All full-size bird photos
│   └── thumbs/            # Thumbnail versions for galleries
├── update-featured.sh     # Script to update featured photos
└── README.md             # This file
```

## Tips

- **Best photos first**: The slideshow rotates every 4 seconds
- **Image size**: Use high-quality images (the script copies them as-is)
- **File naming**: Use descriptive names like `location-species-date.jpg`
- **Recommended count**: 6-10 photos work best for the slideshow
- **Update frequency**: Change photos monthly or seasonally to keep content fresh

## Troubleshooting

**Problem**: Script says "No image files found"
- Make sure your images have .jpg, .jpeg, or .png extensions
- Check that files are in ~/Desktop/homepage-featured (not in a subfolder)

**Problem**: Photos don't appear on website after pushing
- Wait 1-2 minutes for GitHub Pages to rebuild
- Clear your browser cache and refresh the page
- Check that image filenames don't have special characters or spaces

**Problem: Slideshow not working**
- Make sure you have at least 2 images in the featured folder
- Check that filenames don't have special characters
- Verify images are .jpg, .jpeg, or .png format

## File Structure

```
bird-photography/
├── images/
│   ├── featured/          # Homepage slideshow photos (update these monthly)
│   ├── full/              # Full-size photos for species/location pages
│   └── thumbs/            # Thumbnail images for galleries
├── update-featured.sh     # Script to update featured photos
└── index.html             # Homepage with auto-rotating slideshow
```

## Questions?

If you have any issues, check that:
- Image files are .jpg, .jpeg, or .png format
- Images are web-optimized (under 2MB each recommended)
- Filenames don't have special characters or spaces
- The homepage-featured folder exists on your Desktop

The slideshow will automatically cycle through all images in the featured folder!
