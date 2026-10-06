---
name: ai-check
description: 'Standards for features that call an AI provider: settings, service layer, usage log, GBP and USD pricing, spend cap and budgets, data rules, mock mode. Use when adding or reviewing code that calls an LLM or AI API.'
---

# ai-check

Standards for AI-integrated systems. Apply when a feature calls an AI provider. AI usage must be visible, limited and priced.

[S] = Safe and Risk; no tag = Risk only.

**Scope.** Rule 8 in `dev-process`: apply to the lines this task changes or adds; note nearby gaps as "Noticed, not changed".

- **Settings page.** Provider, model, API key (masked), limits, model options, mock mode. Store the key encrypted or in a secret store, never as plaintext in the database or in code.
- **Service layer.** One service for every AI call. Timeouts, safe retries, clear failure messages.
- [S] **Usage log.** Log every call: model, tokens in, tokens out, cost, feature, user, time.
- **Dashboard.** today, this month, by feature, by user.
- **Pricing in GBP and USD.** Prices per 1M tokens and the USD to GBP rate live in settings, never in code. Every cost is shown in both currencies.
- [S] **Spend cap.** A monthly spending limit that stops or degrades AI calls when reached.
- **Budgets.** Per-user limits, with a warning bar and an alert before the limit.
- [S] **Data rules.** No secrets or customer data in prompts. Follow the prompt-data classes. Redact personal data before sending. Log prompts only when policy allows.
- **Testing.** Mock mode and a test for the cost calculation.

Illustrative cost calculation (rates come from settings):

```
usd = (tokens_in * price_in + tokens_out * price_out) / 1,000,000
gbp = usd * usd_to_gbp_rate
```

Proof to gather: settings screen, a usage-log row, dashboard screenshot, cost shown in GBP and USD, a budget alert firing in test, mock mode output, the cost-calculation test.
