from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent

LARGE_DIR = BASE_DIR / "images" / "Large"

GENERATED_JSON = BASE_DIR / "data" / "covers.generated.json"
MANUAL_JSON = BASE_DIR / "data" / "covers.manual.json"
FINAL_JSON = BASE_DIR / "data" / "covers.json"


COUNTRY_LOOKUP = {
    "jp": "Japan",
    "us": "United States",
    "tw": "Taiwan"
}


def display_text(slug):
    return " ".join(word.capitalize() for word in slug.split("-"))


def load_json(path, default):
    if not path.exists():
        return default

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def build_generated_record(image_path):
    stem = image_path.stem

    country_code = stem[:2]
    remainder = stem[3:]

    parts = remainder.split("--")

    city_slug = parts[0] if len(parts) > 0 else ""
    subject_slug = parts[1] if len(parts) > 1 else ""

    country = COUNTRY_LOOKUP.get(country_code, country_code.upper())

    return {
        "id": stem,
        "title": display_text(subject_slug),
        "country": country,
        "city": display_text(city_slug),
        "date_photographed": None,
        "gps": None,
        "filename": image_path.name,
        "large": f"images/Large/{image_path.name}",
        "thumb": f"images/Thumbs/{image_path.name}"
    }


def blank_manual_record(record_id):
    return {
        "id": record_id,
        "region": "",
        "location": "",
        "tags": [],
        "short_description": "",
        "description": "",
        "foundry": "",
        "artist": "",
        "notes": ""
    }


def merge_records(generated_record, manual_record):
    merged = generated_record.copy()
    merged.update(manual_record)
    return merged


def main():
    image_files = sorted(LARGE_DIR.glob("*.jpg"))

    generated_records = [
        build_generated_record(image_path)
        for image_path in image_files
    ]

    existing_manual_records = load_json(MANUAL_JSON, [])

    manual_by_id = {
        record["id"]: record
        for record in existing_manual_records
    }

    updated_manual_records = []

    for generated_record in generated_records:
        record_id = generated_record["id"]

        if record_id in manual_by_id:
            updated_manual_records.append(manual_by_id[record_id])
        else:
            updated_manual_records.append(blank_manual_record(record_id))

    final_records = []

    manual_by_id = {
        record["id"]: record
        for record in updated_manual_records
    }

    for generated_record in generated_records:
        record_id = generated_record["id"]
        manual_record = manual_by_id[record_id]
        final_records.append(merge_records(generated_record, manual_record))

    write_json(GENERATED_JSON, generated_records)
    write_json(MANUAL_JSON, updated_manual_records)
    write_json(FINAL_JSON, final_records)

    print(f"Wrote {len(generated_records)} records")
    print(f"Generated: {GENERATED_JSON}")
    print(f"Manual:    {MANUAL_JSON}")
    print(f"Final:     {FINAL_JSON}")


if __name__ == "__main__":
    main()