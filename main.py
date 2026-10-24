
# main.py

import json

from ollama import ResponseError
from httpx import ConnectError, TimeoutException

from settings import MODEL_NAME
from ollama_service import OllamaService

from prompt_templates import (
    GENERAL_SYSTEM,
    TUTOR_SYSTEM,
    TECHNICAL_SYSTEM,
    CLASSIFIER_SYSTEM,
    WRITER_SYSTEM,
    EXTRACTION_SYSTEM,
    build_clear_prompt,
    build_classification_prompt,
    build_email_prompt,
    build_revision_prompt
)


def read_text(label, max_chars=800):
    """Read and validate a short user input."""

    value = input(label).strip()

    if not value:
        print("Input is required.")
        return None

    if len(value) > max_chars:
        print(
            f"Input must not exceed {max_chars} characters."
        )
        return None

    return value


def compare_prompts(service):
    """Compare vague and specific prompts."""

    topic = read_text("\nEnter a Python topic: ")

    if topic is None:
        return

    vague_prompt = f"Explain {topic}."

    clear_prompt = build_clear_prompt(topic)

    print("\n--- VAGUE PROMPT ---")
    print(vague_prompt)

    answer1 = service.generate(
        GENERAL_SYSTEM,
        vague_prompt,
        max_tokens=250
    )

    print("\nResponse:")
    print(answer1)

    print("\n--- SPECIFIC PROMPT ---")
    print(clear_prompt)

    answer2 = service.generate(
        GENERAL_SYSTEM,
        clear_prompt,
        max_tokens=400
    )

    print("\nResponse:")
    print(answer2)


def compare_roles(service):
    """Compare two assistant roles."""

    topic = read_text(
        "\nEnter a Python concept: "
    )

    if topic is None:
        return

    question = f"Explain {topic}."

    print("\n--- PYTHON TUTOR ---")

    tutor_answer = service.generate(
        TUTOR_SYSTEM,
        question,
        max_tokens=300
    )

    print(tutor_answer)

    print("\n--- TECHNICAL ASSISTANT ---")

    technical_answer = service.generate(
        TECHNICAL_SYSTEM,
        question,
        max_tokens=300
    )

    print(technical_answer)


def few_shot_classification(service):
    """Classify a customer message using examples."""

    message = read_text(
        "\nEnter a customer message: "
    )

    if message is None:
        return

    prompt = build_classification_prompt(
        message
    )

    answer = service.generate(
        CLASSIFIER_SYSTEM,
        prompt,
        temperature=0.0,
        max_tokens=20
    )

    category = answer.strip().rstrip(".").title()

    allowed = {
        "Billing",
        "Technical",
        "General"
    }

    if category not in allowed:

        print(
            "\nThe model did not return "
            "a valid category."
        )

        print("Raw response:", answer)
        return

    print("\nCustomer Message:")
    print(message)

    print("\nPredicted Category:")
    print(category)


def extract_json(service):
    """Demonstrate structured JSON extraction."""

    source_text = (
        "Maya is 22 years old and is studying "
        "Python and Statistics."
    )

    schema = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string"
            },
            "age": {
                "type": "integer"
            },
            "courses": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": [
            "name",
            "age",
            "courses"
        ],
        "additionalProperties": False
    }

    prompt = f"""
Extract the student information
from the following sentence.

Source:
<source>
{source_text}
</source>

Return only the requested JSON object.
"""

    response_text = service.generate(
        EXTRACTION_SYSTEM,
        prompt,
        temperature=0.0,
        max_tokens=180,
        json_schema=schema
    )

    student = json.loads(response_text)

    # Validate the returned structure.
    if not isinstance(student, dict):
        raise ValueError(
            "Expected a JSON object."
        )

    if set(student.keys()) != {
        "name",
        "age",
        "courses"
    }:
        raise ValueError(
            "Unexpected JSON properties."
        )

    if (
        not isinstance(student["name"], str)
        or type(student["age"]) is not int
        or not isinstance(student["courses"], list)
        or not all(
            isinstance(item, str)
            for item in student["courses"]
        )
    ):
        raise ValueError(
            "Invalid JSON field types."
        )

    print("\nSource Text:")
    print(source_text)

    print("\nStructured JSON:")
    print(
        json.dumps(
            student,
            indent=4,
            ensure_ascii=False
        )
    )

    print("\nExtracted Values:")
    print("Name:", student["name"])
    print("Age:", student["age"])

    print(
        "Courses:",
        ", ".join(student["courses"])
    )


