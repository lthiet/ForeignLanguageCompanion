function clearAll() {
    $(".form_container").html('');
}

function translate() {
    clearAll()
    $.get("/vocabulary/translate",
        {
            word: $("#word_src").val()
        },
        function (data) {
            $("#result_translate").html(data);
        }
    );
}

function search() {
$.get("/vocabulary/search",
        {
            word: $("#word_dst").val()
        },
        function (data) {
            $("#result_search").html(data);
        }
    );
}

function add() {
$.get("/vocabulary/add",
        {
        },
        function (data) {
            $("#result_add").html(data);
        }
    );

}

function playAudio() {
    select_item = $("#recording")
    var audio = new Audio(select_item.val());
    audio.play();
}

function selectImage(event) {
    image = event.target
    if (image.classList.contains('selected')) {
        event.target.classList.remove('selected');
        event.target.classList.add('unselected');
    } else {
        event.target.classList.add('selected');
        event.target.classList.remove('unselected');
    }
}
