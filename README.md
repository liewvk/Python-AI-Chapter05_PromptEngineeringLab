# Python AI Chapter 05: Prompt Engineering Lab

This repository is a small interactive Python lab for experimenting with prompt engineering patterns using a local Ollama model.

It demonstrates how prompt design affects output quality across several common AI tasks, including:

- comparing vague vs. specific prompts
- comparing assistant roles
- few-shot message classification
- structured JSON extraction from text
- drafting professional emails
- revising a draft based on feedback

## Project purpose

The app is designed as a menu-driven console lab for testing how different prompt formulations influence model responses. It is useful for learning the practical differences between:

- generic prompts and detailed prompts
- different "persona" instructions
- examples vs. zero-shot prompting
- constrained output and structured extraction
- iterative refinement through feedback

## Repository contents

- `main.py` — interactive lab menu and workflow logic
- `ollama_service.py` — wrapper for calling the local Ollama API
- `prompt_templates.py` — reusable prompt templates for each exercise
- `settings.py` — runtime configuration, including local Ollama host and model name
- `requirements.txt` — Python dependencies

## Requirements

- Python 3.10+
- Ollama installed and running locally
- A downloaded model compatible with the configured model name

The default model is configured in `settings.py` as:

- `qwen3:8b`

## Setup

1. Clone the repository.
2. Create and activate a virtual environment if desired.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the Ollama service locally:

```bash
ollama serve
```

5. Pull the model used by the lab:

```bash
ollama pull qwen3:8b
```

6. Run the lab:

```bash
python main.py
```

## Usage

When the application starts, it presents a menu with the following options:

1. Compare vague and specific prompts
2. Compare assistant roles
3. Few-shot message classification
4. Structured JSON extraction
5. Generate a professional email
6. Generate and revise an email
0. Exit

Select an option and follow the prompts to test the different behaviors.

## Notes

- This project expects Ollama to be available on `http://localhost:11434`.
- The application uses a local model rather than cloud APIs, making it appropriate for offline experimentation.
- The templates in `prompt_templates.py` are intentionally simple and educational, designed to highlight prompt-engineering tradeoffs clearly.

## License

This project is provided as a learning exercise and is not explicitly licensed in the repository.
