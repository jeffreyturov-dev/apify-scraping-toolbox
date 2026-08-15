# Maps to Stack — Google Maps leads into GitHub via MCP connector

Scrape businesses from Google Maps and write the results **straight into your GitHub repository** — using Apify's [MCP connectors](https://docs.apify.com/integrations/mcp-connectors).

## Why this Actor is different

Your GitHub credentials never touch the Actor code. You authorize a GitHub connector **once** in your Apify account settings; at run time the Actor receives only a connector ID and calls the connector through the Apify MCP proxy. The proxy enforces which tools the Actor may see and call.

## Use this tool when

- You want scraped leads (businesses, contacts, places) to land directly in your stack (a GitHub repo) instead of a dataset you have to export manually
- You are building lead-generation or local-SEO pipelines that should end in version-controlled storage
- You want a working, minimal example of an Actor that uses `resourceType: "mcpConnector"` in its input schema

## Input

| Field | Description |
|---|---|
| `query` | Google Maps search, e.g. `restaurants Esch-sur-Alzette` |
| `maxResults` | How many businesses to scrape (keep small for tests) |
| `githubConnector` | Your authorized GitHub MCP connector (picker in the run form) |
| `repo` | `owner/repo` to write into (must exist) |
| `path` | File path of the JSON file to create/update |
| `proxyConfiguration` | Residential proxy (required — Maps blocks datacenter IPs) |

## Output

- A dataset with one item per business (name, address, phone, website, rating, category, GPS, Maps URL)
- A JSON file committed to your repository at the chosen path

## How it works

1. Playwright scrapes the Maps search results and each place page (consent wall handled, heavy resources blocked).
2. Results are pushed to the dataset.
3. The Actor connects to `${ACTOR_MCP_CONNECTOR_BASE_URL}/<connectorId>` with your `APIFY_TOKEN` as bearer, lists the connector's tools, picks the file-writing tool, and commits the JSON.

AI-agent ready, API + MCP ready.
