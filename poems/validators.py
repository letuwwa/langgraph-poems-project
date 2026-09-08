def validate_poem(draft: str, target_lines: int) -> list[str]:
    lines = [line.strip() for line in draft.splitlines() if line.strip()]

    if not lines:
        return ["The poem is empty."]

    if len(lines) != target_lines:
        return [
            f"The poem has {len(lines)} nonempty lines; "
            f"it must have exactly {target_lines}."
        ]

    return []

