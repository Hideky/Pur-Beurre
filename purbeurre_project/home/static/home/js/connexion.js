$(document).ready(function(){
    $('.modal-footer button').click(function(){
		var button = $(this);

		if ( button.attr("data-dismiss") != "modal" ){
			var inputs = $('form input');
			var title = $('.modal-title');

			inputs.attr("disabled", "disabled");

			button.attr("disabled", "disabled");


			button.text("Close")					.delay(1600)
					.removeClass("btn-primary")
					.addClass("btn-success")
    				.blur()

					.fadeIn(function(){
						title.text("Connexion Réussi");
						button.attr("data-dismiss", "modal");
					});
		}
	});

	$('#myModal').on('hidden.bs.modal', function (e) {
		var inputs = $('form input');
		var title = $('.modal-title');
		var button = $('.modal-footer button');

		inputs.removeAttr("disabled");

		title.text("Se connecter");

		button.removeClass("btn-success")
				.addClass("btn-primary")
				.text("Ok")
				.removeAttr("data-dismiss");
                
	});
});