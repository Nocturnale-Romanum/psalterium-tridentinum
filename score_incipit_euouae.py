import os

def incipit_from_gabc(gabc):
  """From some gabc code, takes the incipit until *, replaces the last punctuation, if any, with a dot, and adds the euouae."""
  # the gabc needs to have a GreSpecial asterisk and an EUOUAE tag
  if "<eu>" not in gabc or "<sp>*</sp>" not in gabc:
    raise ValueError("GABC has no euouae or no asterisk")
  euouae = "<eu>"+gabc.split("<eu>")[1]  
  incipit = gabc.split("<sp>*</sp>")[0]
  # the following replaces whatever punctuation the incipit ends with with a dot.
  parts = incipit.split("(")
  last_lyrics = list(parts[-2])
  while last_lyrics[-1] in [" ", ".", ",", ";", ":"]:
    del last_lyrics[-1]
  last_lyrics = "".join(last_lyrics)+"."
  parts[-2] = last_lyrics
  incipit = "(".join(parts)
  # the following adds a closing NABC bracket if the incipit has an opening NABC bracket
  # this is a naive algorithm that fails if the brackets have a non-default height
  if ("|ob" in incipit or "|/ob" in incipit or "|//ob" in incipit or "|`ob" in incipit or "``ob" in incipit) and "cb)" not in incipit:
    parts = incipit.split(")")
    parts[-2]+="cb"
    incipit = ")".join(parts)
  return incipit+" (::) "+euouae


def remove_euouae_from_gabc(gabc):
  """from some gabc code, removes the euouae"""
  return gabc.split("<eu>")[0]

def euouae_before_gabc(gabc):
  """from some gabc code, takes the EUOUAE at the end and puts it in front."""
  euouae = "<eu>"+gabc.split("<eu>")[1]
  antiphon = gabc.split("<eu>")[0]
  parts = antiphon.split(")")
  clef = parts[0]+") "
  del parts[0]
  antiphon = ")".join(parts)
  return "\n"+clef+euouae+antiphon

def custos_before_gabc(gabc):
  """from some gabc code, takes the last note of the EUOUAE at the end and puts it in front as custos"""
  lastnote = gabc.split("<eu>")[1].split("(::)")[0].split(")")[-2][-1]
  antiphon = gabc.split("<eu>")[0]
  parts = antiphon.split(")")
  clef = parts[0]+") "
  del parts[0]
  antiphon = ")".join(parts)
  return "\n" + clef + "~({}+) ".format(lastnote) + antiphon

def modify_gabc_file(source_name, target_name, function):
  """isolates the gabc from a gabc file, transforms it according to <function>, 
  and outputs a gabc file with the given target name, the same headers, and the new gabc."""
  contents = open(source_name, encoding="utf-8").read()
  output = open(target_name, "w", encoding="utf-8")
  contents = contents.split("%%")
  gabc = contents[-1]
  gabc = function(gabc)
  contents[-1] = gabc
  contents = "%%".join(contents)
  output.write(contents)


os.chdir("nocturnale-romanum/gabc")
files = os.listdir(".")
files = [f for f in files if f.endswith("A.gabc") or f.endswith("A1.gabc") or f.endswith("A2.gabc") or f.endswith("A3.gabc") or f.endswith("A4.gabc") or f.endswith("A5.gabc") or f.endswith("A6.gabc") or f.endswith("A2a.gabc") or f.endswith("A2b.gabc")]

for f in files:
  try:
    modify_gabc_file(f, f.split(".gabc")[0]+"_incipit.gabc", incipit_from_gabc)
    modify_gabc_file(f, f.split(".gabc")[0]+"_noeuouae.gabc", custos_before_gabc)
  except:
    print(f)