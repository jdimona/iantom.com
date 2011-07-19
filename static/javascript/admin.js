
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
var albumkey_toremove = "";
var photokey_toremove = "";
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
				$ajax('admin', 'delete_album', [albumkey_toremove], function(ret){
					location.reload();
				});
			},
			Cancel: function() {
				$( this ).dialog( "close" );
			}
		}
	});
}

function albumCreate() {
	var args = [$('#albumForm .album-title').val(), $('#albumForm .album-info').val()];
	$ajax('admin', 'create_album', args, function(ret){
		location.reload();
	});
}


function newAlbum() {
	$('#new-album-button').hide();
	$('#albumPopup').dialog('option', 'buttons', { "Create": function() { albumCreate(); } });
	$('#albumPopup').dialog( 'open' );
}



function setAlbumOrder() {
	var order = $('#a_sortable').sortable('toArray');
	$ajax('admin', 'set_album_order', [order], function(ret){
		location.reload();
	});
}

function removeAlbum(albumKey) {
	$("#dialog-confirm").dialog( 'open' );
	albumkey_toremove = albumKey;
}

function  openAlbum(albumKey) {
	$ajax('admin', 'show_album', [albumKey], function(html){
		$('#album-listing').hide();
		$('#album-display').html(html).show();
		$("#slidePopup").dialog({
	    	autoOpen: false,
	    	width: 600,
	    	close: function(event, ui) { $('#new-slide-button').show(); }
	    });
	    $( "#dialog-confirm-photo" ).dialog({
	    	autoOpen: false,
			resizable: false,
			height:140,
			modal: true,
			buttons: {
				"Delete item": function() {
					$ajax('admin', 'delete_photo', [photokey_toremove, $('#album-to-add-to').val()], function(ret){
						location.reload();
					});
				},
				Cancel: function() {
					$( this ).dialog( "close" );
				}
			}
		});
		$('#album-to-add-to').val(albumKey);
	});
}

		
jQuery(document).ready(function($) {
	$(function() {
			$( "#a_sortable" ).sortable();
			$( "#a_sortable" ).disableSelection();
			$( "#b_sortable" ).sortable();
			$( "#b_sortable" ).disableSelection();
	});
	
	
});



//// Slides ////
function newSlide() {
	$('#new-slide-button').hide();
	$('#slidePopup').dialog();
	$('#slidePopup').dialog( 'open' );
}



function setPhotoOrder() {
	var order = $('#b_sortable').sortable('toArray');
	$ajax('admin', 'set_photo_order', [order], function(ret){
		location.reload();
	});
}

function removeSlide(photoKey) {
	photokey_toremove = photoKey;
	$("#dialog-confirm-photo").dialog( 'open' );
}




