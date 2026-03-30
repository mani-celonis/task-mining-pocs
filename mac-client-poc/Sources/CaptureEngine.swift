import CoreGraphics
import Foundation
import AppKit

/// Orchestrates all capture components: on each input event it reads the active
/// window, queries the Accessibility tree, optionally takes a screenshot, builds
/// a TaskMiningEvent, and persists it.  Mirrors the role of the Windows client's
/// UIEventProcessorWorker + DataManagerEventsHandler pipeline.
class CaptureEngine {
    let eventStore = EventStore()

    private let windowTracker = WindowTracker()
    private let accessibilityReader = AccessibilityReader()
    private let screenshotCapture = ScreenshotCapture()
    private let eventTapMonitor = EventTapMonitor()
    private let clipboardMonitor = ClipboardMonitor()

    private var session: EventSession?
    private var isRecording = false
    private var lastWindowSignature = ""
    private var windowPollTimer: Timer?

    var onEventCountChanged: ((Int) -> Void)?
    var onStatusChanged: ((String) -> Void)?

    // MARK: - Public

    func startRecording() {
        guard !isRecording else { return }

        let newSession = EventSession()
        session = newSession
        eventStore.startSession(sessionId: newSession.id)
        isRecording = true

        // Input events
        eventTapMonitor.onEvent = { [weak self] type, event in
            self?.handleInputEvent(type: type, event: event)
        }
        let tapOk = eventTapMonitor.start()
        if !tapOk {
            onStatusChanged?("Event tap failed — grant Accessibility permission")
        }

        // Clipboard
        clipboardMonitor.onClipboardChanged = { [weak self] in
            self?.recordEvent(eventType: "Clipboard changed")
        }
        clipboardMonitor.start()

        // Foreground window polling
        windowPollTimer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
            self?.checkWindowChange()
        }

        recordEvent(eventType: "Task Mining Started")
        onStatusChanged?("Recording — session \(newSession.id.prefix(8))…")
    }

    func stopRecording() {
        guard isRecording else { return }

        recordEvent(eventType: "Task Mining Stopped")

        eventTapMonitor.stop()
        clipboardMonitor.stop()
        windowPollTimer?.invalidate()
        windowPollTimer = nil

        eventStore.stopSession()
        isRecording = false
        session = nil

        onStatusChanged?("Stopped")
    }

    var dataDirectory: URL { eventStore.dataDirectory }

    // MARK: - Internal event handlers

    private func handleInputEvent(type: CGEventType, event: CGEvent) {
        let location = event.location
        let eventType: String
        var keyCode: Int?
        var takeScreenshot = false

        switch type {
        case .leftMouseDown:
            eventType = "Left click"
            takeScreenshot = true
        case .rightMouseDown:
            eventType = "Right click"
            takeScreenshot = true
        case .leftMouseUp:
            eventType = "Left click released"
        case .keyDown:
            eventType = "Key press"
            keyCode = Int(event.getIntegerValueField(.keyboardEventKeycode))
        case .scrollWheel:
            eventType = "Scroll"
        default:
            eventType = "Other"
        }

        recordEvent(
            eventType: eventType,
            mouseLocation: location,
            keyCode: keyCode,
            modifierFlags: event.flags.rawValue,
            captureScreenshot: takeScreenshot
        )
    }

    private func checkWindowChange() {
        guard let window = windowTracker.getActiveWindow() else { return }
        let sig = "\(window.appName)|\(window.windowTitle)"
        guard sig != lastWindowSignature else { return }
        lastWindowSignature = sig
        recordEvent(eventType: "Window changed")
    }

    // MARK: - Event assembly

    private func recordEvent(
        eventType: String,
        mouseLocation: CGPoint? = nil,
        keyCode: Int? = nil,
        modifierFlags: UInt64? = nil,
        captureScreenshot: Bool = false
    ) {
        guard let session else { return }

        let windowInfo = windowTracker.getActiveWindow()

        // Accessibility enrichment
        var a11y: AccessibilityInfo?
        if let loc = mouseLocation {
            a11y = accessibilityReader.getElementAtPosition(x: Float(loc.x), y: Float(loc.y))
        } else {
            a11y = accessibilityReader.getFocusedElement()
        }

        // Screenshot (only on mouse clicks to keep volume sane)
        var screenshotPath: String?
        if captureScreenshot, let wInfo = windowInfo {
            let ssId = UUID().uuidString
            if let image = screenshotCapture.captureWindow(windowId: wInfo.windowId) {
                screenshotPath = eventStore.saveScreenshot(image: image, id: ssId)
            }
        }

        let event = TaskMiningEvent(
            sessionId: session.id,
            snippetId: session.getSnippetId(),
            timestamp: TaskMiningEvent.dateFormatter.string(from: Date()),
            eventType: eventType,
            applicationName: windowInfo?.appName ?? "Unknown",
            windowTitle: windowInfo?.windowTitle ?? "",
            processPath: windowInfo?.processPath ?? "",
            bundleId: windowInfo?.bundleId ?? "",
            mouseX: mouseLocation.map { Double($0.x) },
            mouseY: mouseLocation.map { Double($0.y) },
            keyCode: keyCode,
            modifierFlags: modifierFlags,
            elementName: a11y?.name,
            elementRole: a11y?.role,
            elementValue: a11y?.value,
            elementIdentifier: a11y?.identifier,
            screenshotPath: screenshotPath
        )

        eventStore.store(event: event)

        DispatchQueue.main.async { [weak self] in
            guard let self else { return }
            self.onEventCountChanged?(self.eventStore.eventCount)
        }
    }
}
