from poems.state import PoemState
from poems.model import create_model
from poems.validators import validate_poem


model = create_model()


def write_draft(state: PoemState) -> dict[str, str]:
    if state["form"] == "haiku":
        instructions = (
            "Write an English haiku with exactly three lines "
            "and a 5-7-5 syllable pattern."
        )
    else:
        instructions = (
            f"Write a poem with exactly {state['target_lines']} nonempty lines."
        )

    prompt = (
        f"{instructions}\n"
        f"Topic: {state['topic']}\n"
        f"Tone: {state['tone']}\n"
        "Return only the poem, without a title or explanation."
    )

    response = model.invoke(prompt)

    if not isinstance(response.content, str):
        raise ValueError("Expected the model to return poem text.")

    return {"draft": response.content.strip()}


def check_draft(state: PoemState) -> dict[str, list[str]]:
    target_lines = 3 if state["form"] == "haiku" else state["target_lines"]
    errors = validate_poem(state["draft"], target_lines)

    return {"validation_errors": errors}


def revise_draft(state: PoemState) -> dict[str, str | int]:
    if state["form"] == "haiku":
        instructions = "Use exactly three lines with a 5-7-5 syllable pattern."
    else:
        instructions = f"Use exactly {state['target_lines']} nonempty lines."

    feedback = "\n".join(f"- {error}" for error in state["validation_errors"])

    prompt = (
        "Revise the following poem to fix the listed problems.\n"
        f"Topic: {state['topic']}\n"
        f"Tone: {state['tone']}\n"
        f"Requirements: {instructions}\n\n"
        f"Current draft:\n{state['draft']}\n\n"
        f"Problems to fix:\n{feedback}\n\n"
        "Preserve the imagery and wording where possible.\n"
        "Return only the revised poem, without a title "
        "or explanation."
    )

    response = model.invoke(prompt)

    if not isinstance(response.content, str):
        raise ValueError("Expected the model to return poem text.")

    return {
        "draft": response.content.strip(),
        "revision_count": state["revision_count"] + 1,
    }
