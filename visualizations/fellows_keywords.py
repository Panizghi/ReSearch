import json
import pandas as pd

filepath = "ReSearchcrawler/ReSearchcrawler/acm_profiles.jsonl"

with open(filepath, "r") as f:
    fellows_data = [json.loads(line) for line in f]


# get all keywords
all_keywords = set()
for fellow in fellows_data:
    for keyword in fellow["keywords"]:
        all_keywords.update(keyword["label"])

print(all_keywords)

# # Convert to sorted list for consistent ordering
# all_keywords = sorted(all_keywords)

# # Build a DataFrame
# rows = []
# for person in data:
#     row = {"name": person["name"]}
#     row.update({keyword: person["keywords"].get(keyword, 0) for keyword in all_keywords})
#     rows.append(row)

# # Create DataFrame
# df = pd.DataFrame(rows)