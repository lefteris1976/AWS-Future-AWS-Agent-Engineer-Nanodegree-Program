# Bedrock evaluation observations

## Configuration

- Job: `support-chatbot-eval-run-1`
- Region: `us-east-1`
- Evaluator: `amazon.nova-pro-v1:0`
- Inference source: `my-support-chatbot`
- Dataset: 7 prompts
- Metric: `Builtin.Correctness`
- Average correctness: **1.00**

## Coverage

The evaluation dataset covered:

- initial bug-report information collection;
- FAQ-grounded delivery and payment questions;
- a delivery question not explicitly covered by the FAQ;
- an out-of-scope request;
- a prompt-injection attempt;
- a short, ambiguous checkout issue.

## Findings

All seven records received a correctness score of 1.0. The agent began collecting missing bug information without creating a premature ticket. In a separate manual multi-turn test, it called `create_bug_report` exactly once after the description, reproduction steps, and environment were available, and the resulting ticket appeared in DynamoDB.

Covered platform questions were answered from the embedded FAQ. Uncovered and unrelated requests were redirected to the human support line without invented information. The injection test neither revealed the system prompt nor created a fake ticket. The ambiguous checkout message was handled by requesting clarification instead of immediately invoking the tool.

Some answers included support contact information beyond the reference response. The evaluator considered that additional information consistent with the expected behaviour.

AWS account identifiers, ARNs, bucket names, and session-specific details have been removed from this public summary.
