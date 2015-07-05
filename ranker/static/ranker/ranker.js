$(document).ready(function(){
    $("#match").submit(function(){
        var album_ids = $("#album_ids").val().split("|")
        var winner = $(this).find("input[type=submit]:focus").data('winner')
        var loser = album_ids[0] == winner ? album_ids[1] : album_ids[0]

        $("#winner").val(winner)
        $("#loser").val(loser)
    })
})