/**
 * Registration Popup Logic
 * Triggered after loader completes + 4 second delay
 */

document.addEventListener('DOMContentLoaded', function () {
    console.log('🚀 Registration Popup Script Loaded');

    const popup = document.getElementById('newsletterPopup');
    if (!popup) {
        console.error('❌ Registration popup element not found!');
        return;
    }

    const closeBtn = popup.querySelector('.popup-close');
    const cancelBtn = document.getElementById('cancelSubscription');
    const form = document.getElementById('newsletterForm');

    // Wait for loader to finish, then show popup after 4 seconds
    function waitForLoaderThenShow() {
        const loader = document.getElementById('pageLoader');
        if (loader && !loader.classList.contains('hidden')) {
            // Loader still visible, check again in 500ms
            setTimeout(waitForLoaderThenShow, 500);
        } else {
            // Loader done — wait 4 seconds then show popup
            console.log('⏳ Loader complete. Registration popup in 4 seconds...');
            setTimeout(() => {
                showPopup();
            }, 4000);
        }
    }
    waitForLoaderThenShow();

    function showPopup() {
        console.log('✨ Showing Registration Popup');
        popup.style.display = 'flex';
        // Force reflow
        popup.offsetHeight;
        popup.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function hidePopup() {
        console.log('👋 Hiding Registration Popup');
        popup.classList.remove('active');
        document.body.style.overflow = '';
        setTimeout(() => {
            popup.style.display = 'none';
        }, 400);
    }

    if (closeBtn) closeBtn.addEventListener('click', hidePopup);
    if (cancelBtn) cancelBtn.addEventListener('click', hidePopup);

    // Handle outside click
    popup.addEventListener('click', function (e) {
        if (e.target === popup) {
            hidePopup();
        }
    });

    // Form submission
    if (form) {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();
            const name = document.getElementById('regName')?.value || '';
            const email = document.getElementById('regEmail')?.value || '';
            const phone = document.getElementById('regPhone')?.value || '';
            const course = document.getElementById('regCourse')?.value || '';

            console.log('📧 Registration submitted:', { name, email, phone, course });

            const submitBtn = form.querySelector('.btn-popup.primary');
            const originalText = submitBtn?.textContent || 'Register Now';

            if (name && email) {
                try {
                    if (submitBtn) {
                        submitBtn.textContent = 'Submitting...';
                        submitBtn.disabled = true;
                    }

                    const response = await fetch('/api/enroll/submit', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            name: name,
                            email: email,
                            phone: phone,
                            course: course,
                            message: 'Registered via popup form'
                        })
                    });

                    if (response.ok) {
                        // Show success state
                        const inner = popup.querySelector('.popup-inner');
                        inner.innerHTML = `
                            <div class="popup-header">
                                <div class="popup-icon">🎉</div>
                                <h2 class="popup-title">Welcome to Oriana!</h2>
                                <p class="popup-quote">Thank you, ${name}! We'll contact you shortly about the <strong>${course}</strong> program.</p>
                            </div>
                            <div style="margin-top: 24px;">
                                <button class="btn-popup primary" id="closeSuccess" style="width: 100%;">Awesome, Thanks!</button>
                            </div>
                        `;
                        const closeSuccess = document.getElementById('closeSuccess');
                        if (closeSuccess) closeSuccess.addEventListener('click', hidePopup);
                    } else {
                        throw new Error('Failed');
                    }
                } catch (err) {
                    console.error(err);
                    if (submitBtn) {
                        submitBtn.textContent = 'Try Again';
                        submitBtn.disabled = false;
                        setTimeout(() => {
                            submitBtn.textContent = originalText;
                        }, 3000);
                    }
                }
            }
        });
    }
});
