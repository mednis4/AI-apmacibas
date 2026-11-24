# =====================================================================
#  PRAKTISKAIS DARBS 1 — UZDEVUMS  (≈ 35 min)
#  Nākamā vārda prognozēšana ar varbūtībām (mazs "valodas modelis")
# =====================================================================
#  Ideja: lielais valodas modelis (piem., ChatGPT, Claude) katrā solī
#  uzmin NĀKAMO vārdu. Mēs uzbūvēsim ļoti mazu modeli, kas skaita,
#  kurš vārds cik bieži seko kuram vārdam.
#
#  KĀ STRĀDĀT:
#   1. Atver šo failu Visual Studio Code.
#   2. Aizpildi vietas, kur rakstīts  # TODO
#   3. Palaid failu (▶ poga augšā labajā stūrī vai  python pd1_nakamais_vards.py)
#   4. Apakšā redzēsi pārbaudes: ✅ = pareizi, ❌ = vēl jāstrādā
# =====================================================================

TEKSTS = """
Kaķis guļ uz dīvāna. Kaķis guļ uz paklāja. Suns guļ uz paklāja.
Kaķis sēž uz palodzes. Suns skrien pa parku. Kaķis skrien pa parku.
Suns guļ uz dīvāna. Kaķis guļ uz dīvāna. Putns sēž uz jumta.
Kaķis ēd zivi. Suns ēd gaļu. Kaķis ēd zivi.
"""


# ---------------------------------------------------------------------
# 1.1 Sadali tekstu vārdos
# ---------------------------------------------------------------------
# Piemērs: "Kaķis guļ. Suns"  ->  ["kaķis", "guļ", ".", "suns"]
# Padomi:
#   teksts.lower()               – pārvērš visus burtus par mazajiem
#   teksts.replace(".", " . ")   – ap punktu ieliek atstarpes
#   teksts.split()               – sadala tekstu pa atstarpēm sarakstā
def sadalit_vardos(teksts):
    # TODO: uzraksti 3 rindiņas, izmantojot padomus augstāk
    teksts = teksts.lower()
    teksts = teksts.replace(".", " . ")
    return teksts.split()


# ---------------------------------------------------------------------
# 1.2 Saskaiti vārdu pārus (kurš vārds seko kuram)
# ---------------------------------------------------------------------
# Piemērs: ["a", "b", "a", "c", "a", "b"]
#   -> {"a": {"b": 2, "c": 1}, "b": {"a": 1}, "c": {"a": 1}}
# Padoms: ej cauri sarakstam ar  for i in range(len(vardi) - 1):
#         tagad = vardi[i],  nakamais = vardi[i + 1]
def skaitit_parus(vardi):
    pari = {}
    # TODO: aizpildi vārdnīcu "pari"
    for i in range(len(vardi) - 1):
        tagad = vardi[i]
        nakamais = vardi[i + 1]
        
        if tagad not in pari:
            pari[tagad] = {}
        if nakamais not in pari[tagad]:
            pari[tagad][nakamais] = 0
        pari[tagad][nakamais] += 1
    
    return pari


# ---------------------------------------------------------------------
# 1.3 Pārvērt skaitus varbūtībās
# ---------------------------------------------------------------------
# Varbūtība = cik reizes šis vārds / cik reizes VISI vārdi kopā
# Piemērs: {"b": 2, "c": 1, "d": 1}  ->  {"b": 0.5, "c": 0.25, "d": 0.25}
# Padoms: kopa = sum(skaiti.values())
def varbutibas(skaiti):
    rezultats = {}
    kopa = sum(skaiti.values())
    if kopa == 0:
        return rezultats
    for vards, skaitlis in skaiti.items():
        rezultats[vards] = skaitlis / kopa
    return rezultats


# ---------------------------------------------------------------------
# 1.4 Prognozē visticamāko nākamo vārdu
# ---------------------------------------------------------------------
# Ja vārds nav modelī -> atgriez None.
# Padoms: max(varb, key=varb.get) atrod atslēgu ar lielāko vērtību.
def prognozet(modelis, vards):
    vards = vards.lower()
    if vards not in modelis:
        return None
    varb_dict = varbutibas(modelis[vards])
    return max(varb_dict, key=varb_dict.get)


