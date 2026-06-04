function navigate(screenFile) { window.location.href = screenFile; }
function initNav() {
  const path = window.location.pathname.split('/').pop();
  document.querySelectorAll('.nav-item[data-screen]').forEach(function (el) {
    if (el.getAttribute('data-screen') === path) el.classList.add('active');
  });
}
function openModal(id) { var m = document.getElementById(id); if (m) m.style.display = 'flex'; }
function closeModal(id) { var m = document.getElementById(id); if (m) m.style.display = 'none'; }
document.addEventListener('DOMContentLoaded', initNav);
