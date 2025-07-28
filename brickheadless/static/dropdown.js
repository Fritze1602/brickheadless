export function initDropdowns() {
  document.querySelectorAll('[data-dropdown]').forEach((el) => {
    const trigger = el.querySelector('[data-trigger]');
    const menu = el.querySelector('[data-menu]');
    if (!trigger || !menu) return;

    trigger.addEventListener('click', () => {
      const open = menu.getAttribute('data-open') === 'true';
      menu.setAttribute('data-open', String(!open));
      menu.hidden = open; // toggle visibility
    });
  });
}