// Mani uzdevumi — lietotnes loģika
"use strict";

const GLABATUVES_ATSLEGA = "pd1-uzdevumi";

// Lietotnes stāvoklis
let uzdevumi = [];
let aktivaisFiltrs = "all";

// DOM elementi
const forma = document.getElementById("task-form");
const ievade = document.getElementById("task-input");
const saraksts = document.getElementById("task-list");
const skaititajs = document.getElementById("counter");
const filtruPogas = document.querySelectorAll("[data-filter]");

// Ielādē uzdevumus no localStorage; bojātu datu gadījumā sāk ar tukšu sarakstu
function ieladetUzdevumus() {
  try {
    const dati = JSON.parse(localStorage.getItem(GLABATUVES_ATSLEGA));
    if (!Array.isArray(dati)) {
      return [];
    }
    return dati
      .filter((u) => u && typeof u.id === "number" && typeof u.text === "string")
      .map((u) => ({ id: u.id, text: u.text, done: Boolean(u.done) }));
  } catch (kluda) {
    return [];
  }
}

// Saglabā uzdevumus localStorage kā JSON
function saglabatUzdevumus() {
  try {
    localStorage.setItem(GLABATUVES_ATSLEGA, JSON.stringify(uzdevumi));
  } catch (kluda) {
    // Glabātuve nav pieejama — lietotne turpina darboties bez saglabāšanas
  }
}

// Izveido unikālu id: Date.now(), palielinot, ja tāds jau eksistē
function izveidotId() {
  let id = Date.now();
  while (uzdevumi.some((u) => u.id === id)) {
    id += 1;
  }
  return id;
}

// Pievieno jaunu uzdevumu no ievades lauka
function pievienotUzdevumu() {
  const teksts = ievade.value.trim();
  ievade.value = "";
  ievade.focus();
  if (teksts === "") {
    return;
  }
  uzdevumi.push({ id: izveidotId(), text: teksts, done: false });
  atjaunot();
}

// Pārslēdz uzdevuma izpildes stāvokli
function parslegtUzdevumu(id) {
  const uzdevums = uzdevumi.find((u) => u.id === id);
  if (uzdevums) {
    uzdevums.done = !uzdevums.done;
    atjaunot();
  }
}

// Dzēš uzdevumu pēc id
function dzestUzdevumu(id) {
  uzdevumi = uzdevumi.filter((u) => u.id !== id);
  atjaunot();
}

// Atgriež uzdevumus, kas atbilst aktīvajam filtram
function filtretieUzdevumi() {
  if (aktivaisFiltrs === "active") {
    return uzdevumi.filter((u) => !u.done);
  }
  if (aktivaisFiltrs === "done") {
    return uzdevumi.filter((u) => u.done);
  }
  return uzdevumi;
}

// Izveido vienu saraksta rindu (teksts tiek ievietots ar textContent)
function izveidotRindu(uzdevums) {
  const rinda = document.createElement("li");
  rinda.dataset.id = String(uzdevums.id);
  rinda.classList.toggle("izpildits", uzdevums.done);

  const rutina = document.createElement("input");
  rutina.type = "checkbox";
  rutina.checked = uzdevums.done;
  rutina.setAttribute("aria-label", "Atzīmēt kā izpildītu");

  const teksts = document.createElement("span");
  teksts.className = "uzdevuma-teksts";
  teksts.textContent = uzdevums.text;

  const dzestPoga = document.createElement("button");
  dzestPoga.type = "button";
  dzestPoga.className = "dzest-btn";
  dzestPoga.textContent = "Dzēst";
  dzestPoga.setAttribute("aria-label", "Dzēst uzdevumu");

  rinda.append(rutina, teksts, dzestPoga);
  return rinda;
}

// Uzzīmē sarakstu atbilstoši filtram
function zimetSarakstu() {
  saraksts.replaceChildren(...filtretieUzdevumi().map(izveidotRindu));
}

// Atjauno skaitītāju ar neizpildīto uzdevumu skaitu
function atjaunotSkaititaju() {
  const atlikusi = uzdevumi.filter((u) => !u.done).length;
  skaititajs.textContent = "Atlikuši " + atlikusi + " uzdevumi";
}

// Vizuāli izceļ izvēlēto filtra pogu
function atjaunotFiltruPogas() {
  filtruPogas.forEach((poga) => {
    const izvelets = poga.dataset.filter === aktivaisFiltrs;
    poga.classList.toggle("aktivs", izvelets);
    poga.setAttribute("aria-pressed", String(izvelets));
  });
}

// Saglabā datus un atjauno visu saskarni pēc katras darbības
function atjaunot() {
  saglabatUzdevumus();
  zimetSarakstu();
  atjaunotSkaititaju();
  atjaunotFiltruPogas();
}

// Nolasa uzdevuma id no rindas, kurā atrodas notikuma elements
function rindasId(elements) {
  const rinda = elements.closest("li");
  return rinda ? Number(rinda.dataset.id) : null;
}

// Piesaista notikumu apstrādātājus
function piesaistitNotikumus() {
  forma.addEventListener("submit", (notikums) => {
    notikums.preventDefault();
    pievienotUzdevumu();
  });

  saraksts.addEventListener("change", (notikums) => {
    if (notikums.target.matches("input[type='checkbox']")) {
      parslegtUzdevumu(rindasId(notikums.target));
    }
  });

  saraksts.addEventListener("click", (notikums) => {
    if (notikums.target.matches(".dzest-btn")) {
      dzestUzdevumu(rindasId(notikums.target));
    }
  });

  filtruPogas.forEach((poga) => {
    poga.addEventListener("click", () => {
      aktivaisFiltrs = poga.dataset.filter;
      atjaunot();
    });
  });
}

// Lietotnes palaišana
uzdevumi = ieladetUzdevumus();
piesaistitNotikumus();
atjaunot();
