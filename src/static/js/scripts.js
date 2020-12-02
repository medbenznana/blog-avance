
//Only for Demo animation Selection
$(document).ready(function() {
    $('#alertos').delay(5000).fadeOut( "slow", function() {
        // Animation complete.
        $('#alertos').prop("disabled", false);
    });
});

$(document).ready(function(){
    $("area[rel^='prettyPhoto']").prettyPhoto();
    
    $(".gallery:first a[rel^='prettyPhoto']").prettyPhoto({animation_speed:'normal',theme:'light_square',slideshow:8000, autoplay_slideshow: true});
    $(".gallery:gt(0) a[rel^='prettyPhoto']").prettyPhoto({animation_speed:'fast',slideshow:50000, hideflash: true});

    $("#custom_content a[rel^='prettyPhoto']:first").prettyPhoto({
        custom_markup: '<div id="map_canvas" style="width:260px; height:265px"></div>',
        changepicturecallback: function(){ initialize(); }
    });

    $("#custom_content a[rel^='prettyPhoto']:last").prettyPhoto({
        custom_markup: '<div id="bsap_1259344" class="bsarocks bsap_d49a0984d0f377271ccbf01a33f2b6d6"></div><div id="bsap_1237859" class="bsarocks bsap_d49a0984d0f377271ccbf01a33f2b6d6" style="height:260px"></div><div id="bsap_1251710" class="bsarocks bsap_d49a0984d0f377271ccbf01a33f2b6d6"></div>',
        changepicturecallback: function(){ _bsap.exec(); }
    });
});

 var revapi;

	jQuery(document).ready(function() {
	    "use strict";
	    revapi = jQuery('.tp-banner').revolution(
	            {
	                delay: 5000,
	                startwidth: 1200,
	                startheight: 278,
	                hideThumbs: 10,
	                fullWidth: "on"
	            });

	}); //ready


 $(document).ready(function(){
    $(".content-markdown").each(function(){
            var content = $(this).text()
            var markedContent = marked(content)
            $(this).html(markedContent)
    })
    $(".post-detail-item img").each(function(){
            $(this).addClass("img-responsive");
    })

    

    var contentInput = $("#id_content");

    function setContent(value){
        var markedContent = marked(value)
        $("#preview-content").html(markedContent)
        $("#preview-content img").each(function(){
            $(this).addClass("img-responsive")
        })
    }
    setContent(contentInput.val())

    contentInput.keyup(function(){
        var newContent = $(this).val()
        setContent(newContent)
    })

    var titleInput = $("#id_title");
    


    function setTitle(value) {
        $("#preview-title").text(value)
    }
    setTitle(titleInput.val())

    titleInput.keyup(function(){
        var newContent = $(this).val()
        setTitle(newContent)
    })

    $(".comment-reply-btn").click(function(event){
        event.preventDefault();

        var parent = $(this).parent();
        var parentParent = $(parent).parent();
        var parentParentParent = $(parentParent).parent();
        parentParentParent.next(".comment-reply").fadeToggle();
    })


    // preview-title
    // preview-content

})

