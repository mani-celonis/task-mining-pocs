import Foundation
import CoreGraphics
import ImageIO

/// Thread-safe JSONL persistence for captured events and screenshots.
/// Stores under ~/CelonisTaskMining/sessions/{sessionId}/
class EventStore {
    private let queue = DispatchQueue(label: "com.celonis.taskmining.eventstore")
    private let baseDir: URL
    private var screenshotsDir: URL?
    private var eventsFileHandle: FileHandle?
    private let encoder: JSONEncoder = {
        let e = JSONEncoder()
        e.outputFormatting = .sortedKeys
        return e
    }()

    private(set) var eventCount = 0

    init() {
        baseDir = FileManager.default.homeDirectoryForCurrentUser
            .appendingPathComponent("CelonisTaskMining")
    }

    func startSession(sessionId: String) {
        queue.sync {
            let sessionDir = baseDir
                .appendingPathComponent("sessions")
                .appendingPathComponent(sessionId)
            let ssDir = sessionDir.appendingPathComponent("screenshots")
            try? FileManager.default.createDirectory(at: ssDir, withIntermediateDirectories: true)

            let eventsFile = sessionDir.appendingPathComponent("events.jsonl")
            FileManager.default.createFile(atPath: eventsFile.path, contents: nil)
            eventsFileHandle = FileHandle(forWritingAtPath: eventsFile.path)
            eventsFileHandle?.seekToEndOfFile()

            screenshotsDir = ssDir
            eventCount = 0
        }
    }

    func stopSession() {
        queue.sync {
            eventsFileHandle?.closeFile()
            eventsFileHandle = nil
            screenshotsDir = nil
        }
    }

    func store(event: TaskMiningEvent) {
        queue.async { [weak self] in
            guard let self, let handle = self.eventsFileHandle else { return }
            guard var data = try? self.encoder.encode(event) else { return }
            data.append(0x0A) // newline
            handle.write(data)
            self.eventCount += 1
        }
    }

    func saveScreenshot(image: CGImage, id: String) -> String? {
        var result: String?
        queue.sync {
            guard let dir = screenshotsDir else { return }
            let url = dir.appendingPathComponent("\(id).png")
            guard let dest = CGImageDestinationCreateWithURL(
                url as CFURL, "public.png" as CFString, 1, nil
            ) else { return }
            CGImageDestinationAddImage(dest, image, nil)
            if CGImageDestinationFinalize(dest) {
                result = url.path
            }
        }
        return result
    }

    var dataDirectory: URL { baseDir }
}
