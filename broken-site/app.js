// Basic interaction logic for the demo site
document.addEventListener('DOMContentLoaded', () => {
  const regForm = document.getElementById('registerForm');
  const regMsg = document.getElementById('registerMessage');
  const regBtn = document.getElementById('registerSubmit');

  const loginForm = document.getElementById('loginForm');
  const loginMsg = document.getElementById('loginMessage');

  // Registration handler: simple checks (note: intentionally permissive email check)
  if (regBtn) {
    regBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const email = document.getElementById('regEmail').value.trim();
      const pass = document.getElementById('regPassword').value;

      // Accepts any value containing '@' (intentionally permissive)
      if (!email.includes('@')) {
        regMsg.textContent = 'Please enter a valid email address.';
        return;
      }

      if (!pass || pass.length < 6) {
        // Confusing generic message shown to user
        regMsg.textContent = 'An unexpected error occurred. Please try again later.';
        return;
      }

      // Submit using form.submit() which bypasses native constraint validation
      regForm.submit();
    });
  }

  // Login: handler attachment uses the wrong id (so login will not function correctly)
  const wrongLoginButton = document.getElementById('login-button');
  if (wrongLoginButton) {
    wrongLoginButton.addEventListener('click', (e) => {
      e.preventDefault();
      // Placeholder: would check credentials
      loginMsg.textContent = 'Signing in...';
    });
  }

  // Minimal behavior for the primary CTA
  const cta = document.querySelector('.cta');
  if (cta) cta.addEventListener('click', () => alert('Primary action clicked'));
});
