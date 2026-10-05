---
name: ai-check
description: 'Apply and check the standards for features that call an AI provider: settings page, one service layer, usage log and dashboard, GBP and USD pricing in settings, budgets, data rules, mock mode. Use when adding or reviewing any code that calls an LLM or AI API.'
---

# ai-check

Standards for AI-integrated systems. Full tier.


Apply when a feature calls an AI provider. AI usage must be visible, limited and priced. Full tier.

**Scope.** Apply these standards to the lines and components this task changes or adds, not to the rest of the file or screen. Do not refactor existing code to meet them. If existing code nearby breaks a standard, leave it and note it under "Noticed, not changed" in the handoff.

1. **Settings page.** Provider, model, API key (masked), limits, model options, mock mode. Store the key encrypted or in a secret store, never as plaintext in the database or in code.
2. **Service layer.** One service for every AI call. Timeouts, safe retries, clear failure messages.
3. **Usage log and dashboard.** Log every call: model, tokens in, tokens out, cost, feature, user, time. Dashboard: today, this month, by feature, by user.
4. **Pricing in GBP and USD.** Prices per 1M tokens and the USD to GBP rate live in settings, never in code. Every cost is shown in both currencies.
5. **Budgets.** Per-user and monthly limits, with a warning bar and an alert before the limit.
6. **Data rules.** Follow the prompt-data classes. Redact personal data before sending. Log prompts only when policy allows.
7. **Testing.** Mock mode and a test for the cost calculation.

Illustrative cost calculation (rates come from settings):

```
usd = (tokens_in * price_in + tokens_out * price_out) / 1,000,000
gbp = usd * usd_to_gbp_rate
```

Proof to gather: settings screen, a usage-log row, dashboard screenshot, cost shown in GBP and USD, a budget alert firing in test, mock mode output, the cost-calculation test.
