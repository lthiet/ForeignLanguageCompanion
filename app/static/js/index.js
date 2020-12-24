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
    window.alert('ok')
}
