import json

blocks = {
 "validation_etag_strong": {
    "id": 42, "name": "Klaviatura", "price": 250000, "currency": "UZS"
 },
 "list_response": {
    "data": [
      {"id": 1, "title": "Birinchi maqola"},
      {"id": 2, "title": "Ikkinchi maqola"}
    ],
    "total": 2
 },
 "user_private": {
    "id": 1001,
    "name": "Oqil",
    "balance": 1250000,
    "currency": "UZS"
 },
 "config_public": {
    "max_upload_mb": 25,
    "supported_currencies": ["UZS", "USD", "EUR"],
    "maintenance": False
 }
}

for name, obj in blocks.items():
    s = json.dumps(obj, ensure_ascii=False)
    json.loads(s)  # round-trip
    print("OK", name)
print("ALL JSON VALID")
