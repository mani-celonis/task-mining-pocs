# Task Mining Mac POC

Proof-of-concept macOS client for Celonis Task Mining.  
Demonstrates the same capture pipeline as the Windows `.NET / WPF` client, re-implemented with native macOS APIs.

## What it captures

| Capability | macOS API used | Windows equivalent |
|---|---|---|
| Foreground window (app + title) | `NSWorkspace` + `CGWindowListCopyWindowInfo` | `GetForegroundWindow` / `GetWindowText` |
| Mouse clicks (left/right) | `CGEventTap` | `SetWindowsHookEx WH_MOUSE_LL` |
| Key presses | `CGEventTap` | `SetWindowsHookEx WH_KEYBOARD_LL` |
| Clipboard changes | `NSPasteboard.general.changeCount` polling | `AddClipboardFormatListener` |
| UI element metadata | `AXUIElement` (Accessibility API) | COM `UIAutomationClient` |
| Screenshots on click | `CGWindowListCreateImage` | GDI `BitBlt` / `PrintWindow` |

Events are written as **JSONL** (one JSON object per line) to `~/CelonisTaskMining/sessions/{sessionId}/events.jsonl`.  
Screenshots are saved as PNG in the `screenshots/` subdirectory.

## Requirements

- macOS 13 (Ventura) or later
- Xcode Command Line Tools (`xcode-select --install`)

## Quick start

```bash
# Clone / cd into the project
cd task-mining-mac-poc

# Build
swift build

# Run (from terminal — you'll get permission prompts)
.build/debug/TaskMiningMac
```

### Build as .app bundle (recommended for persistent permissions)

```bash
./build.sh
open TaskMiningMac.app
```

## Permissions

macOS requires explicit user consent for the sensitive APIs this POC uses.  
Grant these in **System Settings → Privacy & Security**:

| Permission | Why | What breaks without it |
|---|---|---|
| **Accessibility** | `CGEventTap` + `AXUIElement` | No keyboard/mouse capture, no UI element reading |
| **Screen Recording** | `CGWindowListCreateImage` + window titles | Screenshots are blank, window titles are empty |
| **Input Monitoring** | Global event tap | Keyboard/mouse events not received |

> **Tip:** If running from Terminal, the permissions are granted to **Terminal.app** (or iTerm).  
> If running the `.app` bundle, they're granted to **TaskMiningMac.app** itself.  
> You may need to **restart the app** after granting permissions.

## Data format

Each line in `events.jsonl` is a JSON object:

```json
{
  "sessionId": "E4F5A6B7-...",
  "snippetId": "E4F5A6B7-..._0",
  "timestamp": "2026-03-24T10:30:15.123Z",
  "eventType": "Left click",
  "applicationName": "Safari",
  "windowTitle": "GitHub - google",
  "processPath": "/Applications/Safari.app",
  "bundleId": "com.apple.Safari",
  "mouseX": 512.0,
  "mouseY": 384.0,
  "elementName": "Search or enter website name",
  "elementRole": "AXTextField",
  "screenshotPath": "/Users/you/CelonisTaskMining/sessions/.../screenshots/UUID.png"
}
```

The schema intentionally mirrors the Windows client's `DefaultSchemaKeys` so that — in a production version — these events can be written to the same Parquet format and uploaded to the same Celonis cloud endpoints.

## Architecture

```
main.swift
  └─ AppDelegate (NSStatusItem menu-bar app)
       └─ CaptureEngine (orchestrator)
            ├─ EventTapMonitor   — CGEventTap (keyboard + mouse)
            ├─ WindowTracker     — NSWorkspace + CGWindowList
            ├─ AccessibilityReader — AXUIElement
            ├─ ClipboardMonitor  — NSPasteboard polling
            ├─ ScreenshotCapture — CGWindowListCreateImage
            └─ EventStore        — JSONL + PNG persistence
```

## What this POC does NOT include (production roadmap)

- **Parquet output** — needs Apache Arrow C bindings or a conversion layer
- **Cloud upload** — OAuth2 activation + multipart upload to Celonis endpoints
- **ECA filter rules** — the Windows client's configurable event filtering engine
- **Encrypted local storage** — AES-256-CTR for cached files
- **Browser extension bridge** — Chrome/Edge native messaging host
- **Password field detection / redaction**
- **SAP GUI enrichment**
- **Installer / notarization / MDM profile for silent TCC approval**

## License

Internal POC — Celonis SE
