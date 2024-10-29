class Silbentrennung:
    def __init__(self):
        # Erweiterte Liste der untrennbaren Konsonantenverbindungen und der Vokale
        self.__untrennbare_konsonantenverbindungen = [
            'ch', 'ck', 'sch', 'ph', 'rh', 'sh', 'th', 'ng', 'st', 'sp', 'pf', 'ts', 'sf', 'tsch'
        ]
        self.__vokale = "aeiouäöü"
        self.__diphthonge = ['ie', 'ei', 'au', 'eu', 'äu']
        self.__suffixe = ['heit', 'keit', 'ung', 'schaft', 'tion', 'sion', 'ismus']
        self.__prefixe = ['ab', 'be', 'ent', 'er', 'ge', 'ver', 'zer', 'miss', 'über', 'unter', 'um', 'aus', 'an']

    def __ist_vokal(self, buchstabe: str) -> bool:
        # Überprüft, ob ein Buchstabe ein Vokal ist
        return buchstabe.lower() in self.__vokale

    def __ist_diphthong(self, buchstabenfolge: str) -> bool:
        # Überprüft, ob eine Buchstabenfolge ein Diphthong ist
        return buchstabenfolge.lower() in self.__diphthonge

    def __ist_untrennbare_konsonantenverbindung(self, konsonanten: str) -> bool:
        # Überprüft, ob eine Konsonantenverbindung untrennbar ist
        return konsonanten in self.__untrennbare_konsonantenverbindungen

    def __ist_suffix(self, wort: str) -> bool:
        # Überprüft, ob das Wort mit einem bekannten Suffix endet
        for suffix in self.__suffixe:
            if wort.endswith(suffix):
                return True
        return False

    def __finde_suffix(self, wort: str) -> str:
        # Findet das passende Suffix im Wort
        for suffix in sorted(self.__suffixe, key=len, reverse=True):
            if wort.endswith(suffix):
                return suffix
        return ""

    def __ist_prefix(self, wort: str) -> bool:
        # Überprüft, ob das Wort mit einem bekannten Präfix beginnt
        for prefix in self.__prefixe:
            if wort.startswith(prefix):
                return True
        return False

    def __finde_prefix(self, wort: str) -> str:
        # Findet das passende Präfix im Wort
        for prefix in sorted(self.__prefixe, key=len, reverse=True):
            if wort.startswith(prefix):
                return prefix
        return ""

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

        # Präfix-Erkennung und -Trennung
        prefix = ""
        if self.__ist_prefix(wort):
            prefix = self.__finde_prefix(wort)
            aktuelle_silbe += prefix
            i += len(prefix)
            silben.append(aktuelle_silbe)
            aktuelle_silbe = ""

        while i < wortlaenge:
            aktuelle_silbe += wort[i]

            # Prüfe auf Diphthong
            if i < wortlaenge - 1 and self.__ist_diphthong(wort[i:i+2]):
                aktuelle_silbe += wort[i+1]
                i += 2
                continue

            # Prüfe Vokal-Konsonant-Muster
            if self.__ist_vokal(wort[i]):
                konsonantenfolge = ""
                j = i + 1

                # Sammle alle nachfolgenden Konsonanten bis zum nächsten Vokal
                while j < wortlaenge and not self.__ist_vokal(wort[j]):
                    konsonantenfolge += wort[j]
                    j += 1

                # Bei Konsonanten zwischen Vokalen:
                if konsonantenfolge:
                    # Überprüfung auf untrennbare Konsonantenverbindungen
                    if len(konsonantenfolge) >= 2 and self.__ist_untrennbare_konsonantenverbindung(konsonantenfolge[:2]):
                        aktuelle_silbe += konsonantenfolge[:2]
                        i += 2
                    else:
                        # Mehrere Konsonanten: teile entsprechend den Silbenbildungsregeln
                        if len(konsonantenfolge) > 1:
                            # Beispielregel: bei 'tt' trenne nach dem ersten 't'
                            aktuelle_silbe += konsonantenfolge[:-1]
                            i += len(konsonantenfolge) - 1
                        else:
                            # Ein einzelner Konsonant geht zur nächsten Silbe
                            silben.append(aktuelle_silbe)
                            aktuelle_silbe = ""
                            i += 1
                            continue

                    # Füge die Silbe hinzu, falls ein Vokal vorhanden ist
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

        # Berücksichtige Suffixe
        if self.__ist_suffix(wort):
            suffix = self.__finde_suffix(wort)
            if suffix:
                # Suche die Position, wo das Suffix beginnt
                suffix_start = wort.rfind(suffix)
                # Trenne die Silbenliste vor dem Suffix
                neue_silben = []
                for silbe in silben:
                    if wort.find(silbe) + len(silbe) <= suffix_start:
                        neue_silben.append(silbe)
                    else:
                        break
                # Füge das Suffix als eigene Silbe hinzu
                neue_silben.append(suffix)
                silben = neue_silben

        # Rückgabe der Silben mit Trennzeichen "·"
        return "·".join(silben)
