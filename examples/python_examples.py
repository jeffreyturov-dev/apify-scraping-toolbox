"""Examples: call every toolbox actor with one function each."""
import requests

APIFY_TOKEN = "<YOUR_APIFY_TOKEN>"
BASE = "https://api.apify.com/v2/acts/travelmonitorlab~{slug}/run-sync-get-dataset-items"


def run(slug: str, payload: dict, timeout: int = 600) -> list:
    """Run any toolbox actor synchronously and return dataset items."""
    r = requests.post(f"{BASE.format(slug=slug)}?token={APIFY_TOKEN}",
                      json=payload, timeout=timeout)
    r.raise_for_status()
    return r.json()


# --- Lead generation -------------------------------------------------------
def google_maps(queries, max_results=20, language="en"):
    return run("google-maps-scraper", {
        "queries": queries, "maxResults": max_results,
        "language": language, "includeReviews": False})


# --- Social ----------------------------------------------------------------
def tiktok_profiles(usernames, max_videos=5):
    return run("tiktok-scraper", {"profiles": usernames,
                                  "maxVideosPerProfile": max_videos})


def instagram_profiles(usernames):
    return run("instagram-scraper", {"profiles": usernames})


def youtube_search(query, max_results=10):
    return run("youtube-scraper", {"searchQueries": [query],
                                   "maxResults": max_results})


def linkedin_profiles(profile_urls, skills=True, experience=True):
    return run("linkedin-profile-scraper", {
        "profileUrls": profile_urls,
        "includeSkills": skills, "includeExperience": experience})


# --- RAG / web -------------------------------------------------------------
def web_to_markdown(query=None, urls=None, max_results=5):
    payload = {"maxResults": max_results, "outputFormat": "markdown"}
    if query:
        payload["query"] = query
    if urls:
        payload["urls"] = urls
    return run("rag-web-browser", payload)


# --- Free tools ------------------------------------------------------------
def fuel_prices_france(departement=None, carburant=None):
    payload = {}
    if departement:
        payload["departement"] = departement
    if carburant:
        payload["carburant"] = carburant
    return run("hermes-revenu-api", payload)


if __name__ == "__main__":
    # Cheapest sanity check: the FREE fuel API (1 department)
    stations = fuel_prices_france(departement="75", carburant="gazole")
    print(f"{len(stations)} stations in Paris")
    for s in stations[:5]:
        print(f"  {s['ville']} | {s['adresse']} | gazole: {s.get('prix_gazole')} €")
