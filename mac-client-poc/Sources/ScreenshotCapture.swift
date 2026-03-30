import CoreGraphics

/// Captures screenshots using CGWindowListCreateImage.
/// Replaces the Windows client's GDI BitBlt / PrintWindow approach.
class ScreenshotCapture {

    /// Capture a single window by its CGWindowID.
    func captureWindow(windowId: CGWindowID) -> CGImage? {
        guard windowId != 0 else { return captureMainDisplay() }
        return CGWindowListCreateImage(
            .null,
            .optionIncludingWindow,
            windowId,
            [.boundsIgnoreFraming, .bestResolution]
        )
    }

    /// Fallback: capture the entire main display.
    func captureMainDisplay() -> CGImage? {
        CGWindowListCreateImage(
            CGRect(x: 0, y: 0,
                   width: CGFloat(CGDisplayPixelsWide(CGMainDisplayID())),
                   height: CGFloat(CGDisplayPixelsHigh(CGMainDisplayID()))),
            .optionOnScreenOnly,
            kCGNullWindowID,
            [.boundsIgnoreFraming]
        )
    }
}
