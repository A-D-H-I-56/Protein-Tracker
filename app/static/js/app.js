// Theme & Navigation Logic
document.addEventListener('DOMContentLoaded', () => {
  // Theme Toggle
  const themeToggle = document.getElementById('themeToggle');
  const savedTheme = localStorage.getItem('theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeIcon(savedTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
      updateThemeIcon(newTheme);
    });
  }

  function updateThemeIcon(theme) {
    if (!themeToggle) return;
    themeToggle.innerHTML = theme === 'dark' ? '☀️' : '🌙';
  }

  // Mobile Navigation Hamburger Toggle
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const navMenu = document.getElementById('navMenu');

  if (mobileMenuBtn && navMenu) {
    mobileMenuBtn.addEventListener('click', () => {
      const isExpanded = mobileMenuBtn.getAttribute('aria-expanded') === 'true';
      mobileMenuBtn.setAttribute('aria-expanded', !isExpanded);
      mobileMenuBtn.classList.toggle('open');
      navMenu.classList.toggle('open');
    });

    // Close menu when clicking outside or clicking any nav link
    document.addEventListener('click', (e) => {
      if (!navMenu.contains(e.target) && !mobileMenuBtn.contains(e.target) && navMenu.classList.contains('open')) {
        navMenu.classList.remove('open');
        mobileMenuBtn.classList.remove('open');
        mobileMenuBtn.setAttribute('aria-expanded', 'false');
      }
    });

    navMenu.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('open');
        mobileMenuBtn.classList.remove('open');
        mobileMenuBtn.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Form Submit Loading Feedback
  const calcForm = document.querySelector('form[action*="calculate"]');
  if (calcForm) {
    calcForm.addEventListener('submit', (e) => {
      const submitBtn = calcForm.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.innerHTML = '<span>⏳ Computing AI Recommendation...</span>';
        submitBtn.style.opacity = '0.85';
        submitBtn.style.pointerEvents = 'none';
      }
    });
  }

  // Live Biometric Calculator
  const ageInput = document.getElementById('age');
  const genderInput = document.getElementById('gender');
  const weightInput = document.getElementById('weight');
  const heightInput = document.getElementById('height');
  const activityInput = document.getElementById('activity_level');

  function updateLiveBioMetrics() {
    const age = parseFloat(ageInput?.value) || 0;
    const gender = genderInput?.value || 'Male';
    const weight = parseFloat(weightInput?.value) || 0;
    const height = parseFloat(heightInput?.value) || 0;
    const activity = activityInput?.value || 'Sedentary';

    const bmiEl = document.getElementById('previewBmi');
    const bmrEl = document.getElementById('previewBmr');
    const tdeeEl = document.getElementById('previewTdee');

    if (weight > 0 && height > 0) {
      const heightM = height / 100.0;
      const bmi = (weight / (heightM * heightM)).toFixed(1);
      if (bmiEl) bmiEl.innerText = bmi;

      if (age > 0) {
        let bmr = (10 * weight) + (6.25 * height) - (5 * age);
        bmr = gender === 'Male' ? bmr + 5 : bmr - 161;
        if (bmrEl) bmrEl.innerText = Math.round(bmr).toLocaleString() + ' kcal';

        const multipliers = {
          'Sedentary': 1.2,
          'Light Active': 1.375,
          'Active': 1.55,
          'Very Active': 1.725
        };
        const mult = multipliers[activity] || 1.2;
        const tdee = Math.round(bmr * mult);
        if (tdeeEl) tdeeEl.innerText = Math.round(tdee).toLocaleString() + ' kcal';
      }
    }
  }

  [ageInput, genderInput, weightInput, heightInput, activityInput].forEach(el => {
    if (el) el.addEventListener('input', updateLiveBioMetrics);
  });

  // Preset Buttons
  const presets = {
    'male-muscle': { age: 25, gender: 'Male', weight: 75, height: 178, activity_level: 'Very Active', goal: 'Muscle Gain' },
    'female-loss': { age: 29, gender: 'Female', weight: 68, height: 165, activity_level: 'Light Active', goal: 'Weight Loss' },
    'active-male': { age: 34, gender: 'Male', weight: 82, height: 180, activity_level: 'Active', goal: 'Maintenance' },
    'female-tone': { age: 26, gender: 'Female', weight: 58, height: 168, activity_level: 'Active', goal: 'Muscle Gain' }
  };

  document.querySelectorAll('.preset-chip').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const key = btn.getAttribute('data-preset');
      const data = presets[key];
      if (!data) return;

      if (ageInput) ageInput.value = data.age;
      if (genderInput) genderInput.value = data.gender;
      if (weightInput) weightInput.value = data.weight;
      if (heightInput) heightInput.value = data.height;
      if (activityInput) activityInput.value = data.activity_level;

      const goalInput = document.getElementById('goal');
      if (goalInput) goalInput.value = data.goal;

      updateLiveBioMetrics();
    });
  });

  // Initial calculation on page load
  updateLiveBioMetrics();
});
