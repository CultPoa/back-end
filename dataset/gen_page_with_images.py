from pathlib import Path

items = []

for line in Path("insert.sql").read_text(encoding="utf-8").splitlines():
    if not line.startswith("INSERT INTO places"):
        continue

    name = line.split("gen_random_uuid(), '", 1)[1].split("'", 1)[0]

    image = line.rsplit(", ", 3)[1]

    if image == "NULL":
        continue

    image_url = image.strip("'")

    items.append(
        f"""
        <div style="display:inline-block;margin:8px;text-align:center">
            <img src="{image_url}" width="64" height="64">
            <div>{name}</div>
        </div>
        """
    )

html = f"""
<!DOCTYPE html>
<html>
<body>
{''.join(items)}
</body>
</html>
"""

Path("index.html").write_text(html, encoding="utf-8")
