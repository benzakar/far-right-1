#!/bin/sh
# Build "FromParty Editor.app" — a double-clickable launcher for the editor.
#
#   sh editor/make-app.sh
#
# Why an app and not a background service: the repository lives under
# ~/Documents, which macOS protects. A launchd job gets no access there and
# dies with "Operation not permitted", and the only way around that is
# granting Full Disk Access to the python3 binary itself — far too broad.
# An app bundle asks for Documents access once, by name, the first time you
# open it, and keeps it afterwards.
#
# The app starts the server if it is not already running, then opens the
# editor in your browser. No terminal stays open.

set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APP="${1:-$HOME/Applications/FromParty Editor.app}"
PORT="${EDITOR_PORT:-8765}"

rm -rf "$APP"
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"

cat > "$APP/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleName</key><string>FromParty Editor</string>
  <key>CFBundleDisplayName</key><string>FromParty Editor</string>
  <key>CFBundleIdentifier</key><string>com.fromparty.editor</string>
  <key>CFBundleVersion</key><string>1.0</string>
  <key>CFBundleShortVersionString</key><string>1.0</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>CFBundleExecutable</key><string>fromparty-editor</string>
  <key>CFBundleIconFile</key><string>app</string>
  <!-- Menu-bar-less background app: no Dock icon, nothing to accidentally quit. -->
  <key>LSUIElement</key><true/>
</dict>
</plist>
PLIST

cat > "$APP/Contents/MacOS/fromparty-editor" <<LAUNCHER
#!/bin/sh
# Starts the editor if needed, then opens it. Safe to run repeatedly.
ROOT="$ROOT"
PORT="$PORT"
LOG="\$HOME/Library/Logs/fromparty-editor.log"
PATH=/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin
export PATH EDITOR_PORT="\$PORT"

if ! curl -s -o /dev/null "http://127.0.0.1:\$PORT/editor/"; then
  cd "\$ROOT" || exit 1
  # Touch a file in the repo first: this is what triggers the one-time
  # "access files in your Documents folder" prompt, attributed to this app.
  ls "\$ROOT/editor/server.py" >/dev/null 2>&1 || exit 1
  nohup python3 "\$ROOT/editor/server.py" >> "\$LOG" 2>&1 &
  i=0
  while [ \$i -lt 60 ]; do
    curl -s -o /dev/null "http://127.0.0.1:\$PORT/editor/" && break
    i=\$((i + 1)); sleep 0.25
  done
fi

open "http://127.0.0.1:\$PORT/editor/"
LAUNCHER

chmod +x "$APP/Contents/MacOS/fromparty-editor"

# Give it the party mark so it is recognisable in Login Items.
if command -v sips >/dev/null 2>&1 && [ -f "$ROOT/static/img/favicon2.png" ]; then
  ICONSET="$(mktemp -d)/app.iconset"
  mkdir -p "$ICONSET"
  for s in 16 32 128 256 512; do
    sips -z $s $s "$ROOT/static/img/favicon2.png" \
      --out "$ICONSET/icon_${s}x${s}.png" >/dev/null 2>&1 || true
  done
  iconutil -c icns "$ICONSET" -o "$APP/Contents/Resources/app.icns" 2>/dev/null || true
fi

echo "Built: $APP"
echo
echo "Next:"
echo "  1. Double-click it once and allow access to your Documents folder."
echo "  2. To start it at login: System Settings > General > Login Items,"
echo "     then add it under \"Open at Login\"."
