$(document).ready(function() {

	$('.hover').mousemove(function(e){
		var hovertext = $(this).attr('hinttext'); 
		$('#hintbox').text(hovertext).show();
		$('#hintbox').css('top',e.clientY+15).css('left',e.clientX+15);
	})
	.mouseout(function(){
		$('#hintbox').hide();
	});

});