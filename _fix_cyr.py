#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ai-python kitobidagi kirill-homogliflarni lotin'ga fonetik transliteratsiya qiladi."""
import os, re, glob

BOOK = r"C:/Users/imomn/Desktop/e-books/docs/ai-python"
CYR = re.compile(r"[Ѐ-ӿ]")

M = {
 'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'yo','ж':'j','з':'z','и':'i',
 'й':'y','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t',
 'у':'u','ф':'f','х':'x','ц':'ts','ч':'ch','ш':'sh','щ':'sh','ъ':"'",'ы':'i','ь':"'",
 'э':'e','ю':'yu','я':'ya','ў':"o'",'қ':'q','ғ':"g'",'ҳ':'h','ҷ':'j','һ':'h',
 'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'E','Ё':'Yo','Ж':'J','З':'Z','И':'I',
 'Й':'Y','К':'K','Л':'L','М':'M','Н':'N','О':'O','П':'P','Р':'R','С':'S','Т':'T',
 'У':'U','Ф':'F','Х':'X','Ц':'Ts','Ч':'Ch','Ш':'Sh','Щ':'Sh','Ы':'I',
 'Э':'E','Ю':'Yu','Я':'Ya','Ў':"O'",'Қ':'Q','Ғ':"G'",'Ҳ':'H',
}

def fix(text):
    return "".join(M.get(ch, ch) for ch in text)

changed = 0
for path in glob.glob(os.path.join(BOOK, "*.md")) + glob.glob(os.path.join(BOOK, "rasmlar", "*.svg")):
    raw = open(path, encoding="utf-8").read()
    if CYR.search(raw):
        new = fix(raw)
        leftover = CYR.findall(new)
        open(path, "w", encoding="utf-8", newline="\n").write(new)
        changed += 1
        print(f"TUZATILDI: {os.path.basename(path)}" + (f"  QOLDIQ: {set(leftover)}" if leftover else ""))

print(f"\nJAMI tuzatilgan fayl: {changed}")
