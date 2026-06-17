# MkDocs post-build hook.
# Qidiruv indeksi (search_index.json) Cloudflare Workers/Pages ning 25 MiB
# bir-fayl limitidan oshmasligi uchun har bo'lim matnini cheklaydi.
# 37+ kitob to'planganda indeks ~30 MiB ga yetdi; bu hook uni ~19 MiB ga tushiradi.
# Sarlavhalar to'liq saqlanadi; faqat uzun bo'limlarning matni birinchi MAX_TEXT
# belgidan keyin kesiladi (qidiruv: barcha bo'lim sarlavha + boshlanishidan topiladi).
import json
import os

MAX_TEXT = 1000  # har bo'lim matni shu belgidan keyin kesiladi


def on_post_build(config, **kwargs):
    path = os.path.join(config["site_dir"], "search", "search_index.json")
    if not os.path.exists(path):
        return

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    docs = data.get("docs", [])
    trimmed = 0
    for d in docs:
        text = d.get("text", "")
        if len(text) > MAX_TEXT:
            d["text"] = text[:MAX_TEXT]
            trimmed += 1

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

    size_mib = os.path.getsize(path) / 1048576
    print(
        f"[trim_search_index] {len(docs)} bo'lim, {trimmed} ta kesildi "
        f"(MAX_TEXT={MAX_TEXT}) -> {size_mib:.1f} MiB"
    )
