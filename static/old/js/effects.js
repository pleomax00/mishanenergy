$(document).ready ( function () {

    (function(d, s, id) {
        var js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) return;
        js = d.createElement(s); js.id = id;
        js.src = "//connect.facebook.net/en_US/all.js#xfbml=1&appId=155804811193105";
        fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));

    if ( $('.pix_diapo').length ) {
        $('.pix_diapo').diapo({fx: 'scrollHorz'});
    }
});
