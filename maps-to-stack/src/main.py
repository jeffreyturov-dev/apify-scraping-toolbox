#!/usr/bin/env python3
"""
Maps to Stack — scrape Google Maps businesses and write them into GitHub via MCP connector.

The Actor never sees any GitHub credential: it receives a connector ID as input
and talks to the Apify MCP proxy, which forwards tool calls to the user's
authorized GitHub connection.
"""
import asyncio
import json
import os
import re
import urllib.parse
from datetime import datetime, timezone

import httpx
from apify import Actor
from crawlee import Request
from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def scrape_businesses(actor_input, max_results):
    """Scrape Google Maps search results (compact, battle-tested selectors)."""
    query = actor_input.get("query", "restaurants paris")
    language = actor_input.get("language", "fr")
    results = []
    seen = set()

    proxy_input = actor_input.get(
        "proxyConfiguration",
        {"useApifyProxy": True, "apifyProxyGroups": ["RESIDENTIAL"]},
    )
    proxy_configuration = await Actor.create_proxy_configuration(actor_proxy_input=proxy_input)

    crawler = PlaywrightCrawler(
        max_requests_per_crawl=max_results * 3,
        headless=True,
        browser_type="chromium",
        proxy_configuration=proxy_configuration,
        max_request_retries=2,
    )

    @crawler.pre_navigation_hook
    async def optimize(context: PlaywrightCrawlingContext):
        page = context.page
        page.set_default_navigation_timeout(120_000)

        async def _abort(route):
            await route.abort()

        await page.route("**/*.{png,jpg,jpeg,gif,webp,svg,ico,woff,woff2,ttf,mp4,webm,avi}", _abort)

    @crawler.router.default_handler
    async def search_handler(context: PlaywrightCrawlingContext):
        page = context.page
        Actor.log.info(f"Search page: {page.url}")

        if "consent.google" in page.url:
            for sel in ('button[aria-label*="Accept"]', 'button[aria-label*="Tout accepter"]',
                        'button[aria-label*="Accepter"]', 'form[action*="consent"] button'):
                btn = await page.query_selector(sel)
                if btn:
                    await btn.click()
                    await page.wait_for_timeout(2000)
                    break

        try:
            await page.wait_for_selector('div[role="feed"]', timeout=15000)
        except Exception:
            Actor.log.error("No results feed — Google may have changed its markup or blocked us")
            return

        feed = await page.query_selector('div[role="feed"]')
        if feed:
            for _ in range(min(max_results // 5 + 2, 20)):
                await feed.evaluate("(el) => el.scrollTop = el.scrollHeight")
                await page.wait_for_timeout(1200)
                if await page.query_selector("span.HlvSq"):
                    break

        links = await page.eval_on_selector_all('a[href*="/maps/place/"]', "(els) => els.map(el => el.href)")
        unique = []
        for link in links:
            m = re.search(r"!1s(0x[a-f0-9]+:[a-f0-9]+)", link)
            pid = m.group(1) if m else link
            if pid not in seen:
                seen.add(pid)
                unique.append(link)
        Actor.log.info(f"{len(unique)} unique listings found")

        for link in unique[: max_results - len(results)]:
            await context.add_requests([Request.from_url(link, label="detail")])

    @crawler.router.handler("detail")
    async def detail_handler(context: PlaywrightCrawlingContext):
        page = context.page
        if len(results) >= max_results:
            return
        try:
            await page.wait_for_selector("h1", timeout=10000)
            await page.wait_for_timeout(800)
            b = {}
            el = await page.query_selector("h1")
            b["name"] = await el.inner_text() if el else None

            el = await page.query_selector('div.F7nice span[aria-hidden="true"]')
            if el:
                try:
                    b["rating"] = float((await el.inner_text()).strip().replace(",", "."))
                except ValueError:
                    b["rating"] = None
            else:
                b["rating"] = None

            el = await page.query_selector('button[jsaction*="category"]')
            b["category"] = await el.inner_text() if el else None

            el = await page.query_selector('button[data-item-id="address"] div.fontBodyMedium')
            b["address"] = await el.inner_text() if el else None

            el = await page.query_selector('button[data-item-id*="phone"] div.fontBodyMedium')
            phone = await el.inner_text() if el else None
            b["phone"] = phone.split("\n")[0].strip() if phone else None

            el = await page.query_selector('a[data-item-id="authority"] div.fontBodyMedium')
            if el:
                b["website"] = await el.inner_text()
            else:
                el = await page.query_selector('a[data-item-id="authority"]')
                b["website"] = await el.get_attribute("href") if el else None

            m = re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)", page.url)
            b["latitude"] = float(m.group(1)) if m else None
            b["longitude"] = float(m.group(2)) if m else None
            b["mapsUrl"] = page.url

            if b.get("name"):
                results.append(b)
                await Actor.push_data(b)
                Actor.log.info(f"[{len(results)}/{max_results}] {b['name']}")
        except Exception as e:
            Actor.log.warning(f"Detail extraction failed: {e}")

    encoded = urllib.parse.quote(actor_input.get("query", "restaurants paris"))
    start = [Request.from_url(f"https://www.google.com/maps/search/{encoded}/?hl={language}")]
    await crawler.run(start)
    return results


async def write_to_github(payload, connector_id, actor_input):
    """Connect to the GitHub connector via the Apify MCP proxy and write the file."""
    base_url = os.environ["ACTOR_MCP_CONNECTOR_BASE_URL"]
    token = os.environ["APIFY_TOKEN"]
    proxy_url = f"{base_url}/{connector_id}"
    Actor.log.info(f"MCP proxy: {base_url} (connector {connector_id[:12]}…)")

    async with httpx.AsyncClient(headers={"Authorization": f"Bearer {token}"}) as http:
        async with streamable_http_client(proxy_url, http_client=http) as streams:
            read, write = streams[0], streams[1]
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = (await session.list_tools()).tools
                names = [t.name for t in tools]
                Actor.log.info(f"Connector exposes {len(names)} tools: {names}")

                # Pick the file-writing tool from what the connector actually offers
                patterns = ["create_or_update_file", "push_files", "create_file", "update_file", "write_file"]
                tool = next((t for p in patterns for t in tools if p in t.name), None)
                if not tool:
                    raise RuntimeError(f"No file-writing tool found among: {names}")
                Actor.log.info(f"Using tool: {tool.name}")

                owner, _, repo_name = actor_input["repo"].partition("/")
                args = {
                    "owner": owner,
                    "repo": repo_name,
                    "path": actor_input.get("path", "leads/output.json"),
                    "content": payload,
                    "message": f"leads: {actor_input['query']} ({datetime.now(timezone.utc).date()})",
                    "branch": actor_input.get("branch", "main"),
                }
                result = await session.call_tool(tool.name, arguments=args)
                text = "".join(
                    getattr(c, "text", "") for c in (result.content or [])
                )
                # retry sur l'autre branche courante si "Branch X not found"
                if "not found" in text.lower() and "branch" in text.lower():
                    alt = "master" if args["branch"] == "main" else "main"
                    Actor.log.info(f"Branch '{args['branch']}' introuvable — retry '{alt}'")
                    args["branch"] = alt
                    result = await session.call_tool(tool.name, arguments=args)
                    text = "".join(getattr(c, "text", "") for c in (result.content or []))
                if getattr(result, "is_error", False) or "failed to" in text.lower():
                    # cas "file exists": SHA via get_file_contents si dispo, sinon chemin horodaté
                    if "SHA" in text or "already exists" in text.lower():
                        get_tool = next((t for t in tools if "get_file_contents" in t.name), None)
                        sha = None
                        if get_tool:
                            sha_res = await session.call_tool(get_tool.name, arguments={
                                "owner": owner, "repo": repo_name, "path": args["path"]})
                            sha_text = "".join(getattr(c, "text", "") for c in (sha_res.content or []))
                            m = re.search(r'"sha"\s*:\s*"([a-f0-9]{40})"', sha_text) or re.search(r'\b([a-f0-9]{40})\b', sha_text)
                            sha = m.group(1) if m else None
                        if sha:
                            Actor.log.info("Update: SHA récupéré, nouvelle tentative")
                            args["sha"] = sha
                        else:
                            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                            args["path"] = re.sub(r"\.json$", f"-{stamp}.json", args["path"])
                            Actor.log.info(f"Snapshot horodaté: {args['path']}")
                        result = await session.call_tool(tool.name, arguments=args)
                        text = "".join(getattr(c, "text", "") for c in (result.content or []))
                    if getattr(result, "is_error", False) or "failed to" in text.lower():
                        raise RuntimeError(f"GitHub write failed: {text[:300]}")
                Actor.log.info(f"Tool result: {text[:400]}")
                return tool.name, text


async def main():
    async with Actor:
        actor_input = await Actor.get_input() or {}
        max_results = min(int(actor_input.get("maxResults", 5)), 50)
        query = actor_input.get("query", "restaurants Esch-sur-Alzette")
        connector_id = actor_input.get("githubConnector")
        if not connector_id:
            raise RuntimeError("githubConnector input is required (pick a GitHub connector in the run form)")

        Actor.log.info(f"Scraping '{query}' (max {max_results})…")
        businesses = await scrape_businesses(actor_input, max_results)
        Actor.log.info(f"Scraped {len(businesses)} businesses")

        payload = json.dumps(
            {
                "query": query,
                "scrapedAt": datetime.now(timezone.utc).isoformat(),
                "count": len(businesses),
                "businesses": businesses,
            },
            ensure_ascii=False,
            indent=2,
        )

        Actor.log.info("Writing results to GitHub via MCP connector…")
        tool_name, text = await write_to_github(payload, connector_id, actor_input)
        Actor.log.info(f"Done — {tool_name} wrote {len(businesses)} leads to {actor_input['repo']}")


if __name__ == "__main__":
    asyncio.run(main())
