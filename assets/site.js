if (location.protocol === 'file:') {
  document.querySelectorAll('a[href^="blogs/"][href$="/"], a[href^="../blogs/"][href$="/"], a[data-local-index]').forEach((link) => {
    link.href += 'index.html';
  });
}
const languageButtons = document.querySelectorAll(".language-switch button");
const translatedLabels = document.querySelectorAll("[data-english][data-singlish]");
const themeToggle = document.querySelector(".theme-toggle");
const showMoreButtons = document.querySelectorAll(".show-more-button");
const copyPrimerCitation = document.getElementById('copy-primer-citation');
if (copyPrimerCitation) {
  copyPrimerCitation.addEventListener('click', async () => {
    const citation = document.querySelector('#primer-bibtex code');
    if (!citation) return;
    try {
      if (navigator.clipboard?.writeText) {
        try {
          await navigator.clipboard.writeText(citation.textContent);
        } catch {
          if (!copySelectedCitation()) throw new Error('Copy unavailable');
        }
      } else if (!copySelectedCitation()) {
        throw new Error('Copy unavailable');
      }
      copyPrimerCitation.textContent = 'Copied';
      setTimeout(() => { copyPrimerCitation.textContent = 'Copy'; }, 2000);
    } catch {
      copyPrimerCitation.textContent = 'Select text to copy';
    }
    function copySelectedCitation() {
      try {
        const selection = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(citation);
        selection.removeAllRanges();
        selection.addRange(range);
        const copied = document.execCommand('copy');
        selection.removeAllRanges();
        return copied;
      } catch {
        return false;
      }
    }
  });
}
const solutionToggle = document.getElementById('toggle-solutions');
if (solutionToggle) {
  const solutions = Array.from(document.querySelectorAll('#tutorial-panel .tutorial-solution'));
  function updateSolutionToggle() {
    const allOpen = solutions.every((solution) => solution.open);
    solutionToggle.textContent = allOpen ? 'Collapse all solutions' : 'Expand all solutions';
    solutionToggle.setAttribute('aria-expanded', String(allOpen));
  }
  solutionToggle.addEventListener('click', () => {
    const open = !solutions.every((solution) => solution.open);
    solutions.forEach((solution) => { solution.open = open; });
    updateSolutionToggle();
  });
  solutions.forEach((solution) => {
    solution.addEventListener('toggle', () => {
      updateSolutionToggle();
    });
  });
}

document.querySelectorAll('.tutorial-solution').forEach((detail) => {
  detail.addEventListener('toggle', () => {
    if (detail.open && window.MathJax?.typesetPromise) {
      window.MathJax.typesetPromise([detail]).catch(() => {});
    }
  });
});

document.querySelectorAll('.notebook-tabs').forEach((tablist) => {
  const tabs = Array.from(tablist.querySelectorAll('[role="tab"]'));
  function selectTab(selected) {
    tabs.forEach((tab) => {
      const active = tab === selected;
      tab.setAttribute('aria-selected', String(active));
      tab.tabIndex = active ? 0 : -1;
      document.getElementById(tab.getAttribute('aria-controls')).hidden = !active;
    });
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => selectTab(tab));
    tab.addEventListener('keydown', (event) => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next === undefined) return;
      event.preventDefault();
      selectTab(tabs[next]);
      tabs[next].focus();
    });
  });
  document.querySelectorAll('[data-open-tutorial]').forEach((link) => {
    link.addEventListener('click', (event) => {
      const tutorialTab = tablist.querySelector('#tutorial-tab');
      if (!tutorialTab) return;
      event.preventDefault();
      selectTab(tutorialTab);
      tutorialTab.focus();
      tutorialTab.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });
});

function setLanguage(language) {
  translatedLabels.forEach((element) => {
    element.textContent = element.dataset[language];
  });

  languageButtons.forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.language === language));
  });

  document.documentElement.lang = language === "singlish" ? "en-SG" : "en";
  try { localStorage.setItem("language", language); } catch {}
}

languageButtons.forEach((button) => {
  button.addEventListener("click", () => setLanguage(button.dataset.language));
});

function setTheme(theme) {
  document.documentElement.dataset.theme = theme;
  themeToggle.checked = theme === "dark";
  try { localStorage.setItem("theme", theme); } catch {}
}

if (themeToggle) {
  themeToggle.checked = document.documentElement.dataset.theme === "dark";
  themeToggle.addEventListener("change", () => setTheme(themeToggle.checked ? "dark" : "light"));
}

let savedLanguage = "english";
try { savedLanguage = localStorage.getItem("language") || "english"; } catch {}
setLanguage(savedLanguage === "singlish" ? "singlish" : "english");

showMoreButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const controlledElements = button.getAttribute("aria-controls")
      .split(/\s+/)
      .map((id) => document.getElementById(id))
      .filter(Boolean);
    if (!controlledElements.length) return;

    const expanded = button.getAttribute("aria-expanded") === "true";
    button.setAttribute("aria-expanded", String(!expanded));
    controlledElements.forEach((element) => { element.hidden = expanded; });
    button.querySelector("span:first-child").textContent = expanded ? "Show more" : "Show less";
    button.querySelector(".show-more-icon").textContent = expanded ? "→" : "↑";
  });
});
