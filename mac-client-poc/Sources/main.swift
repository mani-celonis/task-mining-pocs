import AppKit

let app = NSApplication.shared
let delegate = AppDelegate()

// Support: --auto-record <seconds>
let args = CommandLine.arguments
if let idx = args.firstIndex(of: "--auto-record"),
   idx + 1 < args.count,
   let seconds = Int(args[idx + 1]) {
    delegate.autoRecordSeconds = seconds
}

app.delegate = delegate
app.run()
