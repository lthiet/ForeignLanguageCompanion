// This script contain the Web Interactivity Logic for the sentence HTML page



function displaySentence() {
  $("#choose_sentence_result").text($("#input_sentence").val());
}

function selectSentence() {
  text_part = window.getSelection().toString();
  if (text_part == "") {
    window.alert("You didn't choose anything");
    return;
  }

  $("#selected_part_of_sentence").html(
    "You chose : <em id='text_part'>" + text_part + "</em>"
  );

  $.get("/lemmatizer/", {
    "word": text_part,
    "target": $("#target").val()
  }, function (data) {
    $("#front").val(data)
  })
}

function add_sentences() {
  $.get(
    "/sentences/add/", {
      text_full: $("#input_sentence").val(),
      recording: $("#recording").val(),
      front: $("#front").val(),
      text_part: $("#text_part").text(),
      images: $(".selected")
        .map(function () {
          return this.dataset.content;
        })
        .get(),
      deck: $("#deck").val(),
      twocard: $("#2card").is(":checked"),
      guess_syntax: $("#guess_syntax").is(":checked")
    },
    function (data) {
      $("#thread_status").append(running_status_element(data));
    }
  );
}