var loginModal = document.getElementById('loginModal');
var registerModal = document.getElementById('registerModal');

// ─── INJECT STYLES ──────────────────────────────────────────────────────────
(function injectStyles() {
    var style = document.createElement('style');
    style.textContent = `
        .field-error {
            color: #e53e3e;
            font-size: 12px;
            margin-top: 5px;
            display: block;
        }
        input.input-error,
        select.input-error {
            border: 1.5px solid #e53e3e !important;
            background: #fff5f5 !important;
        }
        .modal-error-banner {
            background: #fff5f5;
            border: 1.5px solid #e53e3e;
            color: #c53030;
            border-radius: 8px;
            padding: 10px 14px;
            font-size: 13px;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
            animation: fadeIn 0.3s ease;
        }
        .modal-error-banner::before {
            content: '✖';
            font-size: 13px;
            flex-shrink: 0;
        }
        .toast {
            position: fixed;
            top: 28px;
            left: 50%;
            transform: translateX(-50%) translateY(-16px);
            padding: 14px 32px;
            border-radius: 10px;
            font-size: 15px;
            font-weight: 600;
            z-index: 99999;
            opacity: 0;
            transition: opacity 0.35s ease, transform 0.35s ease;
            pointer-events: none;
            box-shadow: 0 8px 32px rgba(0,0,0,0.18);
            min-width: 280px;
            text-align: center;
            font-family: 'Poppins', sans-serif;
        }
        .toast.show {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
        .toast-success { background: #22c55e; color: #fff; }
        .toast-error   { background: #ef4444; color: #fff; }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-6px); }
            to   { opacity: 1; transform: translateY(0); }
        }
    `;
    document.head.appendChild(style);
})();

// ─── TOAST ──────────────────────────────────────────────────────────────────
function showToast(message, type, callback) {
    document.querySelectorAll('.toast').forEach(function(t) { t.remove(); });

    var toast = document.createElement('div');
    toast.className = 'toast toast-' + type;
    toast.textContent = message;
    document.body.appendChild(toast);

    requestAnimationFrame(function() {
        requestAnimationFrame(function() { toast.classList.add('show'); });
    });

    setTimeout(function() {
        toast.classList.remove('show');
        setTimeout(function() {
            toast.remove();
            if (callback) callback();
        }, 400);
    }, 2800);
}

// ─── FIELD ERROR HELPERS ────────────────────────────────────────────────────
function clearErrors(form) {
    form.querySelectorAll('.field-error').forEach(function(el) { el.remove(); });
    form.querySelectorAll('.input-error').forEach(function(el) { el.classList.remove('input-error'); });
    var banner = form.querySelector('.modal-error-banner');
    if (banner) banner.remove();
}

function showFieldError(input, message) {
    input.classList.add('input-error');
    var err = document.createElement('span');
    err.className = 'field-error';
    err.textContent = message;
    input.parentNode.appendChild(err);
}

// ─── PASSWORD VALIDATION ────────────────────────────────────────────────────
function validatePassword(value) {
    if (value.length < 6) {
        return 'Password must be at least 6 characters.';
    }
    if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?`~]/.test(value)) {
        return 'Password must include at least one special character (e.g. !, @, #).';
    }
    return null;
}

// ─── REGISTER FORM ──────────────────────────────────────────────────────────
var registerForm = document.querySelector('#registerModal form');
if (registerForm) {
    registerForm.addEventListener('submit', function(e) {
        e.preventDefault();
        clearErrors(registerForm);

        var passwordInput = registerForm.querySelector('[name="password"]');
        var confirmInput  = registerForm.querySelector('[name="confirmPassword"]');
        var hasError = false;

        // Password strength check
        var pwdError = validatePassword(passwordInput.value);
        if (pwdError) {
            showFieldError(passwordInput, pwdError);
            hasError = true;
        }

        // Passwords match check
        if (!hasError && passwordInput.value !== confirmInput.value) {
            showFieldError(confirmInput, 'Passwords do not match.');
            hasError = true;
        }

        if (hasError) return;

        // Submit via fetch — preserves all field values on error
        var formData = new FormData(registerForm);

        fetch('/register', {
            method: 'POST',
            body: formData
        })
        .then(function(res) { return res.json(); })
        .then(function(data) {
            if (data.success) {
                // Close modal, reset form, green toast, then open login
                registerModal.style.display = 'none';
                registerForm.reset();
                showToast('✓ ' + data.message, 'success', function() {
                    loginModal.style.display = 'block';
                });
            } else {
                // Red banner inside modal — all field values stay intact
                var banner = document.createElement('div');
                banner.className = 'modal-error-banner';
                banner.textContent = data.message;
                var firstGroup = registerForm.querySelector('.form-group');
                registerForm.insertBefore(banner, firstGroup);

                // Highlight the ID field
                var idInput = registerForm.querySelector('[name="idNumber"]');
                if (idInput) idInput.classList.add('input-error');
            }
        })
        .catch(function() {
            showToast('Something went wrong. Please try again.', 'error');
        });
    });
}

// ─── OPEN / CLOSE MODALS ────────────────────────────────────────────────────
document.getElementById('loginBtn').onclick = function() {
    loginModal.style.display = 'block';
};

document.getElementById('registerBtn').onclick = function() {
    registerModal.style.display = 'block';
};

document.getElementById('closeLoginModal').onclick = function() {
    loginModal.style.display = 'none';
    document.querySelector('#loginModal form').reset();
};

document.getElementById('closeModal').onclick = function() {
    registerModal.style.display = 'none';
};

document.getElementById('switchToRegister').onclick = function() {
    loginModal.style.display = 'none';
    document.querySelector('#loginModal form').reset();
    registerModal.style.display = 'block';
};

document.getElementById('switchToLogin').onclick = function() {
    registerModal.style.display = 'none';
    loginModal.style.display = 'block';
};

window.onclick = function(e) {
    if (e.target == loginModal) {
        loginModal.style.display = 'none';
        document.querySelector('#loginModal form').reset();
    }
    if (e.target == registerModal) registerModal.style.display = 'none';
};

document.onkeydown = function(e) {
    if (e.key === 'Escape') {
        loginModal.style.display = 'none';
        document.querySelector('#loginModal form').reset();
        registerModal.style.display = 'none';
    }
};

// ─── FLASK LOGIN ERROR → open login modal ───────────────────────────────────
(function handleLoginError() {
    // Flask still uses redirect+session for login errors, so check for flash msg
    var flashMsg = document.getElementById('flashMsg');
    if (flashMsg) {
        var text = flashMsg.textContent || '';
        if (text.toLowerCase().includes('wrong') || text.toLowerCase().includes('invalid')) {
            loginModal.style.display = 'block';
        }
        setTimeout(function() { flashMsg.style.display = 'none'; }, 3000);
    }
})();

// ─── SCROLL REVEAL ───────────────────────────────────────────────────────────
(function initReveal() {
    var reveals = document.querySelectorAll('.reveal');
    if (!reveals.length) return;

    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) entry.target.classList.add('visible');
        });
    }, { threshold: 0.08 });

    reveals.forEach(function(el) { observer.observe(el); });
})();