#!/bin/bash
set -e

APP_NAME="TaskMiningMac"
BUILD_DIR=".build/release"
APP_BUNDLE="${APP_NAME}.app"

echo "==> Building ${APP_NAME}..."
swift build -c release

echo "==> Creating app bundle: ${APP_BUNDLE}"
rm -rf "${APP_BUNDLE}"
mkdir -p "${APP_BUNDLE}/Contents/MacOS"
mkdir -p "${APP_BUNDLE}/Contents/Resources"

cp "${BUILD_DIR}/${APP_NAME}" "${APP_BUNDLE}/Contents/MacOS/${APP_NAME}"
cp Info.plist "${APP_BUNDLE}/Contents/"

echo ""
echo "Build complete!"
echo ""
echo "To run:  open ${APP_BUNDLE}"
echo ""
echo "IMPORTANT — grant these permissions in System Settings > Privacy & Security:"
echo "  1. Accessibility    (for keyboard/mouse monitoring + UI element reading)"
echo "  2. Screen Recording (for screenshots and window title capture)"
echo "  3. Input Monitoring  (for global keyboard/mouse event capture)"
echo ""
echo "You may need to restart the app after granting permissions."
