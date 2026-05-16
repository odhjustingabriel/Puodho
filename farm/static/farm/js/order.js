document.addEventListener('DOMContentLoaded', () => {
  const steps = [...document.querySelectorAll('.assistant-step')];
  const log = document.getElementById('chat-log');
  const productInputs = [...document.querySelectorAll('input[name="selected_products"]')];
  const broilerFields = document.querySelector('.broiler-fields');
  const eggFields = document.querySelector('.egg-fields');
  let current = 0;
  const prompts = [
    'Great. How can Puodho contact you?',
    'Where are you located and do you prefer pickup or delivery?',
    'What would you like to order today?',
    'Add the quantities and options for your selected produce.',
    'Choose your preferred date and add any notes.',
    'Ready to send your order request to Puodho.'
  ];
  function addBubble(text, cls='farm') {
    const bubble = document.createElement('div');
    bubble.className = `bubble ${cls}`;
    bubble.textContent = text;
    log.appendChild(bubble);
    log.scrollTop = log.scrollHeight;
  }
  function showStep(index) {
    steps.forEach((step, i) => step.classList.toggle('active', i === index));
    updateProductFields();
  }
  function updateProductFields() {
    const selected = productInputs.filter(i => i.checked).map(i => i.value);
    if (broilerFields) broilerFields.style.display = selected.includes('broiler-chicken') ? 'grid' : 'none';
    if (eggFields) eggFields.style.display = selected.includes('eggs') ? 'grid' : 'none';
  }
  document.querySelectorAll('.next-step').forEach(button => button.addEventListener('click', () => {
    const active = steps[current];
    const fields = [...active.querySelectorAll('input:not([type="hidden"]), select, textarea')];
    const first = fields.find(field => field.required && !field.value);
    if (first) { first.focus(); addBubble('Please complete this required field before moving on.'); return; }
    addBubble('Done', 'customer');
    current = Math.min(current + 1, steps.length - 1);
    showStep(current);
    addBubble(prompts[current - 1] || prompts[0]);
  }));
  productInputs.forEach(input => input.addEventListener('change', updateProductFields));
  showStep(current);
});
