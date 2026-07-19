# Ninja Luxe Cafe — Recipe & Guide

A mobile-first, single-page website for the Ninja Luxe Cafe espresso machine. Browse 90+ beverage recipes, save favorites, rate drinks, and explore a comprehensive machine guide.

## Features

- **90+ Recipes** — espresso, milk drinks, iced, specialty, tea, blended, cocktails, sugar-free, and Ninja exclusives
- **Milk Selector** — choose from 8 milk types with frothing tips per selection
- **Size Options** — adjustable drink sizes per recipe
- **Favorites & Ratings** — localStorage-based, no login required
- **Machine Guide** — full brew options reference, grind settings, froth system, advanced settings (h00-h08), cleaning, and troubleshooting
- **Mobile-First** — bottom nav on mobile, top nav on desktop, dark coffee theme
- **Machine-Specific Instructions** — every recipe references the exact machine settings (basket, mode, grind, frother)

## New Recipes Added

- **Spanish Latte (Café Bombón)** — layered sweetened condensed milk + espresso
- **Banana Bread Latte** (hot & iced) — banana-spice flavors in latte form

## Tech

- Single `index.html` with embedded CSS/JS
- No frameworks, no build step, no backend
- Uses `localStorage` for ratings and favorites

## Setup

1. Clone the repo
2. Serve with any static server: `python3 -m http.server 8080`
3. Open `http://localhost:8080` in your browser

## Image Credits

Recipe photos sourced from Unsplash, recipe blogs, and stock photography sites. All images are externally hosted and used for recipe reference.

## License

MIT
