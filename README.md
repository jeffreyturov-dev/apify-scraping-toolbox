# Apify Scraping Toolbox — AI-Agent-Ready Data APIs

8 production scraping APIs for **Google Maps, TikTok, Instagram, YouTube, LinkedIn, web RAG, French fuel prices and hotel rates** — all callable by AI agents (Claude, GPT, Cursor, LangChain, n8n) through the [Apify MCP server](https://mcp.apify.com), or directly via a single HTTP call.

> Pay-per-event pricing ($0.002–$0.02 per item). Two tools are **100% free**.

## The tools

| Tool | What it extracts | Price | Link |
|---|---|---|---|
| **Google Maps Business Scraper** | Names, phones, websites, ratings, reviews, GPS | $0.005/business | [Store](https://apify.com/travelmonitorlab/google-maps-scraper) |
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

- *"Find 50 plumbers in Austin TX with phone numbers"* → agent uses the Google Maps scraper
- *"What are current diesel prices in Paris?"* → agent uses the fuel API
- *"Get follower counts for these TikTok creators"* → agent uses the TikTok scraper

The agent discovers the tool, reads its README + input schema, and calls it — no glue code.

## Direct API calls

### Python

```python
import requests

APIFY_TOKEN = "<YOUR_APIFY_TOKEN>"

def scrape_google_maps(queries, max_results=20):
    url = ("https://api.apify.com/v2/acts/"
           "travelmonitorlab~google-maps-scraper/run-sync-get-dataset-items"
           f"?token={APIFY_TOKEN}")
    r = requests.post(url, json={"queries": queries, "maxResults": max_results,
                                 "language": "en", "includeReviews": False}, timeout=600)
    return r.json()

leads = scrape_google_maps(["dentists Austin TX"], max_results=50)
for b in leads:
    print(b["name"], b.get("phone"), b.get("website"), b.get("rating"))
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

- **Lead generation** — live B2B lists with phones/websites for any niche + city
- **Influencer marketing** — creator metrics across TikTok/Instagram/YouTube
- **Recruitment / sales** — LinkedIn profile enrichment at scale
- **RAG pipelines** — clean Markdown extraction for LLM context
- **Travel & mobility apps** — French fuel prices, hotel rate intelligence

## Links

- Store: https://apify.com/travelmonitorlab
- Apify MCP server: https://mcp.apify.com
- Issues / feature requests: open an issue here or on any actor page

---

*Maintained by [@jeffreyturov-dev](https://github.com/jeffreyturov-dev) / travelmonitorlab.*
