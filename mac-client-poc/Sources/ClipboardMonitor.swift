import AppKit

/// Polls NSPasteboard.general.changeCount to detect clipboard changes.
/// Replaces the Windows client's AddClipboardFormatListener + hidden message window.
class ClipboardMonitor {
    var onClipboardChanged: (() -> Void)?

    private var lastChangeCount: Int = 0
    private var timer: Timer?

    func start() {
        lastChangeCount = NSPasteboard.general.changeCount
        timer = Timer.scheduledTimer(withTimeInterval: 0.5, repeats: true) { [weak self] _ in
            self?.check()
        }
    }

    func stop() {
        timer?.invalidate()
        timer = nil
    }

    private func check() {
        let current = NSPasteboard.general.changeCount
        guard current != lastChangeCount else { return }
        lastChangeCount = current
        onClipboardChanged?()
    }
}
