

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
    function load(hash) {
    	if(hash.localeCompare("main") == 0) {
    		$ajax('portfolio', 'get_main', [], function(html) {
    			$('#viewer').html(html);
    			if($('#bottom-bar').css('display') != "none") {
    				$('#bottom-bar').slideDown('slow');
    			}
    		});
    	} 
    	else if(hash.localeCompare("about") == 0) {
    		$ajax('portfolio', 'get_about', [], function(html) {
    			$('#viewer').html(html);
    			if($('#bottom-bar').css('display') != "none") {
    				$('#bottom-bar').slideToggle('slow');
    			}
    		});
    	}
    	else {
    		var hashArr = hash.split("-");
    		$ajax('portfolio', 'get_photo', [hashArr[0], hashArr[1]], function(ret) {
    			html = ret[0];
    			numPhotos = ret[1];
    			$('#viewer').html(html);
    			$('#current-picture-index').html(hashArr[1]);
    			$('#total-pictures').html(numPhotos);
    			$('#prev').removeClass('disabled').attr('href', '#' + hashArr[0] + '-' + (parseInt(hashArr[1]) - 1));
    			$('#next').removeClass('disabled').attr('href', '#' + hashArr[0] + '-' + (parseInt(hashArr[1]) + 1));
    			if(hashArr[1] == 1) {
    				$('#prev').addClass('disabled');
    			}
    			else if(hashArr[1] == numPhotos) {
    				$('#next').addClass('disabled');
    			}
    			if($('#bottom-bar').css('display') == "none") {
    				$('#bottom-bar').slideToggle('slow');
    			}
    		});
    	}
    }

    $.history.init(function(hash) {
        load(hash == "" ? "main" : hash);
    });

    $('#album-nav a').live('click', function(e) {
        var hash = $(this).attr('href');
        hash = hash.replace(/^.*#/, '');
        $.history.load(hash);
        return false;
    });
    
    
    //// Viewer Setup ////
    var windowHeight = $(window).height();
    var windowWidth = $(window).width();
    var viewerHeight = windowHeight - 150;
    var viewerWidth = windowWidth - 340;
    
    $('#viewer').height(viewerHeight);
    $('#viewer').width(viewerWidth);
    
    $(window).resize(function() {
    	windowHeight = $(window).height();
        windowWidth = $(window).width();
        viewerHeight = windowHeight - 150;
        viewerWidth = windowWidth - 340;
        
        $('#viewer').height(viewerHeight);
        $('#viewer').width(viewerWidth);
    });
    
    
    //// Menu UI ////
    $('.nav-link').mouseover(function(){
    	$(this).stop().animate({
    		backgroundColor: "#3D3D3D",
    	    color: "#7A7A7A"
    	}, {duration:150});
    }).mouseout(function(){
    	$(this).stop().animate({
    		backgroundColor: "#000000",
      	    color: "#575757"
      	}, {duration:150});
    });
    
    
    //// Slide Show UI ////
    
    
});




