# Open the vault with AhaAgent (Cursor)

PM markdown lives at `KNOWLEDGE_ROOT` (often an Obsidian vault on the same machine as the clone, e.g. under `Desktop`). For Cursor to apply product-tagging and to read/write those files:

1. **File → Add Folder to Workspace** and add your vault root (the folder that contains `AhaAgent/`), or  
2. **File → Open Folder** a **parent** directory that contains both the AhaAgent clone and the vault, or  
3. Use a **`.code-workspace`** file with two `folders` entries: one for the repo, one for the vault.

Rules use globs like `**/AhaAgent/**/*.md` so they match the vault when it is in the workspace. If only the repo is open, paths under the vault are still valid if you paste absolute paths or add the folder.

## Example multi-root workspace file

The repo includes [`ahaagent.with-vault.code-workspace.example`](../ahaagent.with-vault.code-workspace.example). Copy it to a local file in the **AhaAgent repository root** (same level as `src/`), so the first folder’s `.` points at the clone; if you store the workspace file elsewhere, set the first folder’s `path` to the absolute path of the clone. Edit the second folder’s `path` to your real vault root (the same directory you set as `KNOWLEDGE_ROOT` in `.env`). The placeholder `/path/to/your/vault` must be replaced; JSON does not support comments in the file itself.

Open the workspace in Cursor via **File → Open Workspace from File…**. The first folder is the AhaAgent repository; the second is your PM knowledge root.

After opening, confirm resolved paths (absolute directories, no secrets) with:

```bash
python scripts/print_knowledge_paths.py
```
