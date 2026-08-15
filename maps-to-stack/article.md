# From scraper to stack: pushing Google Maps leads straight into GitHub with MCP connectors

Every lead-generation pipeline I build ends the same way: a dataset full of freshly scraped businesses… that I then have to export, transform, and commit somewhere by hand. The scrape is automated; the last mile never is.

When Apify launched [MCP connectors](https://docs.apify.com/integrations/mcp-connectors) — a new kind of Actor input that lets Actors securely call third-party services like GitHub, Notion, or Slack during a run — I rebuilt that last mile. This article walks through a working Actor that scrapes businesses from Google Maps and commits the results straight into a GitHub repository, **without the Actor code ever seeing a credential**.

Everything below comes from a real build: the pitfalls are ones I actually hit, and the fixes are what actually solved them.

## What we're building

**Maps to Stack**: an Actor that

1. takes a Google Maps search query (e.g. `restaurants Esch-sur-Alzette`),
2. scrapes each place page with Playwright (name, address, phone, website, rating, GPS),
3. pushes the results to the dataset, and
4. **writes a JSON snapshot into your GitHub repo via an MCP connector** — one commit per run, versioned by Git.

Why GitHub as the destination? Because for lead-gen pipelines, a repo is a free CRM: versioned, diffable, and already wired into everything else (CI, dashboards, git-based CMSs). The same pattern works identically for Notion or Slack — only the connector changes.

## The security model that makes this interesting

The classic way to do this is to pass a GitHub token as an Actor input. That means every run log, every shared input JSON, and every fork of your Actor is one leak away from a compromised token.

MCP connectors invert this:

- You authorize GitHub **once** in Apify Console → Settings → Integrations. The credential lives with the connector, not with your code.
- At run time, the Actor receives a **connector ID** (a string like `ebw4ThD4cQbEKzC2l`) — not a token.
- The Actor talks to the **Apify MCP proxy** at `${ACTOR_MCP_CONNECTOR_BASE_URL}/<connectorId>`, authenticating with the run's own `APIFY_TOKEN`.
- The proxy enforces the tool permissions your Actor declared in its input schema. The Actor physically cannot call tools outside its declaration.

## Declaring the connector input

In `.actor/INPUT_SCHEMA.json`, set `resourceType: "mcpConnector"`. The `mcpServers` rule list both filters which connectors the picker offers and caps which tools the proxy will let the Actor call:

```json
"githubConnector": {
  "title": "GitHub connector",
  "description": "MCP connector to your GitHub account. The Actor only sees a connector ID.",
  "type": "string",
  "resourceType": "mcpConnector",
  "mcpServers": [
    {
      "url": "*",
      "tools": {
        "required": ["create_*", "push_*", "update_*", "write_*", "commit_*", "get_*"],
        "readOnly": false
      }
    }
  ]
}
```

At run time the input value is just the connector ID string.

> **Verified in the run log:** the proxy filtered the connector's tool list down to exactly what matched my declaration. My run saw 7 tools — `create_branch`, `create_or_update_file`, `create_pull_request`, `create_repository`, `push_files`, `update_pull_request`, `update_pull_request_branch` — and nothing else. The constraint layer works.

## Connecting from the Actor (Python)

Two environment variables are injected into every run: `ACTOR_MCP_CONNECTOR_BASE_URL` (the proxy) and `APIFY_TOKEN` (the starter's token). You use the standard MCP Python SDK — nothing Apify-specific:

```python
import os
import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

base_url = os.environ["ACTOR_MCP_CONNECTOR_BASE_URL"]
token = os.environ["APIFY_TOKEN"]
proxy_url = f"{base_url}/{connector_id}"

async with httpx.AsyncClient(
    headers={"Authorization": f"Bearer {token}"}
) as http:
    async with streamable_http_client(proxy_url, http_client=http) as streams:
        read, write = streams[0], streams[1]
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = (await session.list_tools()).tools
```

**Pitfall #1 — SDK drift.** The docs unpack `streamable_http_client` into three values (`read, write, _`), but the `mcp` version my image installed yields **two**. `ValueError: not enough values to unpack (expected 3, got 2)`. Indexing the tuple (`streams[0], streams[1]`) works across versions. Same story for the result object: the error flag is `result.is_error` (snake_case), not `isError` — the docs' TypeScript casing leaks into expectations.

## Writing the file — and surviving reality

With the session up, pick the file-writing tool from whatever the connector actually exposes (don't hard-code — the tool list is filtered by your schema *and* by what the server advertised at authorization time):

```python
patterns = ["create_or_update_file", "push_files", "create_file", "update_file", "write_file"]
tool = next((t for p in patterns for t in tools if p in t.name), None)

owner, _, repo_name = actor_input["repo"].partition("/")
args = {
    "owner": owner,
    "repo": repo_name,
    "path": actor_input.get("path", "leads/output.json"),
    "content": payload_json,
    "message": f"leads: {query} ({date.today()})",
    "branch": actor_input.get("branch", "main"),
}
result = await session.call_tool(tool.name, arguments=args)
```

Two failures hit me immediately in real runs — both easy to fix once you see them:

**Pitfall #2 — `Branch main not found`.** My repo's default branch is `master`, not `main`. The MCP tool doesn't fall back to the repo's default; it fails loudly. Cheap robust fix: detect the failure and retry once with the other common branch name.

**Pitfall #3 — `File already exists… provide the current file's SHA`.** The second run collided with the first run's file. The GitHub API wants the blob SHA for updates — but the connector I authorized only exposes write tools (no `get_file_contents` to fetch the SHA). Instead of fighting it, I leaned into a better pattern for pipelines: **immutable, timestamped snapshots**. Every run writes a new dated file; Git itself becomes the history. If a read tool *is* available, the code uses the SHA path instead:

```python
text = "".join(getattr(c, "text", "") for c in (result.content or []))
if "already exists" in text.lower():
    get_tool = next((t for t in tools if "get_file_contents" in t.name), None)
    if get_tool:
        ...  # fetch sha, retry with args["sha"] = sha
    else:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        args["path"] = re.sub(r"\.json$", f"-{stamp}.json", args["path"])
    result = await session.call_tool(tool.name, arguments=args)
```

Worth knowing: **the connector's tool set is fixed at authorization time** ("Layer 1" in the docs). If you authorize a connector and later wish it exposed more tools, re-authorize it — the discovered set doesn't refresh on its own.

## The scraping side, briefly

The Maps half of the Actor uses Crawlee's `PlaywrightCrawler` with a residential proxy (Google blocks datacenter IPs outright). Three details that make it reliable, all learned the hard way on earlier Actors:

- **Kill the consent wall first.** `consent.google.com` intercepts the first navigation; click "Accept" before waiting for any results selector.
- **Block heavy resources in a pre-navigation hook.** The `load` event never fires on Maps (continuous analytics), so route-abort images/fonts/media, or every navigation times out.
- **Don't trust a green run.** A `SUCCEEDED` run can still hold zero useful items — always assert on dataset item count and log per-item progress.

The full scraper is ~150 lines; the dataset holds one item per business with name, category, address, phone, website, rating, coordinates, and the Maps URL.

## What a real run looks like

Input:

```json
{
  "query": "restaurants Esch-sur-Alzette",
  "maxResults": 3,
  "githubConnector": "ebw4ThD4cQbEKzC2l",
  "repo": "jeffreyturov-dev/apify-scraping-toolbox",
  "path": "leads/esch-restaurants.json"
}
```

Run log (abridged):

```
Scraped 3 businesses
Connector exposes 7 tools: ['create_branch', 'create_or_update_file', ...]
Using tool: create_or_update_file
Branch 'main' introuvable — retry 'master'
Snapshot horodaté: leads/esch-restaurants-20260814T193046Z.json
Done — create_or_update_file wrote 3 leads
```

And the commit lands in GitHub with the full JSON: 3 businesses, ratings, phone numbers, coordinates — queryable, diffable, and already where the rest of my tooling lives.

## Where this pattern earns its keep

- **Lead-gen pipelines**: scrape on a schedule, each run commits a dated snapshot; a git log *is* your change history of who opened/closed in a neighborhood.
- **Any-to-any delivery**: swap the connector for Notion (a database row per business) or Slack (a summary message) — the Actor code changes by a dozen lines; the security model stays identical.
- **Untrusted Actor code**: if you consume third-party Actors, connectors are the only sane way to give them access to *your* services — the schema's tool constraints and the proxy's enforcement mean a malicious or sloppy Actor can't exceed its brief.

## Try it

The Actor source (schema, scraper, connector logic) is intentionally small — read it top to bottom in five minutes. The moving parts that matter:

1. `resourceType: "mcpConnector"` in the input schema, with `mcpServers` tool constraints.
2. `${ACTOR_MCP_CONNECTOR_BASE_URL}/<connectorId>` + `APIFY_TOKEN` bearer, via the stock MCP SDK.
3. Defensive write logic: branch fallback, SHA-if-available, timestamped snapshot otherwise.

The connector model removes the part of pipeline building I liked least — sprinkling credentials through code — and replaces it with one authorization, one ID, and a proxy that keeps everyone honest.
