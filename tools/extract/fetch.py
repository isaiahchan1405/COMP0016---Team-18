# This script fetches all records from the IFRC Ops Learning API and saves them to a file in JSON Lines format.

import requests   
import json       
import time       

# The first page to fetch
url = "https://goadmin.ifrc.org/api/v2/ops-learning/?limit=50&offset=0"

# Running count of how many records we've saved so far
total = 0

# Open the output file once and keep writing to it as each page arrives.
# encoding="utf-8" keeps non-English characters (e.g. French, Arabic) intact.
with open("ops_learning.jsonl", "w", encoding="utf-8") as out:

    # Keep looping as long as there's another page to fetch.
    # When we reach the last page, url becomes None and the loop stops.
    while url:

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
        for rec in data["results"]:
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")

        # Update and print progress, e.g. "3000 / 20054"
        total += len(data["results"])
        print(f"{total} / {data['count']}")

        url = data.get("next")

        time.sleep(0.5)

# When the loop ends, the "with" block automatically closes the file.
print("Done!")