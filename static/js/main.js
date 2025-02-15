document.addEventListener("DOMContentLoaded", function () {
  var swiper = new Swiper(".swiper", {
      loop: true,
      spaceBetween: 20,
      slidesPerView: 1,
      pagination: {
          el: ".swiper-pagination",
          clickable: true,
      },
      autoplay: {
          delay: 3000,
          disableOnInteraction: false,
      },

  });
});



document.addEventListener("DOMContentLoaded", function () {
  ScrollReveal().reveal('.hero__text', {
      duration: 1000,
      origin: 'left',
      distance: '50px',
      delay: 200,
      easing: 'ease-in-out',
      reset: true
  });

  ScrollReveal().reveal('.hero__img', {
      duration: 1000,
      origin: 'right',
      distance: '50px',
      delay: 600,
      easing: 'ease-in-out',
      reset: true
  });

   // Text Section (fade in from left)
   ScrollReveal().reveal('.about__text', {
    duration: 1000,
    origin: 'left',
    distance: '50px',
    delay: 200,
    easing: 'ease-in-out',
    reset: true,
    mobile: true
  });

  // Features (staggered fade-in from bottom)
  ScrollReveal().reveal('.about__feature', {
      duration: 800,
      origin: 'bottom',
      distance: '30px',
      delay: 300,
      easing: 'ease-in-out',
      reset: true,
      interval: 200, // Stagger effect
      mobile: true
  });

  // Image (fade in from right)
  ScrollReveal().reveal('.about__img', {
      duration: 1000,
      origin: 'right',
      distance: '50px',
      delay: 400,
      easing: 'ease-in-out',
      reset: true,
      mobile: true
  });

  ScrollReveal().reveal('.service__heading', {
    duration: 1000,
    origin: 'top',
    distance: '30px',
    delay: 200,
    easing: 'ease-in-out',
    reset: true,
    mobile: true
  });

  // Service Cards (staggered zoom-in effect)
  ScrollReveal().reveal('.service__card', {
      duration: 800,
      scale: 0.85,
      opacity: 0,
      delay: 300,
      easing: 'ease-in-out',
      reset: true,
      interval: 150, // Stagger effect
      mobile: true
  });

  ScrollReveal().reveal('.features-heading', {
    origin: 'top',
    distance: '50px',
    duration: 1000,
    delay: 200,
    easing: 'ease-in-out',
    reset: true
  });

  ScrollReveal().reveal('.features-img', {
      origin: 'left',
      distance: '80px',
      duration: 1200,
      delay: 300,
      easing: 'ease-in-out',
      reset: true
  });

  ScrollReveal().reveal('.feature-box', {
      origin: 'bottom',
      distance: '60px',
      duration: 1000,
      delay: 200,
      interval: 200,
      easing: 'ease-in-out',
      reset: true
  });

  ScrollReveal().reveal('.footer-top', {
    origin: 'bottom',
    distance: '50px',
    duration: 1200,
    delay: 200,
    easing: 'ease-in-out',
    reset: true
  });

  ScrollReveal().reveal('.footer-bottom', {
      origin: 'bottom',
      distance: '50px',
      duration: 1000,
      delay: 400,
      easing: 'ease-in-out',
      reset: true
  });

  ScrollReveal().reveal('.footer-links', {
      origin: 'left',
      distance: '40px',
      duration: 1200,
      delay: 300,
      interval: 150,
      easing: 'ease-in-out',
      reset: true
  });

  ScrollReveal().reveal('.footer-icons', {
      scale: 0.8,
      duration: 1000,
      delay: 500,
      easing: 'ease-in-out',
      reset: true
  });

  ScrollReveal().reveal("#contact .w-full.px-4.md\\:w-1\\/2", {
    delay: 200,
    distance: "50px",
    origin: "left",
    duration: 1000,
    easing: "ease-in-out",
    reset: true
  });

  ScrollReveal().reveal("#contact .w-full.px-4.md\\:w-1\\/2.hidden", {
      delay: 300,
      distance: "50px",
      origin: "right",
      duration: 1000,
      easing: "ease-in-out",
      reset: true
  });

  ScrollReveal().reveal("#contact .flex.w-full.max-w-\\[420px\\]", {
      delay: 400,
      distance: "30px",
      origin: "bottom",
      duration: 1000,
      easing: "ease-in-out",
      interval: 150, // Staggers the animations
      reset: true
  });

  ScrollReveal().reveal("#faq .mb-5.sm\\:mb-10", {
    delay: 200,
    distance: "40px",
    origin: "top",
    duration: 1000,
    easing: "ease-in-out",
    reset: true
  });

  ScrollReveal().reveal("#faq .md\\:w-5\\/12 img", {
      delay: 300,
      distance: "50px",
      origin: "left",
      duration: 1000,
      easing: "ease-in-out",
      reset: true
  });

  ScrollReveal().reveal("#faq .md\\:w-6\\/12 li", {
      delay: 400,
      distance: "30px",
      origin: "bottom",
      duration: 1000,
      easing: "ease-in-out",
      interval: 150, // Staggers the animations
      reset: true
  });
});