$(document).ready(function(){
	function updateText(btn, newCount, verb){
	    btn.attr("data-likes", newCount)
	    btn.text(verb + newCount + "")
	}
	$(".like-btn").click(function(e){
	    e.preventDefault()
	    var this_ = $(this)
	    var likeUrl = this_.attr("data-href")
	    var likeCount = parseInt(this_.attr("data-likes")) | 0
	    var addLike = likeCount + 1
	    var removeLike = likeCount - 1

	    var nolikeCount = parseInt($(".nolike-btn").attr("data-likes")) | 0
	    var removenoLike = nolikeCount - 1

	    if (likeUrl){
	       $.ajax({
	        url: likeUrl,
	        method: "GET",
	        data: {},
	        success: function(data){
	          console.log(data)
	          var newLikes;
	          if (data.liked){
	                if (data.noliked){
	                    updateText($(".nolike-btn"), removenoLike, " ")
	                }
	              updateText(this_, addLike, " ")
	          } else {
	              updateText(this_, removeLike, " ")
	              // remove one like
	          }
	        }, error: function(error){
	          console.log(error)
	          console.log("error")
	        }
	      })
	    }
	   
	  })

	$(".nolike-btn").click(function(e){
	    e.preventDefault()
	    var this_ = $(this)
	    var nolikeUrl = this_.attr("data-href")
	    var nolikeCount = parseInt(this_.attr("data-likes")) | 0
	    var addnoLike = nolikeCount + 1
	    var removenoLike = nolikeCount - 1

	    var likeCount = parseInt($(".like-btn").attr("data-likes")) | 0
	    var removeLike = likeCount - 1

	    if (nolikeUrl){
	       $.ajax({
	        url: nolikeUrl,
	        method: "GET",
	        data: {},
	        success: function(data){
	          console.log(data)
	          var newLikes;
	          if (data.noliked){
	                if (data.liked){
	                    updateText($(".like-btn"), removeLike, " ")
	                }
	              updateText(this_, addnoLike, " ")
	          } else {
	              updateText(this_, removenoLike, " ")
	              // remove one like
	          }
	        }, error: function(error){
	          console.log(error)
	          console.log("error")
	        }
	      })
	    }
	   
	  })
	})

$(document).on('submit', '.comment-form', function(e){
    e.preventDefault();
    console.log($(this).serialize());
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: $(this).serialize(),
        dataType: 'json',
        success: function(response){
          $('.main-comment-section').html(response['form']);
          $('textarea').val('');
          $(".comment-reply-btn").click(function(event){
                event.preventDefault();

                var parent = $(this).parent();
                var parentParent = $(parent).parent();
                var parentParentParent = $(parentParent).parent();
                parentParentParent.next(".comment-reply").fadeToggle();

                $('textarea').val('');
            });
        },error: function(rs, e){
          console.log(rs.responseText);
        }
    })

 });
$(document).on('submit', '.reply-form', function(e){
    e.preventDefault();
    console.log($(this).serialize());
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: $(this).serialize(),
        dataType: 'json',
        success: function(response){
          $('.main-comment-section').html(response['form']);
          $('textarea').val('');
          $(".comment-reply-btn").click(function(event){
                event.preventDefault();
                
                var parent = $(this).parent();
                var parentParent = $(parent).parent();
                var parentParentParent = $(parentParent).parent();
                parentParentParent.next(".comment-reply").fadeToggle();
                
                $('textarea').val('');
            });
        },error: function(rs, e){
          console.log(rs.responseText);
        }
    })

 });

$(document).on('submit', '.thread-form', function(e){
    e.preventDefault();
    console.log($(this).serialize());
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: $(this).serialize(),
        dataType: 'json',
        success: function(response){
          $('.main-thread-section').html(response['form']);
          $('textarea').val('');
        },error: function(rs, e){
          console.log(rs.responseText);
        }
    })

 });

$(document).on('submit', '.favorite-form', function(e){
    e.preventDefault();
    console.log($(this).serialize());
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: $(this).serialize(),
        dataType: 'json',
        success: function(response){
            $('.main-favorite-section').html(response['form_favorite']);
            
            if (response.is_favourite){
                $(".btn-favorite").html('<i class="fa fa-heart"></i>');
            }else{
                $(".btn-favorite").html('<i class="fa fa-heart-o"></i>');
            } 
          
        },error: function(rs, e){
          console.log(rs.responseText);
        }
    })

 });


$(window).on("load", function () {
   "use strict";
   $(".loader").fadeOut(800);
   $("#ex2").slider({});
   $("#pageload-modal").modal("show");
});

$(window).bind("load", function() {
   $(".light-modal-body #id_email").val('');
});
$(document).ready(function() {
    $('.light-modal-content').not('.no').removeClass().addClass('flipInY light-modal-content animated');
});



$(document).ready(function() {
    $('.ask').jConfirmAction({
        question : "&ecirc;tes-vous sûr?", 
        yesAnswer : "oui", 
        cancelAnswer : "non"
    });
});