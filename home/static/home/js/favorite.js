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

/*function search(){
  if (!$('#searchbar').val())
    return;
  
  // Save actual status to backup after search
  searchButton = $('#searchbutton')

  // Change button when searching
  $('#searchbutton').html('<span class="glyphicon glyphicon-refresh glyphicon-refresh-animate"></span> Je réfléchi...')
  $('#searchbutton').prop('disabled', true);

  
  
}

// Function used to set a new google map (export from google map api doc)
function initMap(coord) {
        var uluru = {lat: coord.lat, lng: coord.lng};
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 15,
          center: uluru
        });
        var marker = new google.maps.Marker({
          position: uluru,
          map: map
        });
      }

// Binding of Enter on search bar
$('#searchbutton').bind( "click", search);
$('#searchbar').bind('keydown', function (k) {
    if (k.keyCode == 13) {
        $('#searchbutton').click();
    }
});*/