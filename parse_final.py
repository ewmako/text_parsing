# -*- encoding: utf-8 -*-
import os
import re
import codecs

# KONFIGURACJA PROGRAMU ==============================

input_dir = "/home/txt"
output_dir = "/home/parsed_txt"
if not os.path.exists(output_dir):
  os.mkdir(output_dir)

# Pobierz sciezki do plikow do przetworzenia ==========
filepaths = []
for filename in os.listdir(input_dir):
  if not filename.endswith("txt"):
    continue
  filepaths.append(os.path.join(input_dir, filename))

# Iteruj po plikach ===================================
for filepath in filepaths:

  # wczytaj dane z pliku ==============================
  f = open(filepath, "r")
  fcontent = f.read()
  fcontent = unicode(fcontent, "utf-8")
  f.close()

  # Usun poczatek =====================================
  idx = fcontent.find(u'(Początek posiedzenia')
  if idx == -1:
    idx = fcontent.find(u'(Wznowienie posiedzenia')
    if idx != -1:
      fcontent = fcontent[idx:]
    else:
      print("Nie ma poczatku...")
  else:
    fcontent = fcontent[idx:]

  # Usun koniec =======================================
  idx = fcontent.find(u'Załącznik nr 1')
  if idx == -1:
    print("Nie ma konca...")
  else:
    fcontent = fcontent[:idx]

  # regex =============================================

  # znajduje pattern: dwa lub więcej entery dowolny ciąg znaków dwa entery
  p = re.compile(ur'\n{2,}.*?\n\n', re.UNICODE)
  m = p.findall(fcontent)

  # usun powtorzone
  m = list(set(m))

  # Usun
  for e in m:
    fcontent = fcontent.replace(e, "")

  # Usun didaskalia ===================================
  while True:
    idx = fcontent.find(u'(')
    end_idx = fcontent.find(")",idx, -1)
    if idx == -1:
      break
    fcontent1 = fcontent[:idx]
    fcontent2 = fcontent[end_idx+1:]
    fcontent = fcontent1 + fcontent2

  # Save ==============================================
  outfilepath = os.path.join(output_dir, os.path.basename(filepath))
  f = codecs.open(outfilepath, encoding='utf-8', mode='w+')
  f.write(fcontent)
  f.close()

