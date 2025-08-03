let currentLang = localStorage.getItem("lang") || "es";
let translations = {};

async function loadLang(lang) {
  const res = await fetch("lang.json");
  translations = await res.json();
  currentLang = lang;
  localStorage.setItem("lang", lang);
  applyTranslations();
}

function applyTranslations() {
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    if (translations[currentLang] && translations[currentLang][key]) {
      el.textContent = translations[currentLang][key];
    }
  });

  const question = document.getElementById("user-question");
  question.placeholder = translations[currentLang]["assistant_placeholder"];

  // Opciones de selector
  const modeSelect = document.getElementById("ai-mode");
  if (modeSelect) {
    modeSelect.options[0].textContent = translations[currentLang]["mode_psychologist"];
    modeSelect.options[1].textContent = translations[currentLang]["mode_coach"];
    modeSelect.options[2].textContent = translations[currentLang]["mode_friend"];
  }
}

document.querySelectorAll("#language-switcher button").forEach((btn) => {
  btn.addEventListener("click", () => {
    loadLang(btn.dataset.lang);
  });
});

document.getElementById("ask-button").addEventListener("click", async () => {
  const question = document.getElementById("user-question").value.trim();
  const mode = document.getElementById("ai-mode").value;
  const responseBox = document.getElementById("ai-response");
  responseBox.textContent = translations[currentLang]["loading_response"];

  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message: question,
      lang: currentLang,
      mode: mode
    }),
  });

  if (res.ok) {
    const data = await res.json();
    responseBox.textContent = data.reply;
  } else {
    responseBox.textContent = translations[currentLang]["error_response"];
  }
});

// Inicializa traducciones
loadLang(currentLang);
