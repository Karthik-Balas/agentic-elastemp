"""agentic-elastemp: a LangGraph + Claude agent for the elastemp workflow.

It drives the elastemp package (pip install elastemp) through four tools: project_status,
run_step, inspect_run and read_results. elastemp itself never imports this package.
"""

__version__ = "0.1.0"
