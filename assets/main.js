// Init Datatable plugin
$(document).ready(function() {
    $('#datatable').DataTable();
});

// Passing data-id from as Track ID that will be used for data insert

$(document).on("click", "#addToPlaylistBtn", function() {
    var trackID = $(this).data('id');
    $(".modal-body #trackID").val(trackID);
    $('#addToPlaylistModal').modal('show');
});

// Trigger form reset when we close modal window

$('#addToPlaylistModal').on('hidden.bs.modal', function() {
    $(this).find('form').trigger('reset');
});

// AJAX form submission for creating and adding tracks to Playlists

$(document).on("submit", "#createPlaylistForm", function(e) {
    e.preventDefault();

    $.ajax({
        type: 'POST',
        url: '/music/search',
        data: {            
            playlistname: $('input[name=playlistname]').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(){
            $("#createPlaylistModal").find('form').trigger('reset'); // Reset form
            $("#createPlaylistModal").modal("hide"); // Hide modal window
            swal({
                title: "Yey!",
                text: "Playlist has been created",
                icon: "success",
                button: false
            });
            window.setTimeout(function(){location.reload()},500)
            
        }
    });
});

$(document).on("submit", "#addToPlaylistForm", function(e) {
    e.preventDefault();

    $.ajax({
        type: 'POST',
        url: '/music/search',
        data: {            
            playlistid: $('#playlistid').val(),
            trackid: $('input[name=trackid]').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(){ 
            $("#addToPlaylistModal").find('form').trigger('reset'); // Reset form
            $("#addToPlaylistModal").modal("hide"); // Hide modal window
            swal("Song added to Playlist!", "Good Job! :)", "success"); // Sweet Alert Message            
        }
    });
});

