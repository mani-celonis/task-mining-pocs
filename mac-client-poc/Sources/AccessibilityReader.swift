import AppKit
import ApplicationServices

/// Reads UI element metadata via the macOS Accessibility API (AXUIElement).
/// Replaces the Windows client's COM UIAutomation (CUIAutomation8).
class AccessibilityReader {

    func getElementAtPosition(x: Float, y: Float) -> AccessibilityInfo? {
        let systemWide = AXUIElementCreateSystemWide()
        var element: AXUIElement?
        let result = AXUIElementCopyElementAtPosition(systemWide, x, y, &element)
        guard result == .success, let element else { return nil }
        return readAttributes(element)
    }

    func getFocusedElement() -> AccessibilityInfo? {
        guard let frontApp = NSWorkspace.shared.frontmostApplication else { return nil }
        let appElement = AXUIElementCreateApplication(frontApp.processIdentifier)

        var focusedRef: CFTypeRef?
        let result = AXUIElementCopyAttributeValue(
            appElement, kAXFocusedUIElementAttribute as CFString, &focusedRef
        )
        guard result == .success, let ref = focusedRef else { return nil }
        // The returned CFTypeRef is an AXUIElement
        let element = ref as! AXUIElement
        return readAttributes(element)
    }

    // MARK: - Permission helpers

    static func isAccessibilityEnabled() -> Bool {
        AXIsProcessTrusted()
    }

    static func requestAccessibility() {
        let opts = [kAXTrustedCheckOptionPrompt.takeUnretainedValue(): true] as CFDictionary
        AXIsProcessTrustedWithOptions(opts)
    }

    // MARK: - Private

    private func readAttributes(_ element: AXUIElement) -> AccessibilityInfo {
        AccessibilityInfo(
            name: stringAttr(element, kAXTitleAttribute),
            role: stringAttr(element, kAXRoleAttribute),
            roleDescription: stringAttr(element, kAXRoleDescriptionAttribute),
            value: stringAttr(element, kAXValueAttribute),
            identifier: stringAttr(element, "AXIdentifier")
        )
    }

    private func stringAttr(_ element: AXUIElement, _ attribute: String) -> String? {
        var value: CFTypeRef?
        guard AXUIElementCopyAttributeValue(element, attribute as CFString, &value) == .success
        else { return nil }
        return value as? String
    }
}
