function translate() {
    console.log('hi')
    $.get("/vocabulary/translate",
        {
            word: $("#word").val()
        },
        function (data) {
            $(".container").append(data);
        }
    );
}
