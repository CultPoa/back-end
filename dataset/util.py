import csv
import re

INPUT_FILE = "insert.sql"
OUTPUT_FILE = "new_insert.sql"

places = {}

pattern = re.compile(
    r"VALUES\s*\((.*)\);?$",
    re.IGNORECASE
)

def parse_values(values_str):
    reader = csv.reader(
        [values_str],
        delimiter=",",
        quotechar="'",
        skipinitialspace=True
    )

    return next(reader)

def sql_value(value):
    value = value.strip()

    if value.upper() == "NULL":
        return "NULL"

    if re.fullmatch(r"-?\d+(\.\d+)?", value):
        return value

    if value == "gen_random_uuid()":
        return value

    escaped = value.replace("'", "''")

    return f"'{escaped}'"

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    for raw_line in file:
        line = raw_line.strip()

        if "VALUES" not in line:
            continue

        match = pattern.search(line)

        if not match:
            continue

        values_str = match.group(1)

        try:
            tokens = parse_values(values_str)
        except Exception:
            continue

        lat = tokens[2].strip()
        lon = tokens[3].strip()

        key = (lat, lon)

        if key not in places:
            places[key] = tokens
            continue

        current = places[key]

        for i in range(len(tokens)):
            old_value = current[i].strip()
            new_value = tokens[i].strip()

            old_is_null = old_value.upper() == "NULL"
            new_is_null = new_value.upper() == "NULL"

            if old_is_null and not new_is_null:
                current[i] = new_value

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    for tokens in places.values():
        formatted = [sql_value(v) for v in tokens]

        line = (
            "INSERT INTO places "
            "(id, name, lat, lon, type, description, image, wikipedia, website) "
            f"VALUES ({', '.join(formatted)});\n"
        )

        file.write(line)
