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
}

document.querySelectorAll("#language-switcher button").forEach((btn) => {
  btn.addEventListener("click", () => {
    loadLang(btn.dataset.lang);
  });
});

document.getElementById("ask-button").addEventListener("click", async () => {
  const question = document.getElementById("user-question").value.trim();
  const responseBox = document.getElementById("ai-response");
  responseBox.textContent = translations[currentLang]["loading_response"];

  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: question, lang: currentLang }),
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
