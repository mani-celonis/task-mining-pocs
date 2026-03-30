import AppKit
import CoreGraphics

/// Reads the current foreground window via NSWorkspace + CGWindowList.
/// Replaces the Windows client's GetForegroundWindow / GetWindowText / QueryFullProcessImageName.
class WindowTracker {

    func getActiveWindow() -> ActiveWindowInfo? {
        guard let frontApp = NSWorkspace.shared.frontmostApplication else { return nil }

        let pid = frontApp.processIdentifier
        let appName = frontApp.localizedName ?? "Unknown"
        let bundleId = frontApp.bundleIdentifier ?? ""
        let processPath = frontApp.bundleURL?.path ?? ""

        guard let windowList = CGWindowListCopyWindowInfo(
            [.optionOnScreenOnly, .excludeDesktopElements],
            kCGNullWindowID
        ) as? [[String: Any]] else {
            return ActiveWindowInfo(
                appName: appName, bundleId: bundleId, windowTitle: "",
                windowId: 0, bounds: .zero, processPath: processPath, pid: pid
            )
        }

        for window in windowList {
            guard let ownerPID = window[kCGWindowOwnerPID as String] as? Int,
                  ownerPID == Int(pid),
                  let layer = window[kCGWindowLayer as String] as? Int,
                  layer == 0,
                  let windowNumber = window[kCGWindowNumber as String] as? Int
            else { continue }

            let title = window[kCGWindowName as String] as? String ?? ""
            var bounds = CGRect.zero
            if let bd = window[kCGWindowBounds as String] as? NSDictionary {
                CGRectMakeWithDictionaryRepresentation(bd, &bounds)
            }

            return ActiveWindowInfo(
                appName: appName, bundleId: bundleId, windowTitle: title,
                windowId: CGWindowID(windowNumber), bounds: bounds,
                processPath: processPath, pid: pid
            )
        }

        return ActiveWindowInfo(
            appName: appName, bundleId: bundleId, windowTitle: "",
            windowId: 0, bounds: .zero, processPath: processPath, pid: pid
        )
    }
}
