# Apify Scraping Toolbox — AI-Agent-Ready Data APIs

15 production data, monitoring and audit APIs — **Google Maps leads, social profiles, web RAG, API change monitoring, Google reviews, local AI presence, brand mentions and citations, French fuel prices, hotel rates and AEO checks** — callable by AI agents through the [Apify MCP server](https://mcp.apify.com), or directly via one HTTP call.

> All 15 Actors use pay-per-event pricing; none is currently marketed as free. Where `dryRun` is supported, it skips Actor event charges but not necessarily compute, browser, proxy or external-provider usage. All paid Actors are x402-ready for eligible agentic payments in USDC on Base.

Browse the [public example toolbox](https://adagasolutions.lu/toolbox/) or the [15 detailed API pages](https://adagasolutions.lu/apis/) with real inputs, output excerpts, run IDs, durations and measured platform usage.

## The tools

Prices below are the current FREE-tier event prices verified through the Apify API on 8 November 2026. Subscription-tier discounts may apply on Apify.

| Tool | Use this tool when… | Current price | Proof and links |
|---|---|---|---|
| **Local AI Presence Audit** | You need a one-business Google profile, review and website AI-readiness audit with a score and prioritized deliverables | $1/run + $0.50/business | [Proof](https://adagasolutions.lu/apis/local-ai-presence-audit.html) · [Store](https://apify.com/travelmonitorlab/local-ai-presence-audit) |
| **Local AI Presence Monitor** | You need a persistent baseline and alerts for new reviews, rating changes or website AI-readiness regressions | $0.25/run + $0.25/business + $0.10/competitor + $0.10/alert | [Proof](https://adagasolutions.lu/apis/local-ai-presence-monitor.html) · [Store](https://apify.com/travelmonitorlab/local-ai-presence-monitor) |
| **AI Brand Visibility Tracker** | You need to measure exact brand mentions and official-domain citations in real answers from a selected AI model | $0.05/run + $0.05/answer + $0.10/official citation | [Proof](https://adagasolutions.lu/apis/ai-brand-visibility-tracker.html) · [Store](https://apify.com/travelmonitorlab/ai-brand-visibility-tracker) |
| **AEO & AI Visibility Checker** | You need seven technical website AI-readiness checks and a starter `llms.txt`; this does not prove AI citations | $0.01/run + $0.05/audit | [Proof](https://adagasolutions.lu/apis/aeo-ai-visibility-checker.html) · [Store](https://apify.com/travelmonitorlab/aeo-ai-visibility-checker) |
| **Google Maps Business Scraper** | You need names, phones, websites, addresses, categories, ratings, reviews or GPS coordinates for a niche and city | $1/run + $0.03/business | [Proof](https://adagasolutions.lu/apis/google-maps-scraper.html) · [Store](https://apify.com/travelmonitorlab/google-maps-scraper) |
| **Review Radar** | You need Google review monitoring, urgency classification and optional Slack alerts | $0.25/run + $0.01/new review + $0.05/Slack alert | [Proof](https://adagasolutions.lu/apis/review-radar.html) · [Store](https://apify.com/travelmonitorlab/review-radar) |
| **Review Pitch Generator** | You need a review-based audit and personalized outreach draft for a prospect | $0.25/run + $0.10/pitch + $0.05/payload sent | [Proof](https://adagasolutions.lu/apis/review-pitch-generator.html) · [Store](https://apify.com/travelmonitorlab/review-pitch-generator) |
| **API Breaking-Change Radar** | You need OpenAPI baselines, diffs, release classification and critical-change alerts | $0.50/run + $0.005/API + $0.50/breaking change + $1/critical alert | [Proof](https://adagasolutions.lu/apis/api-breaking-change-radar.html) · [Store](https://apify.com/travelmonitorlab/api-breaking-change-radar) |
| **TikTok Profile & Video Scraper** | You need public creator profiles and video metadata | $0.01/profile + $0.002/video | [Proof](https://adagasolutions.lu/apis/tiktok-scraper.html) · [Store](https://apify.com/travelmonitorlab/tiktok-scraper) |
| **Instagram Profile Scraper** | You need public profile, follower, bio and engagement data | $0.01/profile | [Proof](https://adagasolutions.lu/apis/instagram-scraper.html) · [Store](https://apify.com/travelmonitorlab/instagram-scraper) |
| **YouTube Video & Channel Scraper** | You need structured video and channel metadata | $0.002/video | [Proof](https://adagasolutions.lu/apis/youtube-scraper.html) · [Store](https://apify.com/travelmonitorlab/youtube-scraper) |
| **LinkedIn Profile Scraper** | You need public profile headlines, companies, skills and experience for B2B enrichment | $0.02/profile | [Proof](https://adagasolutions.lu/apis/linkedin-profile-scraper.html) · [Store](https://apify.com/travelmonitorlab/linkedin-profile-scraper) |
| **RAG Web Browser** | You need clean Markdown and metadata from public pages for agents or retrieval pipelines | $0.003/page | [Proof](https://adagasolutions.lu/apis/rag-web-browser.html) · [Store](https://apify.com/travelmonitorlab/rag-web-browser) |
| **Fuel Prices France API** 🇫🇷 | You need official French fuel prices by department, station and fuel type | $0.20/run + $0.01/batch of 1,000 stations | [Proof](https://adagasolutions.lu/apis/hermes-revenu-api.html) · [Store](https://apify.com/travelmonitorlab/hermes-revenu-api) |
| **Hotel Rate Monitoring** | You need competitor hotel rates and parity data in structured datasets | $0.00005/run + $0.00001/item | [Proof](https://adagasolutions.lu/apis/travel-monitor-launch.html) · [Store](https://apify.com/travelmonitorlab/travel-monitor-launch) |

Google Maps uses a datacenter proxy by default to control cost; residential proxy is opt-in when needed. Proxy and platform usage are separate from Actor events.

## 28 ready-to-run public tasks

Each link opens a published Apify task with prefilled input. Technical dry-runs are identified as such; they must not be confused with a real commercial or AI-visibility result.

| Use case | Public example |
|---|---|
| Monitor hotel rates | [Hotel rate standby](https://apify.com/travelmonitorlab/travel-monitor-launch/examples/travel-api-standby) |
| Check French diesel prices | [Prices by department](https://apify.com/travelmonitorlab/hermes-revenu-api/examples/french-diesel-prices-by-department) |
| Find a restaurant lead | [Google Maps restaurant lead](https://apify.com/travelmonitorlab/google-maps-scraper/examples/google-maps-restaurant-lead-luxembourg) |
| Export a TikTok profile | [Public TikTok profile](https://apify.com/travelmonitorlab/tiktok-scraper/examples/public-tiktok-profile-latest-video) |
| Export a LinkedIn profile | [Public LinkedIn profile JSON](https://apify.com/travelmonitorlab/linkedin-profile-scraper/examples/public-linkedin-profile-json) |
| Convert a page for RAG | [Web page to Markdown](https://apify.com/travelmonitorlab/rag-web-browser/examples/web-search-to-markdown-for-ai) |
| Export an Instagram profile | [Public Instagram profile JSON](https://apify.com/travelmonitorlab/instagram-scraper/examples/public-instagram-profile-json) |
| Extract YouTube metadata | [Video metadata JSON](https://apify.com/travelmonitorlab/youtube-scraper/examples/youtube-video-metadata-json) |
| Create an OpenAPI baseline | [API breaking-change monitor](https://apify.com/travelmonitorlab/api-breaking-change-radar/examples/openapi-breaking-change-monitor) |
| Monitor Google reviews | [Luxembourg review monitoring](https://apify.com/travelmonitorlab/review-radar/examples/monitor-google-reviews-luxembourg) |
| Prioritize urgent reviews | [Restaurant review triage](https://apify.com/travelmonitorlab/review-radar/examples/triage-urgent-restaurant-reviews) |
| Generate a review-based report | [Restaurant review report](https://apify.com/travelmonitorlab/review-pitch-generator/examples/generate-restaurant-review-report) |
| Prepare a hotel sales call | [Hotel review sales audit](https://apify.com/travelmonitorlab/review-pitch-generator/examples/prepare-hotel-review-sales-audit) |
| Audit website AI readiness | [Seven-check AEO audit](https://apify.com/travelmonitorlab/aeo-ai-visibility-checker/examples/website-ai-crawler-readiness-audit) |
| Audit one local business | [Local presence audit](https://apify.com/travelmonitorlab/local-ai-presence-audit/examples/restaurant-reviews-ai-presence-audit) |
| Monitor website AI readiness | [Website change monitor](https://apify.com/travelmonitorlab/local-ai-presence-monitor/examples/website-ai-readiness-change-monitor) |
| Monitor restaurant reputation | [Review and AI-readiness changes](https://apify.com/travelmonitorlab/local-ai-presence-monitor/examples/restaurant-reputation-ai-change-monitor) |
| Compare a local competitor | [Restaurant competitor benchmark](https://apify.com/travelmonitorlab/local-ai-presence-monitor/examples/restaurant-competitor-benchmark) |
| Test the Brand Tracker integration | [Technical dry-run preview](https://apify.com/travelmonitorlab/ai-brand-visibility-tracker/examples/preview-ai-brand-visibility-measurement) |
| Measure hotel-domain citations | [Yasha Hotel AI citations](https://apify.com/travelmonitorlab/ai-brand-visibility-tracker/examples/yasha-hotel-official-domain-ai-citations) |
| Compare three Luxembourg hotels | [Three-hotel AI-presence comparison](https://apify.com/travelmonitorlab/local-ai-presence-monitor/examples/three-luxembourg-hotels-ai-presence-comparison) |
| Triage Luxembourg City restaurant reviews | [Luxembourg City review triage](https://apify.com/travelmonitorlab/review-radar/examples/luxembourg-city-restaurant-review-triage) |
| Build a small Lyon lead list | [Three real Lyon restaurants](https://apify.com/travelmonitorlab/google-maps-scraper/examples/lyon-restaurant-lead-list-small) |
| Monitor Stripe OpenAPI changes | [Stripe breaking-change watch](https://apify.com/travelmonitorlab/api-breaking-change-radar/examples/stripe-openapi-breaking-change-watch) |
| Compare diesel in Rhône and Paris | [Departments 69 and 75](https://apify.com/travelmonitorlab/hermes-revenu-api/examples/compare-diesel-prices-rhone-paris) |
| Audit a Luxembourg hairdresser | [Bubbles Coiffure local presence audit](https://apify.com/travelmonitorlab/local-ai-presence-audit/examples/bubbles-coiffure-local-ai-presence-audit) |
| Compare two Esch-sur-Alzette restaurants | [Local restaurant comparison](https://apify.com/travelmonitorlab/local-ai-presence-monitor/examples/restaurant-esch-local-competitor-comparison) |
| Measure three fixed-model AI queries | [Yasha fixed-model Brand Tracker](https://apify.com/travelmonitorlab/ai-brand-visibility-tracker/examples/yasha-fixed-model-multi-query-brand-tracker) |

For a real Brand Tracker result, see run `FC19rOVtCldS03ASm`: one selected OpenRouter model answered a query about Adaga solutions in 4.48 seconds. The output recorded `mentioned: true`, `cited: false`, and one model-provided citation. This is evidence for one model, prompt and date—not universal AI visibility. The public task above remains a technical dry-run and makes no visibility claim.

New acceptance proofs include run `ewhxiMDy3NcDAX2Y7` for three real Lyon businesses, run `63iU7PabbEbQLw0vD` for 226 official fuel-station records limited to departments 69 and 75, and run `rTzuzBVg0h45cFz3L` for three out of three Yasha Hotel answers measured with the fixed model `recursive/flint-v1.0:free`. Public Brand tasks use technical dry-run without a provider key; their linked real runs preserve the AI-answer evidence.

## Use with AI agents (MCP)

Add the Apify MCP server to your client:

```json
// Claude Desktop / Cursor — mcp.json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com",
      "headers": { "Authorization": "Bearer <YOUR_APIFY_TOKEN>" }
    }
  }
}
```

Then ask:

- *"Audit the online presence of Boulangerie Paul in Mersch, Luxembourg"* → **Local AI Presence Audit**
- *"Measure whether this selected model mentions my hotel and cites its official domain"* → **AI Brand Visibility Tracker**
- *"Find 50 plumbers in Austin TX with phone numbers"* → **Google Maps Business Scraper**
- *"What are current diesel prices in Paris?"* → **Fuel Prices France API**

The agent discovers the tool, reads its README and input schema, and calls it. Start with a public task or the smallest useful input, then inspect the dataset before scheduling recurring runs.

## Agentic payments (x402)

Paid Actors answer eligible unauthenticated calls with an **HTTP 402 Payment Required** challenge (x402 v2, USDC on Base, schemes `exact`/`upto`). An x402-aware agent can pay per call and retry automatically. Provider, proxy and compute costs remain separate where applicable.

## Direct API calls

### Python

```python
import requests

APIFY_TOKEN = "<YOUR_APIFY_TOKEN>"

def audit_business(query, website=None):
    url = ("https://api.apify.com/v2/acts/"
           "travelmonitorlab~local-ai-presence-audit/run-sync-get-dataset-items"
           f"?token={APIFY_TOKEN}")
    payload = {"query": query, "maxReviews": 15, "language": "en", "dryRun": True}
    if website:
        payload["websiteUrl"] = website
    r = requests.post(url, json=payload, timeout=600)
    r.raise_for_status()
    return r.json()

audit = audit_business("Boulangerie Paul Mersch", "https://paul.lu")
print(audit[0]["presenceScore"]["total"], audit[0]["actionPlan"][:2])
```

This example uses `dryRun: True` for integration testing. Remove it only when you intend to enable billed Actor events and alerts.

### Node.js

```javascript
const APIFY_TOKEN = "<YOUR_APIFY_TOKEN>";

async function fuelPrices(departement) {
  const url = "https://api.apify.com/v2/acts/" +
    "travelmonitorlab~hermes-revenu-api/run-sync-get-dataset-items" +
    `?token=${APIFY_TOKEN}`;
  const r = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ departement, dryRun: true }),
  });
  if (!r.ok) throw new Error(`Apify HTTP ${r.status}`);
  return r.json();
}

const stations = await fuelPrices("75");
console.log(stations[0].ville, stations[0].prix_gazole);
```

### curl

```bash
curl -X POST "https://api.apify.com/v2/acts/travelmonitorlab~tiktok-scraper/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"profiles": ["khaby.lame"], "maxVideosPerProfile": 1}'
```

This TikTok call performs a real extraction and can charge Actor events; this Actor has no `dryRun` input.

## Integrations

The tools work with **Zapier, Make, n8n, LangChain and LlamaIndex** through Apify integrations, and with MCP-compatible agents through the Apify MCP server.

## Use cases

- **Local marketing agencies** — audit a prospect's Google profile and website readiness, then sell the remediation
- **Brand and GEO measurement** — keep model-specific answer evidence, official-domain citations and historical deltas
- **Lead generation** — live B2B lists with phones and websites for any niche and city
- **Reputation operations** — detect new reviews, classify urgency and monitor changes over time
- **Influencer marketing** — creator metrics across TikTok, Instagram and YouTube
- **Recruitment and sales** — public LinkedIn profile enrichment
- **RAG pipelines** — clean Markdown extraction for LLM context
- **Travel and mobility apps** — French fuel prices and hotel rate intelligence

## Links

- Apify Store: https://apify.com/travelmonitorlab
- Public examples and recorded-run demos: https://adagasolutions.lu/toolbox/
- Detailed inputs, outputs, costs and proofs: https://adagasolutions.lu/apis/
- Apify MCP server: https://mcp.apify.com
- Issues and feature requests: open an issue here or on an Actor page

After a successful real run, an honest Store review helps other users evaluate the Actor. Critical feedback is welcome; share a run ID and expected result, never credentials.

---

*Maintained by [@jeffreyturov-dev](https://github.com/jeffreyturov-dev) / [Adaga solutions](https://adagasolutions.lu), Luxembourg.*
