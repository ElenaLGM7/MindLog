async function loadLanguage(lang) {
  const res = await fetch(`static/js/lang/${lang}.json`);
  const translations = await res.json();

  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (translations[key]) {
      el.textContent = translations[key];
    }
  });

  // Opciones de los <select>
  document.querySelectorAll("option[data-i18n]").forEach(opt => {
    const key = opt.getAttribute("data-i18n");
    if (translations[key]) {
      opt.textContent = translations[key];
    }
  });

  document.title = translations["title"];
}

document.getElementById("language-selector").addEventListener("change", e => {
  const lang = e.target.value;
  localStorage.setItem("language", lang);
  loadLanguage(lang);
});

document.addEventListener("DOMContentLoaded", () => {
  const lang = localStorage.getItem("language") || "es";
  document.getElementById("language-selector").value = lang;
  loadLanguage(lang);
});
