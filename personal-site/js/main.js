(function () {
  "use strict";

  var INTERVAL = 5000;

  // ===== 轮播初始化（支持多个） =====
  function initCarousel(carousel) {
    var track = carousel.querySelector(".carousel-track");
    var slides = track.querySelectorAll(".slide");
    var prevBtn = carousel.querySelector(".carousel-btn--prev");
    var nextBtn = carousel.querySelector(".carousel-btn--next");
    var dotsContainer = carousel.querySelector(".carousel-dots");

    if (!slides.length) return;

    var current = 0;
    var timer = null;
    var touchStartX = 0;

    slides.forEach(function (_, i) {
      var dot = document.createElement("button");
      dot.className = "dot" + (i === 0 ? " active" : "");
      dot.setAttribute("role", "tab");
      dot.setAttribute("aria-label", "第 " + (i + 1) + " 张");
      dot.addEventListener("click", function () {
        goTo(i);
        resetTimer();
      });
      dotsContainer.appendChild(dot);
    });

    var dots = dotsContainer.querySelectorAll(".dot");

    function goTo(index) {
      slides[current].classList.remove("active");
      dots[current].classList.remove("active");
      current = (index + slides.length) % slides.length;
      slides[current].classList.add("active");
      dots[current].classList.add("active");
    }

    function next() { goTo(current + 1); }
    function prev() { goTo(current - 1); }

    function startTimer() {
      if (slides.length <= 1) return;
      timer = setInterval(next, INTERVAL);
    }

    function resetTimer() {
      clearInterval(timer);
      startTimer();
    }

    function pauseTimer() {
      clearInterval(timer);
    }

    prevBtn.addEventListener("click", function () { prev(); resetTimer(); });
    nextBtn.addEventListener("click", function () { next(); resetTimer(); });

    carousel.addEventListener("mouseenter", pauseTimer);
    carousel.addEventListener("mouseleave", startTimer);

    carousel.addEventListener("touchstart", function (e) {
      touchStartX = e.changedTouches[0].screenX;
      pauseTimer();
    }, { passive: true });

    carousel.addEventListener("touchend", function (e) {
      var diff = touchStartX - e.changedTouches[0].screenX;
      if (Math.abs(diff) > 50) {
        diff > 0 ? next() : prev();
      }
      resetTimer();
    }, { passive: true });

    startTimer();
  }

  document.querySelectorAll("[data-carousel]").forEach(initCarousel);

  // ===== 顶部导航滚动效果 =====
  var header = document.getElementById("header");
  window.addEventListener("scroll", function () {
    header.classList.toggle("scrolled", window.scrollY > 20);
  });

  // ===== 锚点平滑滚动 =====
  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener("click", function (e) {
      var id = link.getAttribute("href");
      if (id === "#") return;
      var target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: "smooth" });
    });
  });

  // ===== 滚动入场动画 =====
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: "0px 0px -40px 0px" });

    revealEls.forEach(function (el) {
      observer.observe(el);
    });
  } else {
    revealEls.forEach(function (el) {
      el.classList.add("visible");
    });
  }

})();
