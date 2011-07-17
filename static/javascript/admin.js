
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



//// Albums ////
function onAlbumLoad() {
    $("#albumPopup").dialog({
    	autoOpen: false,
    	width: 600,
    	close: function(event, ui) { $('#new-album-button').show(); }
    });
    $( "#dialog-confirm" ).dialog({
    	autoOpen: false,
		resizable: false,
		height:140,
		modal: true,
		buttons: {
			"Delete all items": function() {
				$ajax('admin', 'delete_album', [itemkey_toremove], function(ret){
					location.reload();
				});
			},
			Cancel: function() {
				$( this ).dialog( "close" );
			}
		}
	});
}

function newAlbum() {
	$('#new-album-button').hide();
	$('#albumPopup').dialog('option', 'buttons', { "Create": function() { albumCreate(); } });
	$('#albumPopup').dialog( 'open' );
}

function albumCreate() {
	var args = [$('#albumForm .album-title').val(), $('#albumForm .album-info').val()];
	$ajax('admin', 'create_album', args, function(ret){
		location.reload();
	});
}


function setAlbumOrder() {
	var order = $('#a_sortable').sortable('toArray');
	alert(order[0] + " " + order[1] + " " + order[2]);
	$ajax('admin', 'set_album_order', [order], function(ret){
		location.reload();
	});
}

var itemkey_toremove = "";
function removeAlbum(albumKey) {
	$("#dialog-confirm").dialog( 'open' );
	itemkey_toremove = albumKey;
}

		
jQuery(document).ready(function($) {
	$(function() {
			$( "#a_sortable" ).sortable();
			$( "#a_sortable" ).disableSelection();
	});
	
	
});



//// Slides ////