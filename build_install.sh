#!/bin/bash

APP_NAME="IsimuSense"
APP_PATH="/Applications/$APP_NAME.app"

echo "🧹 Cleaning old builds..."
rm -rf build dist *.spec

echo "🔨 Building app..."
pyinstaller \
--windowed \
--name $APP_NAME \
--icon=IsimuSense.icns \
desktop_app.py \
--add-data "config.py:." \
--add-data "app/templates:app/templates" \
--add-data "app/static:app/static"

echo "🗑 Removing old app from Applications..."
rm -rf "$APP_PATH"

echo "📦 Installing new app..."
mv dist/$APP_NAME.app /Applications/

echo "🎨 Refreshing macOS icon cache..."
touch "$APP_PATH"

echo "🚀 Launching app..."
open "$APP_PATH"

echo "✅ Done!"