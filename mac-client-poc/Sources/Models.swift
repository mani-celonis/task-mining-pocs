import Foundation
import CoreGraphics

// Mirrors the Windows client's DefaultSchemaKeys where applicable
struct TaskMiningEvent: Codable {
    let sessionId: String
    let snippetId: String
    let timestamp: String
    let eventType: String
    let applicationName: String
    let windowTitle: String
    let processPath: String
    let bundleId: String
    let mouseX: Double?
    let mouseY: Double?
    let keyCode: Int?
    let modifierFlags: UInt64?
    let elementName: String?
    let elementRole: String?
    let elementValue: String?
    let elementIdentifier: String?
    let screenshotPath: String?

    static let dateFormatter: ISO8601DateFormatter = {
        let f = ISO8601DateFormatter()
        f.formatOptions = [.withInternetDateTime, .withFractionalSeconds]
        return f
    }()
}

struct ActiveWindowInfo {
    let appName: String
    let bundleId: String
    let windowTitle: String
    let windowId: CGWindowID
    let bounds: CGRect
    let processPath: String
    let pid: pid_t
}

struct AccessibilityInfo {
    let name: String?
    let role: String?
    let roleDescription: String?
    let value: String?
    let identifier: String?
}

/// Manages session identity and time-based snippet splitting (mirrors Windows EventSession)
class EventSession {
    let id: String
    private var nextSnippetId = 0
    private var lastEventTime: Date
    private let snippetSplitSeconds: TimeInterval

    init(snippetSplitSeconds: TimeInterval = 300) {
        self.id = UUID().uuidString
        self.lastEventTime = Date()
        self.snippetSplitSeconds = snippetSplitSeconds
    }

    func getSnippetId() -> String {
        let now = Date()
        if now.timeIntervalSince(lastEventTime) > snippetSplitSeconds {
            nextSnippetId += 1
        }
        lastEventTime = now
        return "\(id)_\(nextSnippetId)"
    }
}
