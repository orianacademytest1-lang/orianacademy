// Main Script for Oriana Academy Workshop Page
document.addEventListener('DOMContentLoaded', () => {
    // Header Scroll Effect
    const header = document.querySelector('header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Smooth Scrolling for Nav Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Form Handling
    const workshopForm = document.getElementById('workshopForm');
    if (workshopForm) {
        workshopForm.addEventListener('submit', (e) => {
            e.preventDefault();

            // Basic validation
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;

            if (name && email) {
                // Simulate submission
                const submitBtn = workshopForm.querySelector('button');
                const originalText = submitBtn.innerText;

                submitBtn.disabled = true;
                submitBtn.innerText = 'Registering...';

                // Get status from radio buttons
                const status = workshopForm.querySelector('input[name="status"]:checked')?.value || 'career-break';
                const phone = document.getElementById('phone').value;

                fetch('/api/workshop/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        workshop_id: 1, // Default to Women's Day Special
                        name: name,
                        email: email,
                        phone: phone,
                        status: status
                    })
                })
                    .then(response => response.json())
                    .then(data => {
                        alert(`Thank you, ${name}! Your seat for the Women's Day Workshop has been reserved.`);
                        workshopForm.reset();
                        submitBtn.disabled = false;
                        submitBtn.innerText = originalText;
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('Registration failed. Please try again later.');
                        submitBtn.disabled = false;
                        submitBtn.innerText = originalText;
                    });
            }
        });
    }

    // Scroll Reveal Animation (Simple Implementation)
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal');
            }
        });
    }, observerOptions);

    // Apply reveal class to sections
    document.querySelectorAll('section').forEach(section => {
        section.style.opacity = "0";
        section.style.transform = "translateY(30px)";
        section.style.transition = "all 0.8s ease-out";
        observer.observe(section);
    });

    // Custom Observer Handler
    const revealOnScroll = () => {
        document.querySelectorAll('section').forEach(section => {
            if (section.classList.contains('reveal')) {
                section.style.opacity = "1";
                section.style.transform = "translateY(0)";
            }
        });
    };

    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll(); // Initial check

    // Registration Popup Logic
    const popup = document.getElementById('newsletterPopup');
    const closeBtn = document.getElementById('popupClose');
    const cancelBtn = document.getElementById('cancelSubscription');

    if (popup) {
        // Show popup after 5 seconds
        setTimeout(() => {
            popup.classList.add('active');
        }, 5000);

        // Close popup
        const closePopup = () => {
            popup.classList.remove('active');
        };

        if (closeBtn) closeBtn.addEventListener('click', closePopup);
        if (cancelBtn) cancelBtn.addEventListener('click', closePopup);

        // Close on clicking outside
        popup.addEventListener('click', (e) => {
            if (e.target === popup) closePopup();
        });

        // Popup Form Handling
        const popupForm = document.getElementById('newsletterForm');
        if (popupForm) {
            popupForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const name = document.getElementById('regName').value;
                const email = document.getElementById('regEmail').value;
                const submitBtn = popupForm.querySelector('button');

                if (name && email) {
                    const originalText = submitBtn.innerText;
                    submitBtn.disabled = true;
                    submitBtn.innerText = 'Registering...';

                    const phone = document.getElementById('regPhone').value;
                    const status = popupForm.querySelector('input[name="popup-status"]:checked')?.value || 'career-break';

                    fetch('/api/workshop/register', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            workshop_id: 1, // Default to Women's Day Special
                            name: name,
                            email: email,
                            phone: phone,
                            status: status
                        })
                    })
                        .then(response => response.json())
                        .then(data => {
                            alert(`Thank you, ${name}! Your seat for the Women's Day Workshop has been reserved.`);
                            popupForm.reset();
                            submitBtn.disabled = false;
                            submitBtn.innerText = originalText;
                            closePopup();
                        })
                        .catch(error => {
                            console.error('Error:', error);
                            alert('Registration failed. Please try again later.');
                            submitBtn.disabled = false;
                            submitBtn.innerText = originalText;
                        });
                }
            });
        }
    }

    // Official Newsletter Form
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const emailInput = newsletterForm.querySelector('input');
            const email = emailInput.value;
            alert(`Thanks for subscribing! We'll send updates to ${email}`);
            newsletterForm.reset();
        });
    }
});
