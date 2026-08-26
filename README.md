# Customer Support AI Agent on Amazon Bedrock AgentCore

A stateful customer-support agent for a fictional online shop. It routes each request to one of three behaviors, gathers complete bug diagnostics across multiple turns, creates a ticket through an AWS Lambda tool, answers supported questions from a grounded FAQ, and hands unsupported requests to human support.

This is a sanitized portfolio edition of a completed Udacity project. It contains the student-authored prompt design, test specification, evaluation summary, and redacted evidence. Course starter infrastructure and account-specific AWS configuration are intentionally excluded.

## What the agent does

| Route | Behaviour | Safety rule |
|---|---|---|
| Bug report | Collects the description, reproduction steps, and environment, then calls `create_bug_report` | The tool is forbidden until all three fields are explicit |
| Platform question | Answers orders, shipping, returns, payment, account, and privacy questions from the embedded FAQ | No policy is invented beyond the FAQ |
| Other or unsupported | Provides a concise human-support hand-off | No attempt is made to answer outside the supported scope |

The prompt also treats customer text as untrusted input and rejects attempts to reveal instructions, bypass required fields, or fabricate a successful tool call.

## Architecture

```mermaid
flowchart TD
    U[Customer message] --> H[AgentCore managed harness]
    H --> R{Prompt-based routing}
    R -->|Bug report| G[AgentCore Gateway]
    G --> L[AWS Lambda tool]
    L --> D[(Amazon DynamoDB)]
    R -->|Platform question| F[Embedded FAQ]
    R -->|Unsupported| S[Human support hand-off]
    H --> T[JSONL evaluation dataset]
    T --> E[Amazon Bedrock Evaluations]
```

The deployed implementation used Amazon Nova Pro, Amazon Bedrock AgentCore Gateway, AWS Lambda, Amazon DynamoDB, and Amazon Bedrock Evaluations with an LLM-as-a-judge workflow.

## Evaluation results

| Measure | Result |
|---|---:|
| Automated prompts | 7 |
| Valid JSONL records | 7 |
| Harness errors | 0 |
| Metric | `Builtin.Correctness` |
| Average correctness | **1.00** |
| Evaluator | `amazon.nova-pro-v1:0` |

The suite covered initial bug-report collection, grounded delivery and payment answers, an uncovered FAQ question, an unrelated request, prompt injection, and an ambiguous short message. A separate multi-turn test verified one tool call only after all required fields were collected and confirmed the ticket in DynamoDB.

See [evaluation observations](evaluation/observations.md) and the [sanitized evaluation evidence](evidence/07_evaluation_metrics.png).

## Evidence

### Multi-turn tool use

![Multi-turn bug-report conversation](evidence/01_bug_report_chat.png)

### Ticket persistence

![Bug report stored in DynamoDB](evidence/02_dynamodb_ticket.png)

### Automated evaluation

![Bedrock evaluation metrics](evidence/07_evaluation_metrics.png)

### Prompt-injection handling

![Prompt-injection test](evidence/08_prompt_injection.png)

Additional screenshots in [`evidence/`](evidence/) show FAQ grounding, unsupported-request hand-off, test coverage, and the prompt's routing and tool-use gate.

## Repository layout

```text
.
├── prompts/prompt_design.md           # Public behaviour contract and pseudocode
├── knowledge/online_shop_faq.md       # Fictional grounding document
├── tests/harness-tests.json           # Seven behavioural test specifications
├── evaluation/                        # Sanitized metrics and observations
├── evidence/                          # Redacted screenshots from the completed run
└── scripts/validate_portfolio.py      # Offline integrity and secret checks
```

## Validate locally

No AWS credentials or third-party packages are required for the public validation scripts.

```bash
python scripts/validate_portfolio.py
```

The verbatim deployed system prompt and AWS deployment scripts are not published. The public behaviour contract, redacted prompt excerpts, tests, and evidence demonstrate the prompt engineering, agent routing, tool-call gating, grounding, adversarial testing, and evaluation work without exposing reusable internal instructions or course starter code.

## Design decisions

- **Prompt-first routing:** one explicit decision among three mutually exclusive behaviours.
- **Stateful collection:** missing bug fields are requested one at a time across turns.
- **Hard tool gate:** no partial arguments, dummy values, or fabricated ticket IDs.
- **Grounded answers:** platform policy comes only from the embedded FAQ.
- **Safe fallback:** unsupported or uncovered requests are handed to human support.
- **Evaluation before claims:** results are reported only from the completed seven-prompt evaluation run.

## Related documentation

- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)
- [Amazon Bedrock model evaluations](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html)
- [Udacity AWS AI Practitioner Challenge certificate](https://www.udacity.com/certificate/e/cafe36ce-27b2-11f1-a4fc-13974a346eab)

## Author

**Lefteris Iordanidis**

[LinkedIn](https://www.linkedin.com/in/lefteris-iordanidis-ab110835) · [GitHub](https://github.com/lefteris1976)

## Disclaimer

Educational portfolio project for a fictional online shop. Not affiliated with or endorsed by Amazon Web Services or Udacity. AWS service names and trademarks belong to their respective owners.
