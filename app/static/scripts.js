$(document).ready(function(){
    // Smooth scrolling for all links
    $("a").on('click', function(event) {
        if (this.hash !== "") {
            event.preventDefault();
            var hash = this.hash;
            $('html, body').animate({
                scrollTop: $(hash).offset().top
            }, 800, function(){
                window.location.hash = hash;
            });
        }
    });

    // Scroll animation
    $(window).on('scroll', function() {
        $('.fade-in').each(function() {
            var top_of_element = $(this).offset().top;
            var bottom_of_element = $(this).offset().top + $(this).outerHeight();
            var bottom_of_screen = $(window).scrollTop() + $(window).innerHeight();
            var top_of_screen = $(window).scrollTop();

            if ((bottom_of_screen > top_of_element) && (top_of_screen < bottom_of_element)) {
                $(this).addClass('visible');
            } else {
                $(this).removeClass('visible');
            }
        });
    });

    // Lazy loading images
    $('.lazy-load').each(function() {
        var img = $(this);
        img.attr('src', img.data('src'));
    });
});
