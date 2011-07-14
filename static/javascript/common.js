

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
    	if(hash == "main") {
    		$ajax('portfolio', 'get_main', [], function(html) {
    			$('#viewer').html(html);
    		});
    	} 
    	else if(hash == "about") {
    		$ajax('portfolio', 'get_about', [], function(html) {
    			$('#viewer').html(html);
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




