# Apify Scraping Toolbox — AI-Agent-Ready Data APIs

13 production data & audit APIs — **local business AI-presence audits, Google Maps leads, TikTok, Instagram, YouTube, LinkedIn, web RAG, API change radar, Google review monitoring, French fuel prices, hotel rates and AEO/GEO website checks** — all callable by AI agents (Claude, GPT, Cursor, LangChain, n8n) through the [Apify MCP server](https://mcp.apify.com), or directly via a single HTTP call.

> Pay-per-event pricing. Three tools are **100% free**. All paid tools are **x402-ready**: an agent can pay per call in USDC on Base (HTTP 402 challenge) — no signup, no API key exchange needed.

## The tools

| Tool | What it does | Price | Link |
|---|---|---|---|
| **Local AI Presence Audit** ⭐ NEW | Full local-business audit in one run: Google Business Profile data, recent reviews with urgency classification + owner-response detection, website AI-readiness scan (llms.txt, JSON-LD, robots.txt AI-crawler rules), presence score /100, and **ready-to-use deliverables** (publishable `llms.txt`, prefilled `LocalBusiness` JSON-LD, AI-drafted review responses, prioritized action plan) | $1/run + $0.50/audit | [Store](https://apify.com/travelmonitorlab/local-ai-presence-audit) |
| **AEO & AI Visibility Checker** | 7-criterion Answer Engine Optimization audit of any website (JSON-LD, LocalBusiness schema, llms.txt, robots.txt AI bots, meta, OG, H1) | **FREE** | [Store](https://apify.com/travelmonitorlab/aeo-ai-visibility-checker) |
| **Google Maps Business Scraper** | Names, phones, websites, ratings, reviews, GPS | $0.005/business | [Store](https://apify.com/travelmonitorlab/google-maps-scraper) |
| **Review Radar** | Monitors Google reviews for a business, alerts on new/negative ones | pay-per-event | [Store](https://apify.com/travelmonitorlab/review-radar) |
| **Review Pitch Generator** | Turns a business's review profile into a sales pitch for marketing services | pay-per-event | [Store](https://apify.com/travelmonitorlab/review-pitch-generator) |
| **API Breaking-Change Radar** | Watches API docs/changelogs and flags breaking changes | pay-per-event | [Store](https://apify.com/travelmonitorlab/api-breaking-change-radar) |
| **TikTok Profile & Video Scraper** | Followers, likes, bio, per-video stats | $0.01/profile | [Store](https://apify.com/travelmonitorlab/tiktok-scraper) |
| **Instagram Profile Scraper** | Followers, bio, verified, engagement | $0.01/profile | [Store](https://apify.com/travelmonitorlab/instagram-scraper) |
| **YouTube Video & Channel Scraper** | Views, likes, subscribers, search | $0.002/video | [Store](https://apify.com/travelmonitorlab/youtube-scraper) |
| **LinkedIn Profile Scraper** | Headlines, companies, skills, experience | $0.02/profile | [Store](https://apify.com/travelmonitorlab/linkedin-profile-scraper) |
| **RAG Web Browser** | Clean Markdown from any URL + Google search | $0.003/page | [Store](https://apify.com/travelmonitorlab/rag-web-browser) |
| **Fuel Prices France API** 🇫🇷 | Real-time prices, ~9,800 stations, GPS (official gouv data) | **FREE** | [Store](https://apify.com/travelmonitorlab/hermes-revenu-api) |
| **Hotel Rate Monitoring** | Competitor rates, parity checks | **FREE** | [Store](https://apify.com/travelmonitorlab/travel-monitor-launch) |

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

Then just ask:

- *"Audit the online presence of Boulangerie Paul in Mersch, Luxembourg"* → agent uses **Local AI Presence Audit**
- *"Can ChatGPT see the website adagasolutions.lu?"* → agent uses **AEO & AI Visibility Checker**
- *"Find 50 plumbers in Austin TX with phone numbers"* → agent uses the **Google Maps scraper**
- *"What are current diesel prices in Paris?"* → agent uses the **fuel API**

The agent discovers the tool, reads its README + input schema, and calls it — no glue code.

## Agentic payments (x402)

All paid actors answer an unauthenticated call with a proper **HTTP 402 Payment Required** challenge (x402 v2, USDC on Base, schemes `exact`/`upto`). An x402-aware agent pays per call and retries automatically — machine-to-machine commerce with zero commercial agreement.

## Direct API calls

### Python

```python
import requests

APIFY_TOKEN = "<YOUR_APIFY_TOKEN>"

def audit_business(query, website=None):
    url = ("https://api.apify.com/v2/acts/"
           "travelmonitorlab~local-ai-presence-audit/run-sync-get-dataset-items"
           f"?token={APIFY_TOKEN}")
    payload = {"query": query, "maxReviews": 15, "language": "en"}
    if website:
        payload["websiteUrl"] = website
    r = requests.post(url, json=payload, timeout=600)
    return r.json()

audit = audit_business("Boulangerie Paul Mersch", "https://paul.lu")
print(audit[0]["presenceScore"]["total"], audit[0]["actionPlan"][:2])
```

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
    body: JSON.stringify({ departement }),
  });
  return r.json();
}

const stations = await fuelPrices("75"); // Paris
console.log(stations[0].ville, stations[0].prix_gazole);
```

### curl

```bash
curl -X POST "https://api.apify.com/v2/acts/travelmonitorlab~tiktok-scraper/run-sync-get-dataset-items?token=<TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"profiles": ["khaby.lame"], "maxVideosPerProfile": 5}'
```

## Integrations

All tools work out of the box with **Zapier, Make, n8n, LangChain (`ApifyWrapper`), LlamaIndex** via the Apify integration hub.

## Use cases

- **Local marketing agencies** — audit a prospect's Google profile + website AI-readiness, get the score and ready-made fixes, sell the remediation
- **GEO / AI visibility work** — measure whether ChatGPT, Perplexity and Gemini can "see" a business, then fix the sources they read
- **Lead generation** — live B2B lists with phones/websites for any niche + city
- **Influencer marketing** — creator metrics across TikTok/Instagram/YouTube
- **Recruitment / sales** — LinkedIn profile enrichment at scale
- **RAG pipelines** — clean Markdown extraction for LLM context
- **Travel & mobility apps** — French fuel prices, hotel rate intelligence

## Links

- Store: https://apify.com/travelmonitorlab
- Apify MCP server: https://mcp.apify.com
- Branded MCP facade + API catalog: https://adagasolutions.lu/apis/
- Issues / feature requests: open an issue here or on any actor page

---

*Maintained by [@jeffreyturov-dev](https://github.com/jeffreyturov-dev) / travelmonitorlab.*
