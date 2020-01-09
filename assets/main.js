// Init Datatable plugin
$(document).ready(function() {
  $('#datatable').DataTable();
});

// Main Loader
window.addEventListener("load", function() {
  const loader = document.querySelector(".loader");
  loader.className += " hidden";
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

// Alert auto close after delay
$(document).ready(function() {
  $('.alert').delay(2500).slideUp();
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
    success: function() {
      $("#createPlaylistModal").find('form').trigger('reset'); // Reset form
      $("#createPlaylistModal").modal("hide"); // Hide modal window
      swal({
        title: "Yey!",
        text: "Playlist has been created",
        icon: "success",
        button: false
      });
      window.setTimeout(function() {
        location.reload()
      }, 500)
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
    success: function() {
      $("#addToPlaylistModal").find('form').trigger('reset'); // Reset form
      $("#addToPlaylistModal").modal("hide"); // Hide modal window
      swal("Song added to Playlist!", "Good Job! :)", "success"); // Sweet Alert Message
    }
  });
});

// Audio Player for Tabelar Views

$(document).ready(function() {

  $('.play-button').on("click", function() {
    player = $("#audio-player");
    url = $(this).data('url');

    // $(".play-button").removeClass('fa-pause-circle').addClass("fa-play-circle");
    $("#audio-player source").attr('src', url);

    if ($(this).hasClass('fa-play-circle')) {
      $(this).removeClass('fa-play-circle');
      $(this).addClass('fa-pause-circle');
      player.trigger('load');
      player.trigger('play');
    } else {
      $(this).removeClass('fa-pause-circle');
      $(this).addClass('fa-play-circle');
      player.trigger('pause');
    }

  });

  $('#audio-player').on('ended', function() {
    $(".play-button").removeClass('fa-pause-circle').addClass("fa-play-circle");
  });

});

// Favorite Song Functionality

$(document).ready(function() {

  $('.favorite-btn').on('click', function() {
    $.ajax({
      type: 'POST',
      url: '/music/track/favorited',
      data: {
        song_id: $(this).data('id'),
        csrfmiddlewaretoken: $(this).data('token')
      },
      success: function() {
        console.log('Yey!');
      }
    });

    if ($(this).hasClass('far')) {
      $(this).removeClass('far').addClass('fas');
    } else {
      $(this).removeClass('fas').addClass('far');
    }

  });
});


// Audio Player Track page

var audio = document.getElementById("audio-player");

$(document).ready(function() {
  $("#play-button").click(function() {
    if ($(this).hasClass("unchecked")) {
      $(this)
        .addClass("play-active")
        .removeClass("play-inactive")
        .removeClass("unchecked");
      $(".info-two")
        .addClass("info-active");
      $("#pause-button")
        .addClass("scale-animation-active");
      $(".waves-animation-one, #pause-button, .seek-field, .volume-icon, .volume-field, .info-two").show();
      $(".waves-animation-two").hide();
      $("#pause-button")
        .children('.icon')
        .addClass("fa-pause")
        .removeClass("fa-play");
      setTimeout(function() {
        $(".info-one").hide();
      }, 400);
      audio.play();
      audio.currentTime = 0;
    } else {
      $(this)
        .removeClass("play-active")
        .addClass("play-inactive")
        .addClass("unchecked");
      $("#pause-button")
        .children(".icon")
        .addClass("fa-pause")
        .removeClass("fa-play");
      $(".info-two")
        .removeClass("info-active");
      $(".waves-animation-one, #pause-button, .seek-field, .volume-icon, .volume-field, .info-two").hide();
      $(".waves-animation-two").show();
      setTimeout(function() {
        $(".info-one").show();
      }, 150);
      audio.pause();
      audio.currentTime = 0;
    }
  });
  $("#pause-button").click(function() {
    $(this).children(".icon")
      .toggleClass("fa-play")
      .toggleClass("fa-pause");

    if (audio.paused) {
      audio.play();
    } else {
      audio.pause();
    }
  });
  $("#play-button").click(function() {
    setTimeout(function() {
      $("#play-button").children(".icon")
        .toggleClass("fa-play")
        .toggleClass("fa-times");
    }, 350);
  });
  $(".like").click(function() {
    $(".icon-heart").toggleClass("like-active");
  });
});

function CreateSeekBar() {
  var seekbar = document.getElementById("audioSeekBar");
  seekbar.min = 0;
  seekbar.max = audio.duration;
  seekbar.value = 0;
}

function EndofAudio() {
  document.getElementById("audioSeekBar").value = 0;
}

function audioSeekBar() {
  var seekbar = document.getElementById("audioSeekBar");
  audio.currentTime = seekbar.value;
}

function SeekBar() {
  var seekbar = document.getElementById("audioSeekBar");
  seekbar.value = audio.currentTime;
}

audio.addEventListener("timeupdate", function() {
  var duration = document.getElementById("duration");
  var s = parseInt(audio.currentTime % 60);
  var m = parseInt((audio.currentTime / 60) % 60);
  duration.innerHTML = m + ':' + s;
}, false);

Waves.init();
Waves.attach("#play-button", ["waves-button", "waves-float"]);
Waves.attach("#pause-button", ["waves-button", "waves-float"]);
