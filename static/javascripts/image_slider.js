document.addEventListener('DOMContentLoaded', function () {
    const sliderContainer = document.querySelector('.slider-container');
    const slides = document.querySelectorAll('.slide');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    let currentIndex = 0;

    function updateSlider() {
        sliderContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
    }

    prevBtn.addEventListener('click', () => {
        if (currentIndex > 0) {
            currentIndex--;
        } else {
            currentIndex = slides.length - 1;
        }
        updateSlider();
    });

    nextBtn.addEventListener('click', () => {
        if (currentIndex < slides.length - 1) {
            currentIndex++;
        } else {
            currentIndex = 0;
        }
        updateSlider();
    });

    // Auto-slide every 5 seconds
    setInterval(() => {
        if (currentIndex < slides.length - 1) {
            currentIndex++;
        } else {
            currentIndex = 0;
        }
        updateSlider();
    }, 5000);
    
});

document.addEventListener("DOMContentLoaded", function () {
    const sliderContainer = document.querySelector(".achievement-slider-container");
    const slides = document.querySelectorAll(".achievement-slide");
    const prevBtn = document.querySelector(".achievement-prev-btn");
    const nextBtn = document.querySelector(".achievement-next-btn");

    let index = 0;
    const totalSlides = slides.length;

    function updateSlider() {
        sliderContainer.style.transform = `translateX(-${index * 100}%)`;
    }

    nextBtn.addEventListener("click", function () {
        index = (index + 1) % totalSlides;
        updateSlider();
    });

    prevBtn.addEventListener("click", function () {
        index = (index - 1 + totalSlides) % totalSlides;
        updateSlider();
    });

    // Auto-slide every 4 seconds
    setInterval(() => {
        index = (index + 1) % totalSlides;
        updateSlider();
    }, 4000);
});

document.addEventListener('DOMContentLoaded', function () {
    // Add interactivity to press items (optional)
    const pressItems = document.querySelectorAll('.press-item');

    pressItems.forEach(item => {
        item.addEventListener('click', () => {
            item.classList.toggle('expanded');
        });
    });

    // Add animation to student quote (optional)
    const studentQuote = document.querySelector('.student-quote');

    studentQuote.addEventListener('mouseenter', () => {
        studentQuote.style.transform = 'scale(1.02)';
        studentQuote.style.transition = 'transform 0.3s ease';
    });

    studentQuote.addEventListener('mouseleave', () => {
        studentQuote.style.transform = 'scale(1)';
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const sliderContainer = document.querySelector('.slider-container2');
    const slides = document.querySelectorAll('.slide2');
    const prevBtn = document.querySelector('.prev-btn2');
    const nextBtn = document.querySelector('.next-btn2');
    let currentIndex = 0;

    function updateSlider() {
        sliderContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
    }

    prevBtn.addEventListener('click', () => {
        if (currentIndex > 0) {
            currentIndex--;
        } else {
            currentIndex = slides.length - 1;
        }
        updateSlider();
    });

    nextBtn.addEventListener('click', () => {
        if (currentIndex < slides.length - 1) {
            currentIndex++;
        } else {
            currentIndex = 0;
        }
        updateSlider();
    });

    // Auto-slide every 5 seconds
    setInterval(() => {
        if (currentIndex < slides.length - 1) {
            currentIndex++;
        } else {
            currentIndex = 0;
        }
        updateSlider();
    }, 5000);
});