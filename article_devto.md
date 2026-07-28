# I built 8 pay-per-use scraping APIs that AI agents can call directly (Google Maps, TikTok, Instagram, YouTube, LinkedIn) — here's what I learned

**Tags:** apify, webscraping, mcp, ai, leadgeneration

---

A few weeks ago I published a set of Actors on Apify Store. Today they're all **AI-agent ready**: any LLM agent (Claude, GPT, Cursor, LangChain, n8n) can discover and call them through the Apify MCP server — no custom integration code needed.

This post is the full playbook: what the tools do, how the pay-per-event monetization works, the bugs I hit, and how AI agents actually consume them.

## The toolbox

| Actor | What it extracts | Price (pay-per-event) |
|---|---|---|
| [Google Maps Business Scraper](https://apify.com/travelmonitorlab/google-maps-scraper) | Names, phones, websites, ratings, reviews, GPS | $0.005 / business |
| [TikTok Profile & Video Scraper](https://apify.com/travelmonitorlab/tiktok-scraper) | Followers, likes, bio, per-video stats | $0.01 / profile |
| [Instagram Profile Scraper](https://apify.com/travelmonitorlab/instagram-scraper) | Followers, bio, verified, engagement | $0.01 / profile |
| [YouTube Video & Channel Scraper](https://apify.com/travelmonitorlab/youtube-scraper) | Views, likes, subscribers, search results | $0.002 / video |
| [LinkedIn Profile Scraper](https://apify.com/travelmonitorlab/linkedin-profile-scraper) | Headlines, companies, skills, experience | $0.02 / profile |
| [RAG Web Browser](https://apify.com/travelmonitorlab/rag-web-browser) | Clean Markdown from any URL + Google search | $0.003 / page |
| [Fuel Prices France API](https://apify.com/travelmonitorlab/hermes-revenu-api) | Real-time prices, 9,800 stations, GPS | **FREE** |
| [Hotel Rate Monitoring](https://apify.com/travelmonitorlab/travel-monitor-launch) | Competitor rates, parity checks | **FREE** |

The two free ones are deliberate lead magnets — more on that below.

## Why "AI-agent ready" changes everything

The old model: a human finds your scraper on the store, reads the docs, clicks buttons.

The new model: an AI agent gets a task ("find me 50 plumbers in Austin with their phone numbers"), searches the Apify Store via MCP, reads the actor's README and input schema, and calls it — end to end, no human.

For that to work, three things must be true:

1. **Your README is written for an LLM, not just humans.** Mine now all start with a "Use this tool when..." section — that's what the agent pattern-matches against the user's request.
2. **Your input schema has a description on every field.** The agent constructs the JSON input from those descriptions. No description = hallucinated parameters = failed runs = no revenue.
3. **Your output is documented field by field.** The agent needs to know what it gets back to reason over it.

Here's the actual flow with the Apify MCP server (`https://mcp.apify.com` — add it to Claude Desktop or Cursor in 30 seconds):

```
User: "Get me the follower counts of these 5 TikTok creators"
Agent: → search-actors("tiktok profile")
       → fetch-actor-details (reads README + input schema)
       → call-actor(travelmonitorlab/tiktok-scraper,
                    {"profiles": [...], "maxVideosPerProfile": 0})
       → returns structured JSON
```

Or skip MCP entirely — every actor is a single synchronous HTTP call:

```bash
curl -X POST "https://api.apify.com/v2/acts/travelmonitorlab~google-maps-scraper/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"queries": ["plumbers Austin TX"], "maxResults": 50}'
```

## Monetization: pay-per-event (and the trap that cost me hours)

Apify offers several pricing models. For new actors, `PRICE_PER_DATASET_ITEM` is **rejected** — you must use `PAY_PER_EVENT`. The model is better anyway: you define events (e.g. `business-scraped` at $0.005) and charge explicitly in code:

```python
await Actor.charge(event_name="business-scraped")
await Actor.push_data(item)
```

**The trap:** put the charge AFTER `crawler.run()` and your event loop may already be closed — the charge silently vanishes, you deliver data for free. Charge inside the handler, right before pushing data. Always verify with `chargedEventCounts` in the run object after a test run.

Setting pricing is pure API:

```python
PUT /v2/acts/{actorId}
{"pricingInfos": [{
  "pricingModel": "PAY_PER_EVENT",
  "reasonForChange": "Launch pricing",
  "pricingPerEvent": {"actorChargeEvents": {
    "business-scraped": {
      "eventTitle": "Business scraped",
      "eventDescription": "One Google Maps business record",
      "eventPriceUsd": 0.005
    }}}}
]}
```

Apify takes 20%. Compute is paid by the user; you pocket the event fees.

## Battle scars (so you don't get them)

- **Crawlee 1.8 breaking changes:** `purge_on_start` and `navigation_timeout_secs` are no longer valid kwargs — use `page.set_default_navigation_timeout()` in a `pre_navigation_hook`.
- **Google Maps never fires `load`:** analytics keep streaming forever, so navigation always times out. Fix: abort images/fonts/media via `page.route()` (the handler must be a coroutine, not a lambda).
- **Residential proxies are mandatory for Google Maps**, and you must pass `actor_proxy_input=` as a *named* argument to `Actor.create_proxy_configuration()`.
- **French number formats will crash your floats:** `"4,8"` → replace comma; `"1 234"` reviews can use `\xa0` *or* `\u202f` as thousand separator.
- **A "SUCCEEDED" run can contain zero useful data.** Always check `itemCount` + sample the dataset + read the end of the log.
- **Don't run 7 queries × 25 results in one run.** Split into parallel runs of ≤5 queries × 15 results; retry failed ones sequentially (residential proxy tunnels occasionally die).

## The distribution strategy

Publishing on the store is step 0. What actually moves the needle:

1. **Free lead magnets** — the fuel-price and hotel-rate actors are 100% free. Free tools get users, ratings, and store ranking; ranked actors surface in MCP search results; MCP visibility drives paying users to the paid actors.
2. **README written for LLMs** — agents choose tools whose docs they can parse. Clear "use when", typed inputs, example I/O.
3. **Niche SEO titles** — "Google Maps Scraper" is saturated; "Fuel Prices France API" has zero competition on the store.
4. **Dogfooding** — I use my own Google Maps actor to build lead lists I sell elsewhere. Every sale is also a demo.

## Try them

All 8 actors are live on [Apify Store](https://apify.com/travelmonitorlab). If you build agents, add `https://mcp.apify.com` to your MCP client and just ask for the data — the agent will find the tools.

Feedback, bugs, feature requests: open an issue on any actor page, I answer fast.
