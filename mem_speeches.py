# -*- encoding: utf-8 -*-
import os
import re
import codecs

# KONFIGURACJA PROGRAMU ==============================

input_dir = "/home/txt"
output_dir = "/home/speeches2"
if not os.path.exists(output_dir):
  os.mkdir(output_dir)

# Pobierz sciezki do plikow do przetworzenia ==========
filepaths = []
for filename in os.listdir(input_dir):
  if not filename.endswith("txt"):
    continue
  filepaths.append(os.path.join(input_dir, filename))

# wystepujace tytuly =================================
titles = [u"Marszałek", u"Wicemarszałek", u"Prezes", u"Wiceprezes", u"Minister",
	  u"Sekretarz", u"Podsekretarz", u"Poseł", u"Senator"]

# Skompiluj regexy
regexes = {}
for title in titles:
  p = re.compile(title + " .*?\n*?.*?\n*?.*?:\n", re.UNICODE)
  regexes[title] = p

# Iteruj po plikach ===================================
for filepath in filepaths:

  # wczytaj dane z pliku ==============================
  f = open(filepath, "r")
  fcontent = f.read()
  fcontent = unicode(fcontent, "utf-8")
  f.close()

  # Sprawdz kazdy tytul i zapisz indeksy
  start_indices = []
  for title in titles:
    for match in regexes[title].finditer(fcontent):
      index = match.start()
      start_indices.append(index)

  # Posortuj
  start_indices = sorted(start_indices)
  

  for idx in range(0, len(start_indices)-1):
    # Zdobadz nazwisko
    mem_start_idx = start_indices[idx]
    mem_stop_idx = fcontent.find(":",mem_start_idx)
    mem_name = fcontent[mem_start_idx:mem_stop_idx]
    mem_name = mem_name.replace(u"\n", u" ")				# Usun ewnetualne entery
    mem_name = mem_name.replace(u"Sprawozdawca", u"")			# Nie dbamy, czy dany posel jest akurat sekretarzem
    for title in titles:						# Usun wszelkie tytuly
      mem_name = mem_name.replace(title, "")
    mem_name = ' '.join(mem_name.split())				# Usun wielokrotne spacje
    mem_name = mem_name + ".txt"
    # Zdobadz wypowiedz
    mem_talk_start_idx = mem_stop_idx+1
    mem_talk_stop_idx = start_indices[idx+1]
    one_speech = fcontent[mem_talk_start_idx:mem_talk_stop_idx]
    one_speech = one_speech.replace(u"-\n", u"")			# Usun ewnetualne przeniesienia do nowej linii
    one_speech = one_speech.replace(u"\n", u" ")			# Usun ewnetualne entery
    one_speech = ' '.join(one_speech.split())				# Usun wielokrotne spacje
    one_speech = one_speech + '\n\n'
    #print mem_name, '\n', one_speech

    # Save ==============================================
    outfilepath = os.path.join(output_dir, mem_name)
    f = codecs.open(outfilepath, encoding='utf-8', mode='a')
    f.write(one_speech)
    f.close()
