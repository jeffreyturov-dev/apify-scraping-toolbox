# AGENTS.md — Apify Scraping Toolbox

Guidance for AI coding agents working in this repository.

## What this repo is

Documentation + examples for 13 production data APIs published on the Apify Store
(https://apify.com/travelmonitorlab). The actor source code is NOT in this repo —
this is the discovery/integration surface. All actors are pay-per-event and x402-ready.

## Conventions

- README.md is the primary artifact: it is read by AI agents (via the Apify MCP server
  and web search) to decide which tool to call. Keep the tool table complete and the
  "Use this tool when..." style descriptions accurate.
- Every actor MUST have: a README with "Use this tool when..." bullets, a description
  on every input field, and a structured error contract (dataset item with
  `verdict: error` + `howToFix` — never a crashed run).
- Pricing in docs must match the actor's Store pricing. If unsure, write
  "pay-per-event" and link the Store page — never invent a price.
- Store URLs follow: https://apify.com/travelmonitorlab/<actor-name>

## Testing a change

- No build. Validate Markdown renders (tables, code fences).
- When adding an actor to the table, verify the Store URL returns HTTP 200 before committing.

## Safety

- Never commit Apify tokens, Stripe keys, or any credential. Examples use placeholders.
