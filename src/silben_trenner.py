class Silbentrennung:
    def __init__(self):
        # Liste der untrennbaren Konsonantenverbindungen und der Vokale
        self.__untrennbare_konsonantenverbindungen = ['ch', 'ck', 'sch', 'ph', 'rh', 'sh', 'th', 'ng', 'st']
        self.__vokale = "aeiouäöü"

    def __ist_vokal(self, buchstabe: str) -> bool:
        # Überprüft, ob ein Buchstabe ein Vokal ist
        return buchstabe.lower() in self.__vokale

    def __ist_untrennbare_konsonantenverbindung(self, konsonanten: str) -> bool:
        # Überprüft, ob eine Konsonantenverbindung untrennbar ist
        return konsonanten in self.__untrennbare_konsonantenverbindungen

    def __korrigiere_alleinstehende_buchstaben(self, silben: list) -> list:
        # Überprüft die Silbenliste und verbindet einzelne Konsonanten mit der vorherigen oder nächsten Silbe
        korrigierte_silben = []
        for i in range(len(silben)):
            if len(silben[i]) == 1 and not self.__ist_vokal(silben[i]):
                # Falls die Silbe nur ein Konsonant ist, füge sie zur vorherigen oder nächsten Silbe hinzu
                if i > 0:
                    korrigierte_silben[-1] += silben[i]  # Füge zur vorherigen Silbe hinzu
                elif i < len(silben) - 1:
                    silben[i + 1] = silben[i] + silben[i + 1]  # Füge zur nächsten Silbe hinzu
            else:
                korrigierte_silben.append(silben[i])
        return korrigierte_silben

    def trenne_wort_in_silben(self, wort: str) -> str:
        # Trennt ein Wort in Silben und gibt es als String mit "·" getrennt zurück
        silben = []
        aktuelle_silbe = ""
        i = 0
        wortlaenge = len(wort)

        while i < wortlaenge:
            aktuelle_silbe += wort[i]

            # Prüfe Vokal-Konsonant-Vokal-Muster
            if self.__ist_vokal(wort[i]):
                konsonantenfolge = ""
                j = i + 1

                # Sammle alle nachfolgenden Konsonanten bis zum nächsten Vokal
                while j < wortlaenge and not self.__ist_vokal(wort[j]):
                    konsonantenfolge += wort[j]
                    j += 1

                # Bei Konsonanten zwischen Vokalen:
                if konsonantenfolge:
                    if len(konsonantenfolge) == 1:
                        # Ein einzelner Konsonant geht zur nächsten Silbe (Fa·mi·lie)
                        aktuelle_silbe += konsonantenfolge
                        i += 1
                    elif self.__ist_untrennbare_konsonantenverbindung(konsonantenfolge[:2]):
                        # Untrennbare Konsonantenverbindung bleibt in einer Silbe (Schmet·ter·ling)
                        aktuelle_silbe += konsonantenfolge[:2]
                        i += 2
                    else:
                        # Mehrere Konsonanten: alles außer letztem Konsonanten zur aktuellen Silbe
                        aktuelle_silbe += konsonantenfolge[:-1]
                        i += len(konsonantenfolge) - 1

                    # Füge die Silbe hinzu
                    if any(self.__ist_vokal(b) for b in aktuelle_silbe):
                        silben.append(aktuelle_silbe)
                        aktuelle_silbe = ""
                else:
                    # Falls keine Konsonanten folgen, ist die Silbe vollständig
                    silben.append(aktuelle_silbe)
                    aktuelle_silbe = ""

            i += 1

        # Füge letzte Silbe hinzu
        if aktuelle_silbe:
            silben.append(aktuelle_silbe)

        # Korrigiere alleinstehende Buchstaben
        silben = self.__korrigiere_alleinstehende_buchstaben(silben)

        # Rückgabe der Silben mit Trennzeichen "·"
        return "·".join(silben)
