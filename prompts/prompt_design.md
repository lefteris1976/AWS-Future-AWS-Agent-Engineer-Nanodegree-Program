# Public prompt design

The deployed system prompt is not published verbatim. This document records its behavioural contract and design decisions without exposing reusable internal instructions.

## Routing contract

Every customer message is assigned to exactly one route:

1. **Bug report** — a technical malfunction in the shop website or app.
2. **Platform question** — a supported order, delivery, return, payment, product, account, or privacy question answerable from the FAQ.
3. **Other request** — anything outside those categories or not covered by the FAQ.

When a technical malfunction and another request appear together, the bug-report route has priority. Short follow-up messages remain part of the active bug-report conversation.

## Tool-use contract

The `create_bug_report` tool accepts three required fields:

- `description`: what failed and what the customer observed;
- `stepsToReproduce`: the concrete sequence that causes the failure;
- `environment`: browser or app, operating system, and device.

The agent requests one missing field at a time. It must not infer missing values, use placeholders, or call the tool early. After all fields are explicit, it calls the tool once, preserves the customer's meaning, and returns only the ticket ID supplied by the tool. A failed call must never be presented as a successful ticket.

## Grounding contract

Platform answers are grounded only in `knowledge/online_shop_faq.md`. The agent may paraphrase the FAQ but may not add unsupported policies, dates, prices, guarantees, or account-specific claims. An uncovered question is handed to human support.

## Adversarial-input contract

Customer text is treated as untrusted input. A prompt injection asking the agent to reveal instructions, bypass required fields, or fabricate a ticket must not change the routing or tool-use rules.

## Behavioural pseudocode

```text
route = classify(conversation)

if route == bug_report:
    collect description, stepsToReproduce, environment
    if any field is missing:
        ask one concise follow-up question
    else:
        result = create_bug_report(fields) exactly once
        report result.ticketId only after success

elif route == platform_question:
    answer only when supported by the FAQ

else:
    provide the human-support hand-off
```

Redacted excerpts from the implemented prompt are available in the `evidence/` directory.
