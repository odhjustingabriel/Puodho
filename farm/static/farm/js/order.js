document.addEventListener('DOMContentLoaded', () => {
  const steps = [...document.querySelectorAll('.assistant-step')];
  const log = document.getElementById('chat-log');
  const productInputs = [...document.querySelectorAll('input[name="selected_products"]')];
  const broilerFields = document.querySelector('.broiler-fields');
  const eggFields = document.querySelector('.egg-fields');
  const preferredDate = document.querySelector('input[name="preferred_date"]');
  let current = 0;
  const prompts = [
    'Great. How can Puodho contact you?',
    'Where are you located and do you prefer pickup or delivery?',
    'What would you like to order today?',
    'Add the quantities and options for your selected produce.',
    'Choose your preferred date and add any notes.',
    'Ready to send your order request to Puodho.'
  ];

  function addBubble(text, cls = 'farm') {
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
    const selected = productInputs.filter(input => input.checked).map(input => input.value);
    if (broilerFields) broilerFields.style.display = selected.includes('broiler-chicken') ? 'grid' : 'none';
    if (eggFields) eggFields.style.display = selected.includes('eggs') ? 'grid' : 'none';
  }

  function setMinimumPreferredDate() {
    if (!preferredDate) return;
    const today = new Date();
    const timezoneOffset = today.getTimezoneOffset() * 60000;
    const localToday = new Date(today.getTime() - timezoneOffset).toISOString().split('T')[0];
    preferredDate.min = preferredDate.min || localToday;
  }

  function firstInvalidField(step) {
    const fields = [...step.querySelectorAll('input:not([type="hidden"]), select, textarea')];
    return fields.find(field => {
      if (field.type === 'radio' || field.type === 'checkbox') {
        return field.required && !step.querySelector(`input[name="${field.name}"]:checked`);
      }
      return field.required && !field.value;
    });
  }

  document.querySelectorAll('.next-step').forEach(button => button.addEventListener('click', () => {
    const active = steps[current];
    const invalid = firstInvalidField(active);
    if (invalid) {
      invalid.focus();
      addBubble('Please complete this step before moving on.');
      return;
    }
    addBubble('Done', 'customer');
    current = Math.min(current + 1, steps.length - 1);
    showStep(current);
    addBubble(prompts[current - 1] || prompts[0]);
  }));

  productInputs.forEach(input => input.addEventListener('change', updateProductFields));
  setMinimumPreferredDate();

  const firstErrorStep = steps.findIndex(step => step.querySelector('.field-error, .form-errors'));
  if (firstErrorStep >= 0) {
    current = firstErrorStep;
    addBubble('Please correct the highlighted field, then continue.');
  }
  showStep(current);
});
