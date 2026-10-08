#!/usr/bin/env python3
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "pid_standard_library_v1.json"


def fail(message):
    print(f"FAIL: {message}", file=sys.stderr)
    return 1


def unique(items, key):
    values = [item.get(key) for item in items]
    return len(values) == len(set(values))


def main():
    try:
        data = json.loads(DATA.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"JSON is not parseable: {exc}")

    symbols = data.get("symbols", [])
    modules = data.get("modules", [])
    symbol_ids = {item.get("symbol_id") for item in symbols}
    module_ids = {item.get("module_id") for item in modules}

    if not unique(symbols, "symbol_id"):
        return fail("symbol_id values are not unique")
    if not unique(modules, "module_id"):
        return fail("module_id values are not unique")

    for module in modules:
        referenced = set(module.get("symbols", []))
        referenced.update(module.get("components", {}).get("symbols", []))
        missing = sorted(referenced - symbol_ids)
        if missing:
            return fail(f"{module.get('module_id')} references missing symbols: {missing}")

    pipeline_numbers = {item.get("line_no") for item in data.get("pipelines", [])}
    for required in [
        "200-P-000104-B1TBA1-N",
        "200-P-000105-B1TBA1-N",
        "200-NFH-000101-A3TBB2R-N",
    ]:
        if required not in pipeline_numbers:
            return fail(f"required pipeline number is missing: {required}")

    symbol_by_id = {item.get("symbol_id"): item for item in symbols}
    for required in ["SB-NO", "SB-NC"]:
        symbol = symbol_by_id.get(required)
        if not symbol:
            return fail(f"{required} is missing")
        if symbol.get("connector_short_line_required") is not True:
            return fail(f"{required} connector_short_line_required must be true")
        if symbol.get("connector_short_line_length_rule") != "same_as_blind_body_short_line_length":
            return fail(f"{required} connector_short_line_length_rule is wrong")

    low_point = next((item for item in modules if item.get("module_id") == "low_point_drain_module"), None)
    if not low_point:
        return fail("low_point_drain_module is missing")
    components = low_point.get("components", {})
    if components.get("terminal_type") is not None:
        return fail("low_point_drain_module.components.terminal_type must be null")
    if components.get("isolation_valve_type") not in (None, "TBD"):
        return fail("low_point_drain_module isolation valve type must remain null/TBD")
    if components.get("terminal_type_candidates") != ["open_service_drain", "close_service_drain"]:
        return fail("low point drain terminal candidates changed")

    serialized = json.dumps(data, ensure_ascii=False)
    forbidden_inferred_values = ["open_service_drain_selected", "close_service_drain_selected"]
    for value in forbidden_inferred_values:
        if value in serialized:
            return fail(f"found inferred value: {value}")

    print("OK: PID standard library validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
