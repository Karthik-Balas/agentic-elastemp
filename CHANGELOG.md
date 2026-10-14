# Changelog

## [0.1.0]

* First release, split out of elastemp 0.2.1 (where it was the `elastemp[agent]` extra). Requires elastemp 0.2.2 or newer.
* `elastemp-agent` command: a LangGraph agent using Claude, with four tools (`project_status`, `run_step`, `inspect_run`, `read_results`).
* `run_step` refuses steps that would delete finished VASP runs unless the user confirms.
* A verification node checks every number in the agent's answer against the tool results; an invented value triggers one rewrite, then an `[Unverified]` note.
* Answers are plain text for the terminal.
* The API key comes from `ANTHROPIC_API_KEY` or a local `.env` file (template: `.env.example`); no key is stored in the code.
