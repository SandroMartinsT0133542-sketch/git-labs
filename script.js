document.addEventListener("DOMContentLoaded", () => {
  const el = document.getElementById("status");
  if (el) {
    el.textContent += " (Script carregado com sucesso!)";
  }
});
