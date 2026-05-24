from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent

LARGE_DIR = BASE_DIR / "images" / "Large"
OUTPUT_JSON = BASE_DIR / "data" / "covers.json"


COUNTRY_LOOKUP = {
    "jp": "Japan",
    "us": "United States",
    "tw": "Taiwan"
}


def make_title(parts):
    # filename format: jp-kyoto-turtle-01.jpg
    # title should come from middle subject words
    subject_parts = parts[2:-1]

    if not subject_parts:
        return ""

    return " ".join(word.capitalize() for word in subject_parts)


def display_text(slug):
    return " ".join(word.capitalize() for word in slug.split("-"))


def build_record(image_path):
    stem = image_path.stem

    # Split country from rest
    country_code = stem[:2]
    remainder = stem[3:]   # skip "jp-"

    parts = remainder.split("--")

    city_slug = parts[0] if len(parts) > 0 else ""
    subject_slug = parts[1] if len(parts) > 1 else ""

    country = COUNTRY_LOOKUP.get(country_code, country_code.upper())
    city = display_text(city_slug)
    title = display_text(subject_slug)

    return {
        "id": stem,
        "title": title,

        "country": country,
        "region": "",
        "city": city,
        "location": "",

        "tags": [],

        "short_description": "",
        "description": "",

        "date_photographed": None,
        "gps": None,

        "filename": image_path.name,
        "large": f"images/Large/{image_path.name}",
        "thumb": f"images/Thumbs/{image_path.name}"
    }

def main():
    records = []

    image_files = sorted(LARGE_DIR.glob("*.jpg"))

    for image_path in image_files:
        records.append(build_record(image_path))

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(records)} records to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()