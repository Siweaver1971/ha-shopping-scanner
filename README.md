# Shopping Scanner - Home Assistant Add-on

Barcode scanner for Home Assistant shopping lists with offline product database.

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

## About

This add-on provides a mobile-friendly barcode scanner that integrates directly with your Home Assistant shopping list. Simply scan product barcodes with your phone's camera, and items are automatically added to your shopping list.

## Features

- 📱 Mobile-optimized camera barcode scanner
- 🔍 Automatic product lookup from Open Food Facts database
- 💾 Offline product database - products are cached locally after first scan
- ✅ Direct integration with Home Assistant Shopping List
- 🎨 Dark mode interface
- 📊 Track your scanning history
- 🔄 Sync shopping list items in real-time

## Installation

### Add Repository

1. In Home Assistant, navigate to **Settings** → **Add-ons** → **Add-on Store**
2. Click the **⋮** menu (three dots) in the top right
3. Select **Repositories**
4. Add this repository URL: \https://github.com/Siweaver1971/ha-shopping-scanner\
5. Click **Add** → **Close**

### Install Add-on

1. Find **Shopping Scanner** in the add-on store
2. Click on it and press **Install**
3. Wait for the installation to complete
4. Toggle **Start on boot** (recommended)
5. Click **Start**

## Configuration

The add-on requires no configuration! It automatically connects to your Home Assistant instance.

### Optional Settings

\\\yaml
ssl: false
\\\

- **ssl**: Set to \	rue\ if you want to enforce SSL (default: false)

## Usage

### First Time Setup

1. After starting the add-on, click **Open Web UI** or access it from the sidebar
2. Grant camera permissions when prompted (required for barcode scanning)

### Scanning Products

1. Click the **"Start Scanning"** button
2. Point your camera at a product barcode
3. The app will automatically:
   - Scan the barcode
   - Look up product information
   - Add it to your Home Assistant shopping list
   - Store it in the local database for faster future scans

### Managing Your List

- Switch to the **"List"** tab to view your shopping list
- Check off items as you shop
- Items sync in real-time with Home Assistant

### Product Database

- Switch to the **"Products"** tab to view all scanned products
- Search through your product history
- Delete products if needed

## Supported Barcodes

- EAN-13 (most common in Europe)
- EAN-8
- UPC-A (most common in North America)
- UPC-E

## Supported Architectures

- amd64 (Intel/AMD 64-bit)
- aarch64 (ARM 64-bit - Raspberry Pi 3/4/5, etc.)

## Troubleshooting

### Camera Not Working

- Make sure you've granted camera permissions in your browser
- Try accessing the add-on via HTTPS if using Chrome on mobile
- Check that no other app is using the camera

### Products Not Adding to List

1. Go to the **Settings** tab in the app
2. Verify your Home Assistant connection settings
3. Make sure you have a "Shopping List" integration enabled in Home Assistant

### Unknown Products

If a product isn't found in the Open Food Facts database:
- You'll be prompted to enter the product name manually
- It will be saved to your local database for future scans

## How It Works

1. **Scan**: Uses your device's camera to scan barcodes via the QuaggaJS library
2. **Lookup**: Queries the Open Food Facts API for product information
3. **Cache**: Stores product data locally in IndexedDB for offline access
4. **Sync**: Adds items to your Home Assistant shopping list via the API

## Privacy

- All product data is stored locally in your browser
- No data is sent to external servers except:
  - Open Food Facts API (only for new product lookups)
  - Your Home Assistant instance

## Support

Found a bug or have a feature request?
[Open an issue on GitHub](https://github.com/Siweaver1971/ha-shopping-scanner/issues)

## License

MIT License - see [LICENSE](LICENSE) file for details

## Credits

- Built for [Home Assistant](https://www.home-assistant.io/)
- Product data from [Open Food Facts](https://world.openfoodfacts.org/)
- Barcode scanning powered by [QuaggaJS](https://serratus.github.io/quaggaJS/)

---

**Author**: Simon Weaver  
**Repository**: https://github.com/Siweaver1971/ha-shopping-scanner

[releases-shield]: https://img.shields.io/github/release/Siweaver1971/ha-shopping-scanner.svg
[releases]: https://github.com/Siweaver1971/ha-shopping-scanner/releases
[license-shield]: https://img.shields.io/github/license/Siweaver1971/ha-shopping-scanner.svg