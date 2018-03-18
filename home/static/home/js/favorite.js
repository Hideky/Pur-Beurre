$(document).ready(function(){
    $('#listing').find('button').click(function(){
		var button = $(this);
		button.prop('disabled', true);
		$.ajax({
			type: "GET",
			url: "/saveproduct/"+button.attr('name'),
			success: function(data){
				console.log(button.html());
				if (button.html().includes('Enregistrer'))
					button.html('<i class="fa fa-trash fa-lg"></i>  Supprimer');
				else
					button.html('<i class="fa fa-save fa-lg"></i>  Enregistrer');
				console.log(data);
			},
			error: function(){
				console.log('Error');
			},
			complete: function(){
				console.log('Complete');
				button.prop('disabled', false);
			}
		});
	});
});