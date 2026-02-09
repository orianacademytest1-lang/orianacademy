// Authentication State Handler
(function () {
    'use strict';

    function updateAuthLinks() {
        const user = localStorage.getItem('user');
        const authLinks = document.querySelectorAll('.login-link, .login-btn');

        console.log('Auth state check:', user ? 'User logged in' : 'No user');

        authLinks.forEach(link => {
            if (user && user !== 'null') {
                // User is logged in - show Sign Out
                link.textContent = 'Sign Out';
                link.href = '#';
                link.classList.add('logout-link');

                // Handle logout click
                link.onclick = function (e) {
                    e.preventDefault();
                    console.log('Logging out...');
                    localStorage.removeItem('user');
                    window.location.href = 'index.html';
                };
            } else {
                // No user - show Sign In
                link.textContent = 'Sign In';
                link.href = 'login.html';
                link.classList.remove('logout-link');
                link.onclick = null;
            }
        });
    }

    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', updateAuthLinks);
    } else {
        updateAuthLinks();
    }
})();
