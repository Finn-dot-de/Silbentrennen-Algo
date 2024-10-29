from src.silben_trenner import Silbentrennung
import sys

list = [
    "Abenteuer", "Fantasie", "Gelassenheit", "Gemütlichkeit", "Harmonie", 
    "Intelligenz", "Kreativität", "Lebensfreude", "Menschlichkeit", 
    "Nachhaltigkeit", "Neugierde", "Optimismus", "Philosophie", "Schmetterling", 
    "Traumfänger", "Universität", "Verständnis", "Weltanschauung", 
    "Wissenschaft", "Zufriedenheit"
]


if __name__ == "__main__":
    trenne = Silbentrennung()
    line = sys.argv[1:]
    wort = ''.join(line)
    for wort in list:
        getrennt = trenne.trenne_wort_in_silben(wort)
        print(getrennt)