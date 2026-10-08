# PID Standard Library V1

This directory contains a deterministic PID symbol and PSV-A process branch library.

## Contents

- `data/pid_standard_library_v1.json` is the single source of truth for the library metadata.
- `symbols/` contains deterministic SVG drawing assets built from SVG primitives.
- `modules/` contains reusable module SVGs.
- `previews/` contains SVG and PNG review previews.
- `scripts/validate_pid_library.py` validates the required library invariants.

## Rules

- SVG files are deterministic drawing assets. Formal PID output must not be drawn directly with generative image models.
- PNG files are previews only and are not the source of truth.
- Template values such as `PSV 001A`, `6Q8`, `SET@`, and `1.63MPag` are marked as `template_value_not_project_confirmed`; they are not final project values.
- Unconfirmed engineering values must stay as `null` or `TBD`.
- The low point drain terminal remains `null`; allowed candidates are only `open_service_drain` and `close_service_drain` until project data confirms one.

## Important Source Note

The prompt requested preserving a provided `pid_standard_library_v1.json` verbatim, but no JSON file was attached in this session. The JSON here is constructed only from explicit requirements in `CODEX_PROMPT_build_pid_standard_library_v1.md`; replace or reconcile it with the original project JSON when that source is available.

## Validation

Run:

```bash
python3 pid-standard-library/scripts/validate_pid_library.py
```