# ---------------------------------------------------------------------
# 1.5 Ģenerē teikumu (katru reizi ņemot visticamāko vārdu)
# ---------------------------------------------------------------------
# Sāc ar sakuma_vards, tad atkārto: atrodi nākamo vārdu ar prognozet(),
# pievieno to sarakstam. Apstājies, ja nākamais ir "." vai None.
def generet(modelis, sakuma_vards, max_vardi=10):
    teikums = [sakuma_vards.lower()]
    for _ in range(max_vardi):
        nakamais = prognozet(modelis, teikums[-1])
        if nakamais is None or nakamais == ".":
            teikums.append(".")
            break
        teikums.append(nakamais)
    return " ".join(teikums)


# ---------------------------------------------------------------------
# 1.6 (gatavs) Parāda varbūtības kā joslu diagrammu ar # simboliem
# ---------------------------------------------------------------------
def paradit_varbutibas(modelis, vards):
    if vards not in modelis:
        print(f"Vārds '{vards}' modelī nav atrasts.")
        return
    varb = varbutibas(modelis[vards])
    print(f"\nPēc vārda '{vards}' modelis domā:")
    for v, p in sorted(varb.items(), key=lambda x: -x[1]):
        josla = "#" * round(p * 40)
        print(f"  {v:<10} {p*100:5.1f}%  {josla}")


# =====================================================================
#  PĀRBAUDES (nemaini šo daļu)
# =====================================================================
def parbaude(nosaukums, funkcija):
    try:
        ok = funkcija()
    except Exception as e:
        print(f"  ❌ {nosaukums}: kļūda — {e}")
        return
    print(f"  {'✅' if ok else '❌'} {nosaukums}")


if __name__ == "__main__":
    print("PĀRBAUDES:")
    parbaude("1.1 sadalit_vardos", lambda: sadalit_vardos("Kaķis guļ. Suns") == ["kaķis", "guļ", ".", "suns"])
    parbaude("1.2 skaitit_parus", lambda: skaitit_parus(["a", "b", "a", "c", "a", "b"])
             == {"a": {"b": 2, "c": 1}, "b": {"a": 1}, "c": {"a": 1}})
    parbaude("1.3 varbutibas", lambda: varbutibas({"b": 2, "c": 1, "d": 1}) == {"b": 0.5, "c": 0.25, "d": 0.25})

    vardi = sadalit_vardos(TEKSTS)
    modelis = skaitit_parus(vardi)
    parbaude("1.4 prognozet('uz') == 'dīvāna'", lambda: prognozet(modelis, "uz") == "dīvāna")
    parbaude("1.4 nezināms vārds -> None", lambda: prognozet(modelis, "zilonis") is None)
    parbaude("1.5 generet('kaķis')", lambda: generet(modelis, "kaķis") == "kaķis guļ uz dīvāna .")

    print("\nDEMONSTRĀCIJA:")
    print("Vārdu skaits tekstā:", len(vardi))
    paradit_varbutibas(modelis, "uz")
    for sakums in ["kaķis", "suns", "putns"]:
        print(f"Ģenerēts teikums no '{sakums}':", generet(modelis, sakums))

# ---------------------------------------------------------------------
# JAUTĀJUMI PĀRDOMĀM (atbildi komentāros vai pārrunā ar kaimiņu):
#  a) Modelis uzģenerēja "putns sēž uz dīvāna". Vai šāds teikums ir tekstā?
#     Kāpēc modelis to "izdomāja"?
#  b) Pievieno TEKSTAM vēl 3 teikumus par putnu. Kā mainās prognozes?
#  c) Kāpēc visi teikumi beidzas ar "uz dīvāna"? Kā to varētu mainīt?
#     (Atbildi uzzināsi 2. praktiskajā darbā!)
# ---------------------------------------------------------------------
