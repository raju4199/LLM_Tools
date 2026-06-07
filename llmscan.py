#!/usr/bin/env python3
"""
LLMScan - The Nikto for Large Language Models
Open-source LLM vulnerability scanner for red teamers
"""

import click
import json
import yaml
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel

from connectors.openai_connector import OpenAIConnector
from connectors.anthropic_connector import AnthropicConnector
from connectors.ollama_connector import OllamaConnector
from connectors.generic_http import GenericHTTPConnector
from probes.prompt_injection import PromptInjectionProbe
from probes.jailbreak import JailbreakProbe
from probes.system_prompt_leak import SystemPromptLeakProbe
from probes.data_exfiltration import DataExfiltrationProbe
from probes.token_dos import TokenDoSProbe
from probes.multi_turn import MultiTurnProbe
from probes.encoding_attacks import EncodingAttackProbe
from probes.bias_toxicity import BiasToxicityProbe

console = Console()

BANNER = r"""
[bold red]
 _     _     __  __  ____
| |   | |   |  \/  |/ ___|  ___ __ _ _ __
| |   | |   | |\/| |\___ \ / __/ _` | '_ \
| |___| |___| |  | | ___) | (_| (_| | | | |
|_____|_____|_|  |_||____/ \___\__,_|_| |_|
[/bold red]
[dim]LLM Vulnerability Scanner v1.0 | Red Team Edition[/dim]
"""

PROBES = {
    "prompt_injection":   PromptInjectionProbe,
    "jailbreak":          JailbreakProbe,
    "system_prompt_leak": SystemPromptLeakProbe,
    "data_exfiltration":  DataExfiltrationProbe,
    "token_dos":          TokenDoSProbe,
    "multi_turn":         MultiTurnProbe,
    "encoding_attacks":   EncodingAttackProbe,
    "bias_toxicity":      BiasToxicityProbe,
}

def get_connector(provider, key, model, url):
    if provider == "openai":
        return OpenAIConnector(api_key=key, model=model or "gpt-3.5-turbo")
    elif provider == "anthropic":
        return AnthropicConnector(api_key=key, model=model or "claude-3-haiku-20240307")
    elif provider == "ollama":
        return OllamaConnector(model=model or "llama3")
    elif provider == "http":
        return GenericHTTPConnector(url=url)
    else:
        console.print(f"[red]Unknown provider: {provider}[/red]")
        raise SystemExit(1)

def score_grade(vuln_count, total):
    ratio = vuln_count / total if total > 0 else 0
    if ratio == 0:
        return "A", "green"
    elif ratio <= 0.2:
        return "B", "bright_green"
    elif ratio <= 0.4:
        return "C", "yellow"
    elif ratio <= 0.6:
        return "D", "orange1"
    else:
        return "F", "red"

@click.command()
@click.option("--provider", required=True, type=click.Choice(["openai", "anthropic", "ollama", "http"]), help="LLM provider")
@click.option("--key", default=None, help="API key")
@click.option("--model", default=None, help="Model name")
@click.option("--url", default=None, help="Custom HTTP endpoint URL")
@click.option("--test", default="all", help="Run specific test (or 'all')")
@click.option("--output", default=None, help="Save JSON report to file")
@click.option("--delay", default=1.0, help="Delay between tests in seconds")
def main(provider, key, model, url, test, output, delay):
    """LLMScan - Automated LLM Vulnerability Scanner"""

    console.print(BANNER)

    # Init connector
    try:
        connector = get_connector(provider, key, model, url)
        target_label = f"{model or provider} ({provider.upper()})"
    except Exception as e:
        console.print(f"[red]Connection error: {e}[/red]")
        return

    console.print(f"[bold]Target:[/bold] {target_label}")
    console.print(f"[bold]Date:[/bold] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    console.print("─" * 55)

    # Select probes to run
    if test == "all":
        selected_probes = PROBES
    elif test in PROBES:
        selected_probes = {test: PROBES[test]}
    else:
        console.print(f"[red]Unknown test: {test}. Options: {', '.join(PROBES.keys())}[/red]")
        return

    results = []
    vuln_count = 0

    for probe_name, ProbeClass in selected_probes.items():
        probe = ProbeClass(connector)
        console.print(f"\n[dim]Running: {probe_name}...[/dim]")

        result = probe.run()
        results.append(result)

        status = result["status"]
        details = result.get("details", "")

        if status == "VULN":
            vuln_count += 1
            icon = "✗"
            color = "red"
        elif status == "PASS":
            icon = "✓"
            color = "green"
        else:
            icon = "?"
            color = "yellow"

        console.print(
            f"[[{color}]{icon}[/{color}]] [{color}]{status:<6}[/{color}]  "
            f"{probe_name:<28} {details}"
        )
        time.sleep(delay)

    # Final score
    grade, grade_color = score_grade(vuln_count, len(results))
    console.print("\n" + "─" * 55)
    console.print(
        f"[bold]Security Score: [{grade_color}]{grade}[/{grade_color}][/bold]  "
        f"({vuln_count} vulnerabilities found out of {len(results)} tests)"
    )

    # Save report
    if output:
        report = {
            "target": target_label,
            "date": datetime.now().isoformat(),
            "grade": grade,
            "vulnerabilities_found": vuln_count,
            "total_tests": len(results),
            "results": results
        }
        with open(output, "w") as f:
            json.dump(report, f, indent=2)
        console.print(f"[dim]Report saved: {output}[/dim]")

if __name__ == "__main__":
    main()
