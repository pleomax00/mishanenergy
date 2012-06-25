jQuery.fn.extend({
   imgShow: function() {
       showOn = $(this);
       clientLen = $(this).find ("li").length;
       showNext = function() {
           if (clientLen > 1) {
               while (true) {
                   next = Math.round(Math.random()*1000) % clientLen;
                   if ( $(showOn.find ("li")[next]).hasClass ("active") ) {
                       continue;
                   }
                   break;
               }
           }
           else {
               next = 0;
           }
           showOn.find ("li.active").removeClass ("active").fadeOut( function () {
               $(showOn.find ("li")[next]).addClass ("active");
               $(showOn.find ("li")[next]).fadeIn();
           });
       };
       setInterval ( "showNext()", 2000 );
   },
   hideable: function() {
       $(this).hover ( function () {
           $(this).find ( ".hiddenuploadpage" ).fadeIn ( 60 );
       }, function () {
           $(this).find ( ".hiddenuploadpage" ).fadeOut ( 60 );
       });
   },
   textInput: function() {
       $(this).val ( $(this).attr("title") );
       $(this).focus ( function () {
           if ( $(this).val() == $(this).attr("title") ) {
               $(this).val ("");
           }
       }).blur ( function () {
           if ( $(this).val() == "" ) {
               $(this).val ( $(this).attr("title") );
           }
       });
   },
   hoverify: function () {
       $.hoverObj = $(this);
       $.hoverObj.hover ( function() {
           $(this).attr ( "src", "/static/images/" + $(this).attr("hoverable") + "_hover." + $(this).attr("filetype") );
       }, function () {
           $(this).attr ( "src", "/static/images/" + $(this).attr("hoverable") + "." + $(this).attr("filetype") );
       });
   },
   dropper: function (options) {
       $.dropperObj = $(this);
       options = options || {};
       iwidth = options.width || 200;
       $(document).bind ( "click", unfoldDropper );
       $.dropperObj.click ( function (e) {
           ileft = $.dropperObj.find("img").position().left;
           itop = $.dropperObj.find("img").position().top;
           if ( alreadyOpen ) {
               return;
           }
           $.dropperObj.find ("img" ).css ( {"background": "#f6faff", "z-index": 9, "border": "1px solid #ccc", "border-bottom": "none" } );
           $(".dropped").css ( { left: ileft - iwidth + 28, top: itop+31, width: iwidth+"px", "z-index": 4, "display": "block" } );
           setTimeout ( "alreadyOpen = true;", 10 );
       });
   },
   ibutton: function (options) {
       $.buttonObj = $(this);
       $.buttonObj.click ( function () {
           if ( $(this).attr ( "state" ) == "disabled" ) {
               $(this).find ( "img" ).attr ( "src", "/static/images/" + $(this).find("img").attr("image") + ".png" );
               $(this).attr ( "state", "enabled" );
           }
           else {
               $(this).find ( "img" ).attr ( "src", "/static/images/" + $(this).find("img").attr("image") + "_bw.png" );
               $(this).attr ( "state", "disabled" );
           }
           $.post ( "/settings/" + $(this).attr("id") + "/" + $(this).attr("state") );
       });
   },
   dropdown: function () {
       $.objDD = $(this);
       $.hasDDOn = false;
       $.objDD.keyup ( function () {
           if ( $.objDD.val().length >= 3 ) {
               if ( ! $.hasDDOn ) {
                   left = $(".searchbox").position().left - 3;
                   $(".searchwhat").css ( {"display": "block", "left": left} );
               }
           }
           else {
               $(".searchwhat").css ( "display", "none" );
           }
       });
       $.objDD.blur ( function () {
           setTimeout ( function() { $(".searchwhat").css ( "display", "none" ); }, 300 );
       });
   },

   tooltip: function () {
       $(this).unbind ( 'mouseenter mouseleave' );
       $(this).hover ( function (e) {
           midx = parseInt($(this).position().left) + parseInt($(this).width() + 3);
           midy = parseInt($(this).position().top);
           $(this).find ( ".tip" ).css ( "left", midx ).css ( "top", midy );
           $(this).find ( ".tip" ).fadeIn("fast");
       }, function() {
           $(this).find ( ".tip" ).css ( "display", "none" );
       });
   },

   hovermenu: function () {
       $(this).hover ( function () {
           dt = $(this).find ( "." + $(this).attr("droptarget") );
           dt.css ( "display", "block" );
       }, function () {
           dt = $(this).find ( "." + $(this).attr("droptarget") );
           dt.fadeOut ("fast"); //css ( "display", "none" );
       });
   }
});

jQuery.fn.dhtmlform = function(options) {
    options = options || {};
    s = options.success || function() {};
    e = options.error || function () {};
    dataType = options.dataType || "html";
    elem = $(this);
    $(this).options = options;
    $(this).submit ( function (e) {
        hasError = false;
        $(this).find("input[empty=false]").each ( function () {
            if ( $(this).val () == "" || $(this).val() == $(this).attr("title") ) {
                $(this).css ( "border", "1px solid red" );
                hasError = true;
            }
        });
        $(this).find("textarea[empty=false]").each ( function () {
            if ( $(this).val () == "" || $(this).val() == $(this).attr("title") ) {
                $(this).css ( "border", "1px solid red" );
                hasError = true;
            }
        });

        if (hasError) {
            return false;
        }

        if ( options.spinner ) {
            options.spinner.html ( "<img src='/static/images/ajaxloader.gif' style='vertical-align: middle;' />" );
        }

        $.ajax ( { 
            url: $(this).attr("action"),
            data: $(this).serialize(),
            type: $(this).attr("method"),
            dataType: dataType,
            context: options,
            success: function (data) {
                options.spinner.html ( "" );
                this.success(data);
            },
            error: function () {
                this.spinner.html ( "" );
                //notify ( "There was an error in the request with the server! Please try again later." );
                this.error();
            }
        });
        return false;
    });
}
$(document).ready ( function () {
    $(".textinput").each ( function () {
        $(this).textInput ();
    });
    Cufon.replace ( ".cufon" );
    Cufon.replace ( ".makeblog .timestamp" );
    Cufon.replace ( ".blogpost" );
    Cufon.replace ( ".blogcatagory" );
    Cufon.replace ( ".mediatags" );
    Cufon.replace ( ".makeblog h2" );
    Cufon.replace ( ".textile h3" );
    Cufon.replace ( ".textile h2" );
    Cufon.replace ( ".textile ul li" );

    $(".regwebminar > form").dhtmlform ( {
        success: function(data) {
            console.log (data.text);
            $(".webinar_message" ).html ( data.text );
            Cufon.replace (".webinar_message");
        },
        error: function () {
            console.log ("Error in request!");
        },
        spinner: $(".webinar_spinner"),
        dataType: "json"
    });
    
    $(".dropper").hovermenu();
    $(".imgshow").imgShow();

});

