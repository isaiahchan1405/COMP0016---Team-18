import requests   # lets Python make web requests (like curl, but in code)
import json       # converts between JSON text and Python objects
import time       # used to pause between requests

# The first page to fetch:
#   limit=50  -> give me 50 records per page
#   offset=0    -> start from the very first record
url = "https://goadmin.ifrc.org/api/v2/ops-learning/?limit=50&offset=0"

# Running count of how many records we've saved so far
total = 0

# Open the output file once and keep writing to it as each page arrives.
# encoding="utf-8" keeps non-English characters (e.g. French, Arabic) intact.
with open("ops_learning.jsonl", "w", encoding="utf-8") as out:

    # Keep looping as long as there's another page to fetch.
    # When we reach the last page, url becomes None and the loop stops.
    while url:

        # Ask the server for this page. Wait up to 120 seconds for a reply.
        r = requests.get(url, timeout=120)

        # If the server returned an error (e.g. 502 Bad Gateway), stop here
        # with a clear error message instead of carrying on with bad data.
        r.raise_for_status()

        # Turn the response text into a Python dictionary.
        # Each page looks roughly like this:
        #   {
        #     "count": 20054,               <- total records across ALL pages
        #     "next": "https://...offset=50",  <- link to the next page
        #     "results": [ {...}, {...}, ... ]   <- the 50 records on this page
        #   }
        data = r.json()

        # Write each record on its own line in the file (the "JSON Lines" format).
        # This means we never hold the whole 600 MB in memory at once:
        # only one page (~30 MB) at a time.
        for rec in data["results"]:
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")

        # Update and print progress, e.g. "3000 / 20054"
        total += len(data["results"])
        print(f"{total} / {data['count']}")

        # The API tells us where the next page is, so we don't have to
        # work out the offset ourselves. On the last page, "next" is None,
        # which ends the while loop.
        url = data.get("next")

        # Wait half a second before the next request so we don't
        # overload the server (and risk getting blocked).
        time.sleep(0.5)

# When the loop ends, the "with" block automatically closes the file.
print("Done!")