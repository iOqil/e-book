#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Har bobning oldingi/keyingi navigatsiyasi to'g'ri qo'shni bobga ishora qilishini tekshiradi."""
import os, re, glob

BOOK = r"C:/Users/imomn/Desktop/e-books/docs/livewire"
files = sorted(glob.glob(os.path.join(BOOK, "[0-9][0-9]-*.md")))
order = [os.path.basename(f) for f in files]
idx = {name: i for i, name in enumerate(order)}

problems = []
for f in files:
    name = os.path.basename(f)
    i = idx[name]
    text = open(f, encoding="utf-8").read()
    # markdown link targetlari (.md) ni nav qatorlaridan ol
    links = re.findall(r"\]\(\.\/([0-9]{2}-[^)]+\.md)\)", text)
    prev_expected = order[i-1] if i > 0 else None
    next_expected = order[i+1] if i < len(order)-1 else None
    # "Oldingi" va "Keyingi" havolalarini topish
    oldingi = re.findall(r"Oldingi:[^\]]*\]\(\.\/([0-9]{2}-[^)]+\.md)\)", text)
    keyingi = re.findall(r"Keyingi:[^\]]*\]\(\.\/([0-9]{2}-[^)]+\.md)\)", text)
    if prev_expected:
        if not oldingi or oldingi[0] != prev_expected:
            problems.append(f"{name}: OLDINGI '{oldingi[0] if oldingi else 'YO`Q'}' != kutilgan '{prev_expected}'")
    else:
        if oldingi:
            problems.append(f"{name}: birinchi bobda 'Oldingi' bo'lmasligi kerak edi (-> {oldingi})")
    if next_expected:
        if not keyingi or keyingi[0] != next_expected:
            problems.append(f"{name}: KEYINGI '{keyingi[0] if keyingi else 'YO`Q'}' != kutilgan '{next_expected}'")
    else:
        if keyingi:
            problems.append(f"{name}: oxirgi bobda 'Keyingi' bo'lmasligi kerak edi (-> {keyingi})")
    # nav qatori boshda va oxirda bormi (kamida 2 marta README havolasi)
    readme_links = text.count("](./README.md)")
    if readme_links < 2:
        problems.append(f"{name}: navigatsiya yuqori/pastda takrorlanmagan (README havolasi {readme_links} marta)")

print(f"Tekshirilgan boblar: {len(files)}")
print(f"Navigatsiya muammolari: {len(problems)}")
for p in problems:
    print("  -", p)
if not problems:
    print("  >>> Barcha oldingi/keyingi navigatsiya TO'G'RI <<<")
