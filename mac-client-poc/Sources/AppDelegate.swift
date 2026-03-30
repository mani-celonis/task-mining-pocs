import AppKit
import ApplicationServices

class AppDelegate: NSObject, NSApplicationDelegate {
    private var statusItem: NSStatusItem!
    private let captureEngine = CaptureEngine()
    private var isRecording = false

    // Menu items we update at runtime
    private var startStopItem: NSMenuItem!
    private var statusLabel: NSMenuItem!
    private var eventCountItem: NSMenuItem!

    // MARK: - Lifecycle

    /// Pass `--auto-record <seconds>` to record headlessly and quit.
    var autoRecordSeconds: Int?

    func applicationDidFinishLaunching(_ notification: Notification) {
        NSApp.setActivationPolicy(.accessory)

        captureEngine.onEventCountChanged = { [weak self] count in
            self?.eventCountItem?.title = "Events captured: \(count)"
            if self?.autoRecordSeconds != nil {
                print("[auto] events: \(count)")
            }
        }
        captureEngine.onStatusChanged = { [weak self] status in
            self?.statusLabel?.title = "Status: \(status)"
            if self?.autoRecordSeconds != nil {
                print("[auto] \(status)")
            }
        }

        buildMenuBar()

        if let seconds = autoRecordSeconds, seconds > 0 {
            startAutoRecord(seconds: seconds)
        } else {
            promptForPermissionsIfNeeded()
        }
    }

    private func startAutoRecord(seconds: Int) {
        print("[auto] Starting \(seconds)-second recording…")
        captureEngine.startRecording()
        isRecording = true
        startStopItem?.title = "Stop Recording"

        DispatchQueue.main.asyncAfter(deadline: .now() + .seconds(seconds)) { [weak self] in
            guard let self else { return }
            print("[auto] Time's up — stopping recording.")
            self.captureEngine.stopRecording()
            self.isRecording = false

            let dir = self.captureEngine.dataDirectory
            print("[auto] Data directory: \(dir.path)")
            print("[auto] Total events: \(self.captureEngine.eventStore.eventCount)")
            NSApp.terminate(nil)
        }
    }

    // MARK: - Menu bar

    private func buildMenuBar() {
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)

        if let button = statusItem.button {
            button.image = NSImage(
                systemSymbolName: "record.circle",
                accessibilityDescription: "Task Mining"
            )
            button.title = " Task Mining"
        }

        let menu = NSMenu()

        statusLabel = menu.addItem(
            withTitle: "Status: Stopped", action: nil, keyEquivalent: ""
        )
        statusLabel.isEnabled = false

        eventCountItem = menu.addItem(
            withTitle: "Events captured: 0", action: nil, keyEquivalent: ""
        )
        eventCountItem.isEnabled = false

        menu.addItem(.separator())

        startStopItem = menu.addItem(
            withTitle: "Start Recording",
            action: #selector(toggleRecording),
            keyEquivalent: "r"
        )
        startStopItem.target = self

        menu.addItem(.separator())

        let permsItem = menu.addItem(
            withTitle: "Check Permissions…",
            action: #selector(showPermissions),
            keyEquivalent: ""
        )
        permsItem.target = self

        let openItem = menu.addItem(
            withTitle: "Open Data Folder",
            action: #selector(openDataFolder),
            keyEquivalent: ""
        )
        openItem.target = self

        menu.addItem(.separator())

        let aboutItem = menu.addItem(
            withTitle: "About Task Mining POC",
            action: #selector(showAbout),
            keyEquivalent: ""
        )
        aboutItem.target = self

        let quitItem = menu.addItem(
            withTitle: "Quit", action: #selector(quit), keyEquivalent: "q"
        )
        quitItem.target = self

        statusItem.menu = menu
    }

    // MARK: - Actions

    @objc private func toggleRecording() {
        if isRecording {
            captureEngine.stopRecording()
            startStopItem.title = "Start Recording"
            statusItem.button?.image = NSImage(
                systemSymbolName: "record.circle",
                accessibilityDescription: "Task Mining"
            )
        } else {
            captureEngine.startRecording()
            startStopItem.title = "Stop Recording"
            statusItem.button?.image = NSImage(
                systemSymbolName: "record.circle.fill",
                accessibilityDescription: "Task Mining — Recording"
            )
        }
        isRecording.toggle()
    }

    @objc private func showPermissions() {
        let hasA11y = AXIsProcessTrusted()

        let alert = NSAlert()
        alert.messageText = "Permission Status"
        alert.informativeText = """
        Accessibility: \(hasA11y ? "Granted" : "NOT granted")
        Screen Recording: Check System Settings > Privacy & Security
        Input Monitoring: Check System Settings > Privacy & Security

        \(hasA11y ? "" : "Click \"Request Accessibility\" to be prompted.\n")
        You may need to restart the app after granting permissions.
        """
        alert.alertStyle = .informational

        if !hasA11y {
            alert.addButton(withTitle: "Request Accessibility")
            alert.addButton(withTitle: "Open System Settings")
            alert.addButton(withTitle: "OK")
        } else {
            alert.addButton(withTitle: "Open System Settings")
            alert.addButton(withTitle: "OK")
        }

        NSApp.activate(ignoringOtherApps: true)
        let response = alert.runModal()

        if !hasA11y {
            if response == .alertFirstButtonReturn {
                AccessibilityReader.requestAccessibility()
            } else if response == .alertSecondButtonReturn {
                openPrivacySettings()
            }
        } else if response == .alertFirstButtonReturn {
            openPrivacySettings()
        }
    }

    @objc private func openDataFolder() {
        let dir = captureEngine.dataDirectory
        try? FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)
        NSWorkspace.shared.open(dir)
    }

    @objc private func showAbout() {
        let alert = NSAlert()
        alert.messageText = "Task Mining Mac POC"
        alert.informativeText = """
        Proof of Concept — Celonis Task Mining Client for macOS

        Captures:
          • Window switches (foreground app + title)
          • Mouse clicks (left / right)
          • Key presses
          • Clipboard changes
          • UI element metadata (Accessibility API)
          • Screenshots on click events

        Data stored in: ~/CelonisTaskMining/
        Format: JSONL (one JSON object per line)
        """
        alert.alertStyle = .informational
        alert.addButton(withTitle: "OK")
        NSApp.activate(ignoringOtherApps: true)
        alert.runModal()
    }

    @objc private func quit() {
        if isRecording { captureEngine.stopRecording() }
        NSApp.terminate(nil)
    }

    // MARK: - Helpers

    private func promptForPermissionsIfNeeded() {
        guard !AXIsProcessTrusted() else { return }
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) { [weak self] in
            self?.statusLabel.title = "Status: Accessibility permission needed"
            AccessibilityReader.requestAccessibility()
        }
    }

    private func openPrivacySettings() {
        if let url = URL(string: "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility") {
            NSWorkspace.shared.open(url)
        }
    }
}
