

//// Shared ////
function $ajax(mod_name, fname, arglist, callback) {
    var meth = (('string' == typeof mod_name) ? '/rpc/' + mod_name : '/rpc');
    $.post(meth,
           { 
               func: fname,
               args: JSON.stringify(arglist) 
           }, 
           callback, "json");
}



jQuery(document).ready(function($) {
	    //// Viewer Setup ////
    var windowHeight = $(window).height();
    var windowWidth = $(window).width();
    var viewerHeight = windowHeight - 150;
    var viewerWidth = windowWidth - 340;
    
    $('#viewer').height(viewerHeight);
    $('#viewer').width(viewerWidth);
    $('#viewer-wrapper').height(viewerHeight);
    $('#viewer-wrapper').width(viewerWidth);
    
    $(window).resize(function() {
    	windowHeight = $(window).height();
        windowWidth = $(window).width();
        viewerHeight = windowHeight - 150;
        viewerWidth = windowWidth - 340;
        
        $('#viewer').height(viewerHeight);
        $('#viewer').width(viewerWidth);
        $('#viewer-wrapper').height(viewerHeight);
    	$('#viewer-wrapper').width(viewerWidth);
    });
    
    function load(hash) {
    	if(hash.localeCompare("main") === 0) {
    		$ajax('portfolio', 'get_main', [], function(html) {
    			$('#viewer').html(html);
    			if($('#bottom-bar').css('display') != "none") {
    				$('#bottom-bar').slideDown(500);
    			}
    		});
    	} 
    	else if(hash.localeCompare("about") === 0) {
    		$ajax('portfolio', 'get_about', [], function(html) {
    			$('#viewer').html(html);
    			if($('#bottom-bar').css('display') != "none") {
    				$('#bottom-bar').slideToggle(500);
    			}
    		});
    	}
    	else {
    		var hashArr = hash.split("-");
    		$ajax('portfolio', 'get_photo', [hashArr[0], hashArr[1], viewerWidth, viewerHeight], function(ret) {
    			$('#viewer').hide()
    			$('#viewer-wrapper').addClass('loading');
    			html = ret[0];
    			currentPhoto = parseInt(ret[1]);
    			numPhotos = parseInt(ret[2]);
    			$('#viewer').html(html);
    			if(ret[4]) {
	    			$('#viewer').find('img')
					    // once the image has loaded, execute this code
					    .load(function () {
					    
					      // with the holding div #loader, apply:
					      $('#viewer-wrapper')
					        // remove the loading class (so no background spinner), 
					        .removeClass('loading');
					      // fade our image in to create a nice effect
					      $('#viewer').fadeIn(500);
					    });
				} else {
					$('#slide-text').css('padding-top', ((viewerHeight/2) - 50) + 'px')
					$('#viewer-wrapper').removeClass('loading');
					$('#viewer').fadeIn(500);
				}  
    			$('#current-picture-index').html(currentPhoto + 1);
    			$('#total-pictures').html(numPhotos);
    			$('#prev').attr('href', '#' + hashArr[0] + '-' + (currentPhoto - 1));
    			$('#next').attr('href', '#' + hashArr[0] + '-' + (currentPhoto + 1));
    			
    			if(currentPhoto == 0) {
    				$('#prev').addClass('disabled');
    				$('#prev').animate({
    					color: '#636363'
    				});
    			} else if(currentPhoto){
    				$('#prev').removeClass('disabled');
    				$('#prev').animate({
    					color: '#BABABA'
    				});
    			}
    			
    			if(currentPhoto + 1 >= numPhotos) {
    				$('#next').addClass('disabled');
    				$('#next').animate({
    					color: '#636363'
    				});
    			} else {
    				$('#next').removeClass('disabled');
    				$('#next').animate({
    					color: '#BABABA'
    				});
    			}
    			
    			if($('#bottom-bar').css('display') == "none") {
    				$('#bottom-bar').slideToggle(500);
    			}
    		});
    	}
    }

    $.history.init(function(hash) {
        load(hash === "" ? "main" : hash);
    });

    $('#album-nav a').live('click', function(e) {
        var hash = $(this).attr('href');
        hash = hash.replace(/^.*#/, '');
        $.history.load(hash);
        return false;
    });
    
    

    
    
    //// Menu UI ////
    $('.nav-link').mouseenter(function(){
    	$(this).stop().animate({
    		backgroundColor: "#3D3D3D",
    	    color: "#7A7A7A"
    	}, {duration:150});
    }).mouseleave(function(){
    	$(this).stop().animate({
    		backgroundColor: "#000000",
      	    color: "#575757"
      	}, {duration:150});
    });
    
    
    //// Slide Show UI ////
    $('#next').mouseover(function(){
    	if(!$('#next').hasClass('disabled')) {
			$(this).stop().animate({
			    color: "#DEDEDE"
			}, {duration:150});
		}
    }).mouseout(function(){
    	if(!$('#next').hasClass('disabled')) {
	    	$(this).stop().animate({
	      	    color: "#BABABA"
	      	}, {duration:150});
      }
    });
    
    $('#prev').mouseover(function(){
    	if(!$('#prev').hasClass('disabled')) {
	    	$(this).stop().animate({
	    	    color: "#DEDEDE"
	    	}, {duration:150});
	    }
    }).mouseout(function(){
    	if(!$('#prev').hasClass('disabled')) {
	    	$(this).stop().animate({
	    		color: "#BABABA"
	      	}, {duration:150});
      }
    });
    
    
});




