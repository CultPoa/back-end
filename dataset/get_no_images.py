import re

INPUT_FILE = "new_insert.sql"
OUTPUT_FILE = "missing_image.sql"

pattern = re.compile(
    r"VALUES\s*\((.*)\);?$",
    re.IGNORECASE
)

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    lines = file.readlines()

result = []

for line in lines:
    match = pattern.search(line)

    if not match:
        continue

    values = match.group(1)

    if "wikipedia" not in values.lower():
        continue

    if ", NULL," in values:
        tokens = values.split(",")

        image = tokens[6].strip()
        wikipedia = tokens[7].strip()

        if image.upper() == "NULL" and wikipedia.upper() != "NULL":
            result.append(line)

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    file.writelines(result)
