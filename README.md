# agentic-elastemp

An LLM agent for [elastemp](https://github.com/Karthik-Balas/elastemp), the workflow that computes quasi-harmonic, temperature-dependent elastic constants from VASP and phonopy. It is built with LangGraph and uses Claude.

You ask about a project in plain language. The agent can tell you where the project stands, run the next analysis step, explain why a VASP run failed, and summarize the results. **It never runs or submits VASP jobs; you still do that.**

## Install

```
pip install agentic-elastemp
```

This also installs elastemp, LangGraph and the Anthropic client. Python 3.10 or newer is required.

## API key

The agent needs a Claude API key. It reads `ANTHROPIC_API_KEY` from the environment or from a `.env` file in the current or project folder:

```
cp .env.example .env      # then fill in ANTHROPIC_API_KEY=...
```

`.env` is in `.gitignore`. Never commit a real key; `.env.example` holds empty placeholders only. To choose the Claude model, set `ELASTEMP_AGENT_MODEL` in `.env` or pass `--model`.

## Use

```
elastemp-agent --workdir runs/TiN                                   # conversation
elastemp-agent --workdir runs/TiN --ask "What should I run next?"   # one question
```

Type `exit` (or press Ctrl+D) to leave a conversation.

Example:

```
you> The VASP jobs finished. Where do we stand?
   [tool] project_status()

agent> The static runs are back: 43 of 44 converged, 1 failed. deformation-3/strain-2 hit NELM
(electronic SCF did not converge). Every deformation still has at least 7 converged points, so
get_elastic can drop that point and refit. You could also rerun it with a larger NELM first.

you> Rerun make_bulk_dynamic.
   [tool] run_step({"step": "make_bulk_dynamic"})

agent> I haven't run it. make_bulk_dynamic would delete 11 Phonon_calculation folders that already
contain finished DFPT runs. Do you want me to go ahead and delete them?
```

## How it works

The agent has four tools. All of them are deterministic code on top of elastemp:

| Tool | Purpose |
|---|---|
| `project_status` | Which steps are done, which VASP runs are finished, failed or missing, and what comes next |
| `run_step` | Run one elastemp step. A step that would delete finished VASP runs (for example rerunning `make_bulk_dynamic`) is refused unless you explicitly confirm |
| `inspect_run` | Convergence verdict (from vasprun.xml) and OSZICAR/OUTCAR evidence for one run |
| `read_results` | Elastic constants, moduli, stability, temperature dependence, consistency checks and flags |

```
START -> agent --(tool calls)--> tools -> agent
               --(answer)--> verify --(ok)--> END
                                    --(invented numbers)--> agent (one rewrite)
```

**Number check:** after each answer, a verify node compares every number in it with the tool results. If the agent states a value that came from nowhere (an "experimental" value from memory, say), it is asked to rewrite the answer once. If it still does, the answer is shown with an `[Unverified: ...]` note.

## Development

```
pip install -e ".[dev]"
pytest
```

The tests replace Claude with a scripted model, so they need no API key and make no network calls.

## License

MIT. See [LICENSE](LICENSE).
