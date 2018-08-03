# -*- encoding: utf-8 -*-
import os
import re
import codecs

# KONFIGURACJA PROGRAMU ==============================

# folder wejsciowy
input_dir = "/home/txt"

# tytuly do sprawdzenia
titles = [u"Marszałek", u"Wicemarszałek", u"Prezes", u"Wiceprezes", u"Minister",
	  u"Sekretarz", u"Podsekretarz", u"Poseł", u"Senator", u"Starosta", u"Wojewoda",
	  u"Prezydent", u"Burmistrz", u"Wójt"]

# Wyjściowdy dict
got_it = {}
for title in titles:
    got_it[title] = False

# Skompiluj regexy
regexes = {}
for title in titles:
  p = re.compile(title + " (.*?)(\n*?)(.*?)(\n*?)(.*?):\n", re.UNICODE)
  regexes[title] = p

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

  # Sprawdz kazdy tytul
  for title in titles:
    m = regexes[title].findall(fcontent)
    m = list(set(m))

    # Jezeli jest przynajmniej jedno wystapienie tytulu
    if len(m) > 0:
      # Zapamietaj tytul jako wystapiony
      got_it[title] = True

# Wyswietl info na temat kazdego tytulu ===============
for key, val in got_it.iteritems():
  print key, val
