# =====================================================================
#  PRAKTISKAIS DARBS 2 — UZDEVUMS  (≈ 30 min)
#  Kā modelis IZVĒLAS vārdu: nejaušība, temperatūra un top-k
# =====================================================================
#  Modelis neizvēlas vienmēr visticamāko vārdu. Tas "met kauliņu",
#  kurā lielākām varbūtībām ir lielāki laukumi. Temperatūra nosaka,
#  cik "drosmīgi" modelis met kauliņu.
#
#  Aizpildi vietas ar  # TODO  un palaid failu. ✅ = pareizi.
# =====================================================================
import random

random.seed(42)  # lai rezultāti katru reizi būtu vienādi (atkārtojami)

# Modelis teikumam "Kaķis guļ uz ..." ir aprēķinājis šādas varbūtības:
VARBUTIBAS = {
    "dīvāna": 0.45,
    "paklāja": 0.30,
    "palodzes": 0.15,
    "jumta": 0.07,
    "mēness": 0.03,
}


# ---------------------------------------------------------------------
# 2.1 Nejauša izvēle pēc varbūtībām ("rulete")
# ---------------------------------------------------------------------
# Iedomājies lineālu no 0 līdz 1, sadalītu gabalos:
#   dīvāna [0.00–0.45)  paklāja [0.45–0.75)  palodzes [0.75–0.90) ...
# 1) r = random.random()   -> nejaušs skaitlis no 0 līdz 1
# 2) ej cauri vārdiem, saskaiti varbūtības (summa += p)
# 3) tiklīdz r < summa -> atgriez šo vārdu
def izveleties_nejausi(varb):
    # TODO
    # return None
    r = random.random()
    summa = 0.0
    for vards, p in varb.items():
        summa += p
        if r < summa:
            return vards
    # Ja noapaļošanas dēļ summa nedaudz < 1, atgriež pēdējo vārdu ar p > 0
    return [v for v, p in varb.items() if p > 0][-1]


# ---------------------------------------------------------------------
# 2.2 Temperatūra
# ---------------------------------------------------------------------
# 1) Katru varbūtību kāpini pakāpē (1 / T):   p ** (1 / T)
# 2) Saskaiti visas jaunās vērtības:           kopa = sum(...)
# 3) Katru jauno vērtību izdali ar kopa, lai summa atkal būtu 1.
#   T < 1  -> uzvarētājs kļūst vēl stiprāks
#   T = 1  -> nekas nemainās
#   T > 1  -> varbūtības izlīdzinās
def pielietot_temperaturu(varb, T):
    if T <= 0:
        labakais = max(varb, key=varb.get)
        return {v: (1.0 if v == labakais else 0.0) for v in varb}
    jaunas = {}
    # TODO: 1) aizpildi "jaunas"   2) aprēķini kopa   3) atgriez normalizētu vārdnīcu
    # return jaunas
    for vards, p in varb.items():
        jaunas[vards] = p ** (1 / T)
    kopa = sum(jaunas.values())
    return {v: x / kopa for v, x in jaunas.items()}


# ---------------------------------------------------------------------
# 2.3 Eksperiments: 1000 izvēles ar dažādām temperatūrām
# ---------------------------------------------------------------------
# 1) jaunas = pielietot_temperaturu(varb, T)
# 2) skaiti = {v: 0 for v in varb}
# 3) n reizes: izvēlies vārdu ar izveleties_nejausi(jaunas) un palielini skaitu
def eksperiments(varb, T, n=1000):
    skaiti = {v: 0 for v in varb}
    # TODO
    # return skaiti
    jaunas = pielietot_temperaturu(varb, T)
    for _ in range(n):
        skaiti[izveleties_nejausi(jaunas)] += 1
    return skaiti


def zimet_grafiku(skaiti, virsraksts):  # gatavs
    print(f"\n{virsraksts}")
    n = max(sum(skaiti.values()), 1)
    for vards, s in skaiti.items():
        print(f"  {vards:<9} {s:4d}  {'#' * round(s / n * 50)}")


# ---------------------------------------------------------------------
# 2.4 (papilduzdevums) Top-k: atstāj tikai k visticamākos vārdus
# ---------------------------------------------------------------------
# Padoms: sorted(varb.items(), key=lambda x: -x[1])[:k]
# Pēc tam atkal izdali ar kopsummu, lai summa = 1.
def top_k(varb, k):
    # TODO
    # return {}
    labakie = sorted(varb.items(), key=lambda x: -x[1])[:k]
    kopa = sum(p for _, p in labakie)
    return {v: p / kopa for v, p in labakie}


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


def tuvu(a, b):
    return abs(a - b) < 0.001


if __name__ == "__main__":
    print("PĀRBAUDES:")
    parbaude("2.1 izvēle atgriež vārdu no saraksta", lambda: izveleties_nejausi(VARBUTIBAS) in VARBUTIBAS)
    parbaude("2.1 vienmēr 'a', ja tā varbūtība 1", lambda: izveleties_nejausi({"a": 1.0, "b": 0.0}) == "a")
    parbaude("2.2 T=1 neko nemaina", lambda: tuvu(pielietot_temperaturu(VARBUTIBAS, 1)["dīvāna"], 0.45))
    parbaude("2.2 T=0.5 -> 'dīvāna' > 0.45", lambda: pielietot_temperaturu(VARBUTIBAS, 0.5)["dīvāna"] > 0.45)
    parbaude("2.2 T=2 -> 'dīvāna' < 0.45", lambda: pielietot_temperaturu(VARBUTIBAS, 2)["dīvāna"] < 0.45)
    parbaude("2.2 summa vienmēr = 1", lambda: tuvu(sum(pielietot_temperaturu(VARBUTIBAS, 3).values()), 1))
    parbaude("2.3 eksperiments dod 1000 izvēles", lambda: sum(eksperiments(VARBUTIBAS, 1).values()) == 1000)
    parbaude("2.4 top_k(…, 2) atstāj 2 vārdus", lambda: list(top_k(VARBUTIBAS, 2)) == ["dīvāna", "paklāja"])
    parbaude("2.4 top_k summa = 1", lambda: tuvu(sum(top_k(VARBUTIBAS, 3).values()), 1))

    for T in [0.3, 1.0, 2.0]:
        zimet_grafiku(eksperiments(VARBUTIBAS, T), f"1000 izvēles, temperatūra T = {T}")

# ---------------------------------------------------------------------
# JAUTĀJUMI PĀRDOMĀM:
#  a) Kurai temperatūrai "mēness" parādās visbiežāk? Kāpēc tā ir problēma?
#  b) Kādu temperatūru izvēlētos: (1) matemātikas uzdevumam, (2) dzejolim?
#  c) Kāpēc viens un tas pats jautājums čatbotam var dot dažādas atbildes?
# ---------------------------------------------------------------------
