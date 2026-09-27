// 라이트/다크 테마 토글 (localStorage에 저장)
const root = document.documentElement;
const toggle = document.getElementById("theme-toggle");

const saved = localStorage.getItem("jobportal-theme");
if (saved) {
  root.setAttribute("data-theme", saved);
}
updateIcon();

toggle.addEventListener("click", () => {
  const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
  root.setAttribute("data-theme", next);
  localStorage.setItem("jobportal-theme", next);
  updateIcon();
});

function updateIcon() {
  toggle.textContent = root.getAttribute("data-theme") === "dark" ? "☀️" : "🌙";
}
