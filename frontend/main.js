let currentLang = localStorage.getItem("lang") || "es";
let langData = {};
const emotions = ["😊", "😢", "😡", "😨", "😍", "😐", "🥲", "😎", "🤯"];

async function loadLang() {
  const res = await fetch("lang.json");
  langData = await res.json();
  applyLang();
}

function applyLang() {
  document.getElementById("app-title").textContent = langData[currentLang].title;
  document.querySelectorAll("[data-translate]").forEach(el => {
    el.textContent = langData[currentLang][el.dataset.translate];
  });
  document.getElementById("entry-text").placeholder = langData[currentLang].entry_placeholder;
  document.getElementById("ai-question").placeholder = langData[currentLang].ai_placeholder;
  renderEmotions();
}

function renderEmotions() {
  const container = document.getElementById("emotions-container");
  container.innerHTML = "";
  emotions.forEach(emoji => {
    const label = document.createElement("label");
    label.innerHTML = `<input type="checkbox" name="emotions" value="${emoji}"/> ${emoji}`;
    container.appendChild(label);
  });
}

function changeSection(sectionId) {
  document.querySelectorAll("main section").forEach(s => s.classList.remove("active"));
  document.getElementById(sectionId).classList.add("active");
}

document.querySelectorAll("nav button").forEach(btn => {
  btn.addEventListener("click", () => changeSection(btn.dataset.section));
});

document.getElementById("language-select").addEventListener("change", e => {
  currentLang = e.target.value;
  localStorage.setItem("lang", currentLang);
  applyLang();
});

document.getElementById("entry-form").addEventListener("submit", e => {
  e.preventDefault();
  const text = document.getElementById("entry-text").value;
  const selected = Array.from(document.querySelectorAll('input[name="emotions"]:checked'))
    .map(e => e.value);
  const entry = { text, emotions: selected, date: new Date().toISOString() };
  const history = JSON.parse(localStorage.getItem("mindlog") || "[]");
  history.unshift(entry);
  localStorage.setItem("mindlog", JSON.stringify(history));
  e.target.reset();
  renderHistory();
  changeSection("history");
});

function renderHistory() {
  const list = document.getElementById("history-list");
  const entries = JSON.parse(localStorage.getItem("mindlog") || "[]");
  list.innerHTML = entries.map(e => `<li>${e.date.split("T")[0]} - ${e.emotions.join(" ")}<br>${e.text}</li>`).join("");
}

document.getElementById("clear-data").addEventListener("click", () => {
  if (confirm(langData[currentLang].confirm_clear)) {
    localStorage.removeItem("mindlog");
    renderHistory();
  }
});

document.getElementById("ask-ai").addEventListener("click", () => {
  const input = document.getElementById("ai-question").value.trim();
  const output = document.getElementById("ai-response");
  if (input) {
    output.textContent = "🤖 " + langData[currentLang].ai_dummy;
  }
});

loadLang();
renderHistory();
