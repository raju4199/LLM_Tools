# LLMScan 🔍
### The Nikto for Large Language Models

An open-source CLI tool that automatically probes any LLM endpoint for security vulnerabilities and generates a detailed report.

## Installation

```bash
git clone https://github.com/yourusername/LLMScan.git
cd LLMScan
pip install -r requirements.txt
```

## Usage

```bash
# Test OpenAI endpoint
python llmscan.py --provider openai --key sk-xxxx --model gpt-4

# Test Anthropic Claude
python llmscan.py --provider anthropic --key sk-ant-xxxx --model claude-3-opus

# Test local Ollama model
python llmscan.py --provider ollama --model llama3

# Test any custom HTTP endpoint
python llmscan.py --provider http --url https://your-llm-api.com/chat

# Run specific test only
python llmscan.py --provider openai --key sk-xxxx --test jailbreak

# Save report to file
python llmscan.py --provider openai --key sk-xxxx --output report.json
```

## Test Categories

| Test | Description |
|------|-------------|
| `prompt_injection` | Tries to override system prompts via user input |
| `jailbreak` | Runs known jailbreak patterns (DAN, roleplay, encoding tricks) |
| `system_prompt_leak` | Tries to extract hidden system instructions |
| `data_exfiltration` | Checks if model reveals sensitive training data |
| `token_dos` | Tests for context window exhaustion attacks |

## Supported Providers

- ✅ OpenAI (GPT-3.5, GPT-4, GPT-4o)
- ✅ Anthropic (Claude 3 Opus, Sonnet, Haiku)
- ✅ Ollama (local open-source models)
- ✅ Any HTTP endpoint (generic support)

## Sample Output

```
[LLMScan v1.0] Starting scan against: gpt-4 (OpenAI)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[✓] PASS   Prompt Injection Basic       (12 tests)
[✗] VULN   Jailbreak — DAN Variant      Bypassed safety filter
[✓] PASS   System Prompt Leak           (8 tests)
[✗] VULN   Roleplay Escalation          Model complied with harmful request
[✓] PASS   Token DoS                    (3 tests)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Security Score: C  (2 vulnerabilities found)
Report saved: report_gpt4_2026-06-07.json
```

## Legal

Use this tool only on systems you have explicit permission to test.

## License

MIT License
