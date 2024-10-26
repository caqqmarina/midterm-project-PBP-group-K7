document.addEventListener("DOMContentLoaded", function () {
    var swiper = new Swiper('.mySwiper', {
        slidesPerView: 1,
        loop: true,
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        autoplay: {
            delay: 4000, 
            disableOnInteraction: false, 
        },
    });
    const swiperContainer = document.querySelector('.swiper-container');
    swiperContainer.addEventListener('mouseenter', function () {
        swiper.autoplay.stop();
    });

    swiperContainer.addEventListener('mouseleave', function () {
        swiper.autoplay.start();
    });
});
