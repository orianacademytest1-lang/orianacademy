// ============================================
// ORIANA ACADEMY - ENHANCED JAVASCRIPT
// Dynamic Animations & Interactions
// ============================================

document.addEventListener('DOMContentLoaded', function () {
  console.log('Oriana Academy: DOM Content Loaded. Script initializing...');

  // ============================================
  // MOTIVATIONAL QUOTE POPUP LOGIC (Trigger Early)
  // ============================================
  const quotes = [
    { text: "The best way to predict the future is to create it.", author: "Peter Drucker" },
    { text: "Your career is your business. It's time for you to manage it.", author: "Dorit Sher" },
    { text: "Learning is the only thing the mind never exhausts.", author: "Leonardo da Vinci" },
    { text: "The only way to do great work is to love what you do.", author: "Steve Jobs" },
    { text: "Innovation distinguishes between a leader and a follower.", author: "Steve Jobs" },
    { text: "Direct your passion toward your career success.", author: "Oriana Academy" },
    { text: "Master the skills that the future demands today.", author: "Oriana Academy" }
  ];

  function showQuotePopup() {
    console.warn('Oriana Academy: Attempting to show Quote Popup...');
    const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
    const popup = document.createElement('div');
    popup.className = 'quote-popup';

    const isInCourseFolder = window.location.pathname.includes('/courses/');
    const contactPath = isInCourseFolder ? '../contact.html' : 'contact.html';

    popup.innerHTML = `
      <div class="quote-close" aria-label="Close">&times;</div>
      <div class="quote-content">
        <p class="quote-text">"${randomQuote.text}"</p>
        <p class="quote-author">— ${randomQuote.author}</p>
      </div>
    `;

    document.body.appendChild(popup);

    setTimeout(() => {
      popup.classList.add('active');
      console.log('Oriana Academy: Motivational Popup should now be visible.');
    }, 100);

    popup.addEventListener('click', (e) => {
      if (!e.target.classList.contains('quote-close')) {
        window.location.href = contactPath;
      }
    });

    popup.querySelector('.quote-close').addEventListener('click', (e) => {
      e.stopPropagation();
      popup.classList.remove('active');
      setTimeout(() => popup.remove(), 600);
    });
  }

  console.log('Oriana Academy: Popup scheduled for 4s delay');
  setTimeout(showQuotePopup, 4000);


  // ============================================
  // PAGE LOADER (Resilient Hiding)
  // ============================================
  const pageLoader = document.getElementById('pageLoader');

  if (pageLoader) {
    const hideLoader = () => {
      setTimeout(() => {
        pageLoader.classList.add('hidden');
        console.log('Oriana Academy: Page Loader hidden.');
      }, 300);
    };

    if (document.readyState === 'complete') {
      hideLoader();
    } else {
      window.addEventListener('load', hideLoader);
      // Fallback: Force hide after 1.5s as script is already at bottom
      setTimeout(hideLoader, 1500);
    }
  }

  // ============================================
  // HEADER SCROLL EFFECT
  // ============================================
  const header = document.getElementById('header');

  if (header) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 50) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    });
  }

  // ============================================
  // MOBILE MENU TOGGLE
  // ============================================
  const mobileToggle = document.getElementById('mobileToggle');
  const navMenu = document.getElementById('navMenu');

  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', function () {
      this.classList.toggle('active');
      navMenu.classList.toggle('active');
      document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
    });

    // Close menu when clicking a link
    navMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', function () {
        mobileToggle.classList.remove('active');
        navMenu.classList.remove('active');
        document.body.style.overflow = '';
      });
    });

    // Close menu when clicking outside
    document.addEventListener('click', function (e) {
      if (!navMenu.contains(e.target) && !mobileToggle.contains(e.target)) {
        mobileToggle.classList.remove('active');
        navMenu.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
  }

  // ============================================
  // SMOOTH SCROLL
  // ============================================
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');

      if (targetId !== '#' && targetId.length > 1) {
        const target = document.querySelector(targetId);

        if (target) {
          e.preventDefault();
          const headerHeight = header ? header.offsetHeight : 80;
          const targetPosition = target.offsetTop - headerHeight - 20;

          window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
          });
        }
      }
    });
  });

  // ============================================
  // SCROLL REVEAL ANIMATIONS
  // ============================================
  const revealElements = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');

  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  });

  revealElements.forEach(el => revealObserver.observe(el));

  // ============================================
  // COUNTER ANIMATION
  // ============================================
  const counters = document.querySelectorAll('.stat-number[data-count]');

  const animateCounter = (counter) => {
    const target = parseInt(counter.getAttribute('data-count'));
    const duration = 2000;
    const startTime = performance.now();

    // Get the original suffix ONCE before animation starts
    // This prevents the "-" bug when the textContent changes during animation
    const originalText = counter.textContent;
    const suffix = originalText.replace(/[0-9,.-]/g, '').trim() || '+';

    // Mark as animated to prevent re-animation
    if (counter.dataset.animated === 'true') return;
    counter.dataset.animated = 'true';

    const updateCounter = (currentTime) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);

      // Easing function
      const easeOutQuart = 1 - Math.pow(1 - progress, 4);
      const current = Math.floor(easeOutQuart * target);

      // Format number with commas
      let displayValue = current.toLocaleString();
      counter.textContent = displayValue + suffix;

      if (progress < 1) {
        requestAnimationFrame(updateCounter);
      }
    };

    requestAnimationFrame(updateCounter);
  };

  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        counterObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(counter => counterObserver.observe(counter));

  // ============================================
  // PARALLAX EFFECT (Subtle)
  // ============================================
  const heroFloats = document.querySelectorAll('.hero-float-1, .hero-float-2, .hero-float-3');

  if (heroFloats.length > 0) {
    window.addEventListener('scroll', () => {
      const scrolled = window.pageYOffset;

      heroFloats.forEach((el, index) => {
        const speed = 0.1 + (index * 0.05);
        el.style.transform = `translateY(${scrolled * speed}px) rotate(${scrolled * 0.02}deg)`;
      });
    });
  }

  // ============================================
  // FORM INPUT ERROR CLEARING (Helper only - no submit handling)
  // Each form has its own submit handler in its respective page
  // ============================================
  document.querySelectorAll('form input, form select, form textarea').forEach(input => {
    input.addEventListener('input', function () {
      this.style.borderColor = '';
      const error = this.parentElement.querySelector('.error-message');
      if (error) error.remove();
    });
  });



  // ============================================
  // CARD TILT EFFECT
  // ============================================
  const tiltCards = document.querySelectorAll('.course-card, .feature-card');

  tiltCards.forEach(card => {
    card.addEventListener('mousemove', function (e) {
      const rect = this.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      const rotateX = (y - centerY) / 30;
      const rotateY = (centerX - x) / 30;

      this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px) scale(1.02)`;
    });

    card.addEventListener('mouseleave', function () {
      this.style.transform = '';
    });
  });

  // ============================================
  // ACTIVE NAV LINK
  // ============================================
  const currentPath = window.location.pathname.toLowerCase();
  const navLinks = document.querySelectorAll('.nav-menu > li > a');

  // 1. Clear all existing active classes first
  navLinks.forEach(link => link.classList.remove('active'));

  // 2. Normalize and check each link
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (!href || href === '#' || href === 'javascript:void(0)') return;

    try {
      const linkPath = new URL(link.href).pathname.toLowerCase();

      // Normalize: remove index.html and trailing slashes for stable comparison
      const normalizeP = (p) => p.replace(/\/index\.html$/, '/').replace(/\/$/, '') || '/';

      const normLink = normalizeP(linkPath);
      const normPage = normalizeP(currentPath);

      if (normLink === normPage) {
        link.classList.add('active');
      }
    } catch (e) {
      // Ignore invalid URLs
    }
  });

  // 3. Special case for hierarchy (e.g., any page inside /courses/ should highlight Courses)
  if (currentPath.includes('/courses/')) {
    const coursesToggle = Array.from(navLinks).find(l => l.textContent.toLowerCase().includes('courses'));
    if (coursesToggle) {
      coursesToggle.classList.add('active');
    }
  }

  // ============================================
  // SCROLL PROGRESS BAR
  // ============================================
  const progressBar = document.createElement('div');
  progressBar.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background: linear-gradient(90deg, #10B981, #3B82F6);
    z-index: 9999;
    transition: width 0.1s linear;
    width: 0%;
  `;
  document.body.appendChild(progressBar);

  window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPercent = (scrollTop / docHeight) * 100;
    progressBar.style.width = scrollPercent + '%';
  });

  // ============================================
  // LAZY LOADING IMAGES
  // ============================================
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          if (img.dataset.src) {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
          }
          img.style.opacity = '1';
          imageObserver.unobserve(img);
        }
      });
    }, { rootMargin: '50px' });

    document.querySelectorAll('img[data-src]').forEach(img => {
      img.style.opacity = '0';
      img.style.transition = 'opacity 0.5s ease';
      imageObserver.observe(img);
    });
  }

  // ============================================
  // TYPING EFFECT (Optional)
  // ============================================
  const typingElement = document.querySelector('.typing-text');

  if (typingElement) {
    const words = ['Future', 'Career', 'Skills', 'Success'];
    let wordIndex = 0;
    let charIndex = 0;
    let isDeleting = false;

    function type() {
      const currentWord = words[wordIndex];

      if (isDeleting) {
        typingElement.textContent = currentWord.substring(0, charIndex - 1);
        charIndex--;
      } else {
        typingElement.textContent = currentWord.substring(0, charIndex + 1);
        charIndex++;
      }

      let delay = isDeleting ? 50 : 100;

      if (!isDeleting && charIndex === currentWord.length) {
        delay = 2000;
        isDeleting = true;
      } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        wordIndex = (wordIndex + 1) % words.length;
        delay = 500;
      }

      setTimeout(type, delay);
    }

    type();
  }

  // ============================================
  // AUTHENTICATION STATE HANDLING
  // ============================================
  const loginLink = document.querySelector('.login-link');
  const user = JSON.parse(localStorage.getItem('user') || 'null');

  if (loginLink && user) {
    loginLink.textContent = 'Sign Out';
    loginLink.href = '#';
    loginLink.classList.add('logout-link');

    loginLink.addEventListener('click', (e) => {
      e.preventDefault();
      localStorage.removeItem('user');
      window.location.reload();
    });
  }

  // ============================================
  // CONSOLE BRANDING
  // ============================================
  console.log('%c<svg viewBox="0 0 24 24"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg> Oriana Academy', 'color: #10B981; font-size: 24px; font-weight: bold;');
  console.log('%cTransforming Careers Through Education', 'color: #3B82F6; font-size: 14px;');

  // ============================================
  // DROPDOWN HOVER (Desktop)
  // ============================================
  document.querySelectorAll('.dropdown').forEach(dropdown => {
    const toggle = dropdown.querySelector('.dropdown-toggle');

    if (toggle && window.innerWidth > 768) {
      toggle.addEventListener('click', function (e) {
        e.preventDefault();
      });
    }
  });

  // ============================================
  // NEWSLETTER SUBSCRIPTION
  // ============================================
  const newsletterForms = document.querySelectorAll('.newsletter-form');

  newsletterForms.forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const input = form.querySelector('input[type="email"]');
      const email = input.value;
      const btn = form.querySelector('button');
      const originalText = btn.textContent;

      if (!email) return;

      try {
        btn.textContent = '...';
        btn.disabled = true;

        const response = await fetch('/api/contact/submit', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: 'Subscriber',
            email: email,
            phone: '',
            subject: 'Newsletter Subscription',
            message: 'New subscription from website footer'
          })
        });

        if (response.ok) {
          input.value = '';
          btn.textContent = '';
          setTimeout(() => {
            btn.textContent = originalText;
            btn.disabled = false;
          }, 3000);
          alert('Thanks for subscribing!');
        } else {
          throw new Error('Failed');
        }
      } catch (err) {
        console.error(err);
        btn.textContent = 'Error';
        setTimeout(() => {
          btn.textContent = originalText;
          btn.disabled = false;
        }, 3000);
      }
    });
  });
});

