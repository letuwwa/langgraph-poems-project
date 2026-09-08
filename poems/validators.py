def validate_poem(draft: str, target_lines: int) -> list[str]:
    line_count = sum(bool(line.strip()) for line in draft.splitlines())

    if not line_count:
        return ["The poem is empty."]

    if line_count != target_lines:
        return [
            f"The poem has {line_count} nonempty lines; "
            f"it must have exactly {target_lines}."
        ]

    return []
