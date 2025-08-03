let currentLang = localStorage.getItem("lang") || "es";
let langData = {};

document.addEventListener("DOMContentLoaded", async () => {
  await loadLanguage(currentLang);
  document.getElementById("language-select").value = currentLang;
  setupNavigation();
  setupForm();
  setupLanguageSwitch();
});

async function loadLanguage(lang) {
  const res = await fetch("lang.json");
  langData = await res.json();
  currentLang = lang;
  localStorage.setItem("lang", lang);
  applyLanguage();
}

function applyLanguage() {
  const t = langData[currentLang];

  document.getElementById("app-title").textContent = t.title;

  const sections = ["home", "new-entry", "history", "stats", "assistant", "settings"];
  sections.forEach((id, i) => {
    document.querySelector(`nav button[data-section="${id}"]`).textContent = t.sections[id];
    document.querySelector(`#${id} h2`).textContent = t.sections[id];
  });

  document.querySelector("#home p").textContent = t.welcome;
  document.querySelector("#entry-title").placeholder = t.placeholders.title;
  document.querySelector("#entry-text").placeholder = t.placeholders.text;
  document.querySelector("#entry-form button").textContent = t.buttons.save;

  document.querySelector("#assistant-input").placeholder = t.placeholders.assistant;
  document.querySelector("#assistant-submit").textContent = t.buttons.ask;
  document.querySelector("#settings label").textContent = t.language;
}

function setupNavigation() {
  const buttons = document.querySelectorAll("nav button");
  const sections = document.querySelectorAll(".section");

  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      buttons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      sections.forEach(sec => sec.classList.remove("active"));
      document.getElementById(btn.dataset.section).classList.add("active");
    });
  });
}

function setupForm() {
  const form = document.getElementById("entry-form");
  form.addEventListener("submit", e => {
    e.preventDefault();
    alert(langData[currentLang].alerts.saved);
    form.reset();
  });

  document.getElementById("assistant-submit").addEventListener("click", () => {
    const input = document.getElementById("assistant-input").value;
    document.getElementById("assistant-response").textContent =
      input ? `"${input}" 🤖 (respuesta simulada)` : "";
  });
}

function setupLanguageSwitch() {
  document.getElementById("language-select").addEventListener("change", e => {
    loadLanguage(e.target.value);
  });
}