def generate_email(service):
    """Generate a business email from a template."""

    purpose = read_text(
        "\nEnter the email purpose: "
    )

    if purpose is None:
        return

    audience = read_text(
        "Enter the intended recipient or audience: "
    )

    if audience is None:
        return

    print("\nSelect a tone:")
    print("1. Formal")
    print("2. Friendly")

    choice = input("Choice (1/2): ").strip()

    tone = (
        "friendly and professional"
        if choice == "2"
        else "formal and professional"
    )

    prompt = build_email_prompt(
        purpose,
        audience,
        tone
    )

    response = service.generate(
        WRITER_SYSTEM,
        prompt,
        max_tokens=400
    )

    print("\n--- EMAIL DRAFT ---")
    print(response)

    print(
        "\nThis is a draft only. "
        "No email has been sent."
    )


def revise_email(service):
    """Generate and improve a draft using feedback."""

    purpose = read_text(
        "\nEnter the email purpose: "
    )

    if purpose is None:
        return

    audience = read_text(
        "Enter the intended audience: "
    )

    if audience is None:
        return

    initial_prompt = build_email_prompt(
        purpose,
        audience,
        "professional"
    )

    draft = service.generate(
        WRITER_SYSTEM,
        initial_prompt,
        max_tokens=400
    )

    print("\n--- ORIGINAL DRAFT ---")
    print(draft)

    feedback = read_text(
        "\nHow should this draft be improved? "
    )

    if feedback is None:
        return

    revision_prompt = build_revision_prompt(
        draft,
        feedback
    )

    revised = service.generate(
        WRITER_SYSTEM,
        revision_prompt,
        max_tokens=400
    )

    print("\n--- REVISED DRAFT ---")
    print(revised)

    print(
        "\nReview the revised content before use."
    )


def display_menu():

    print("\n====================================")
    print("       PROMPT ENGINEERING LAB")
    print("====================================")

    print("1. Compare vague and specific prompts")
    print("2. Compare assistant roles")
    print("3. Few-shot message classification")
    print("4. Structured JSON extraction")
    print("5. Generate a professional email")
    print("6. Generate and revise an email")
    print("0. Exit")


def main():

    service = OllamaService()

    print("Python Prompt Engineering Lab")
    print("Visual Studio 2026")
    print("Ollama Model:", MODEL_NAME)

    while True:

        display_menu()

        try:
            choice = input(
                "\nSelect an option: "
            ).strip()

            if choice == "0":
                print("Goodbye!")
                break

            if choice == "1":
                compare_prompts(service)

            elif choice == "2":
                compare_roles(service)

            elif choice == "3":
                few_shot_classification(service)

            elif choice == "4":
                extract_json(service)

            elif choice == "5":
                generate_email(service)

            elif choice == "6":
                revise_email(service)

            else:
                print("Invalid menu option.")

        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        except ResponseError as ex:
            print("\nOllama API error:")
            print(ex)

            print(
                "Check the Ollama server "
                "and installed model."
            )

        except ConnectError:
            print("\nCannot connect to Ollama.")

            print(
                "Ensure the server is running "
                "at localhost:11434."
            )

        except TimeoutException:
            print("\nThe AI request timed out.")

            print(
                "Try a smaller model or "
                "shorter response length."
            )

        except (ValueError, KeyError) as ex:
            print("\nResponse validation error:")
            print(ex)


if __name__ == "__main__":
    main()