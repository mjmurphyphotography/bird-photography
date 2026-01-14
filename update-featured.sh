#!/bin/bash

# Update Featured Photos Script
# This script copies photos from ~/Desktop/homepage-featured to the repository

echo "==============================================="
echo "  Bird Photography - Update Featured Photos"
echo "==============================================="
echo ""

REPO_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SOURCE_DIR="$HOME/Desktop/homepage-featured"
DEST_DIR="$REPO_DIR/images/featured"

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory does not exist: $SOURCE_DIR"
    echo "Please create the folder and add your photos."
    exit 1
fi

# Check if there are any image files
IMAGE_COUNT=$(ls -1 "$SOURCE_DIR"/*.{jpg,JPG,jpeg,JPEG,png,PNG} 2>/dev/null | wc -l)
if [ "$IMAGE_COUNT" -eq 0 ]; then
    echo "Error: No image files found in $SOURCE_DIR"
    echo "Please add .jpg, .jpeg, or .png files to the folder."
    exit 1
fi

echo "Found $IMAGE_COUNT image(s) in $SOURCE_DIR"
echo ""

# Clear existing featured photos
echo "Clearing existing featured photos..."
rm -f "$DEST_DIR"/*

# Copy new photos
echo "Copying new featured photos..."
cp "$SOURCE_DIR"/*.{jpg,JPG,jpeg,JPEG,png,PNG} "$DEST_DIR/" 2>/dev/null

# Rename files to lowercase extensions for consistency
cd "$DEST_DIR"
for file in *.JPG *.JPEG *.PNG 2>/dev/null; do
    if [ -f "$file" ]; then
        lowercase=$(echo "$file" | sed 's/\(.*\.\)\(.*\)/\1\L\2/')
        mv "$file" "$lowercase" 2>/dev/null
    fi
done

# Count final images
FINAL_COUNT=$(ls -1 "$DEST_DIR"/*.{jpg,jpeg,png} 2>/dev/null | wc -l)

echo ""
echo "✓ Successfully copied $FINAL_COUNT image(s) to images/featured/"
echo ""
echo "Next steps:"
echo "  1. Review the images in images/featured/"
echo "  2. Commit the changes:"
echo "     git add images/featured/"
echo "     git commit -m \"Update featured homepage photos for $(date +'%B %Y')\""
echo "  3. Push to GitHub:"
echo "     git push"
echo ""
echo "Your slideshow will automatically update with the new photos!"
echo ""
