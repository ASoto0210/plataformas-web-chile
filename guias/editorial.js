document.querySelectorAll('[data-print]').forEach(button => button.addEventListener('click', () => window.print()));
const calculator = document.querySelector('[data-calculator]');
if (calculator) {
  const update = () => {
    const read = name => Number(calculator.elements[name].value);
    const fields = ['initial', 'monthly', 'sales', 'rate', 'fixed', 'orders', 'months'];
    const valid = fields.every(name => calculator.elements[name].checkValidity() && calculator.elements[name].value !== '' && Number.isFinite(read(name)));
    const output = calculator.querySelector('output');
    if (!valid) { output.textContent = 'Completa los campos con valores válidos.'; return; }
    const total = read('initial') + read('months') * (read('monthly') + read('sales') * read('rate') / 100 + read('fixed') * read('orders'));
    output.textContent = new Intl.NumberFormat('es-CL', {style: 'currency', currency: 'CLP', maximumFractionDigits: 0}).format(total);
  };
  calculator.addEventListener('input', update);
  calculator.addEventListener('submit', event => event.preventDefault());
  update();
}
