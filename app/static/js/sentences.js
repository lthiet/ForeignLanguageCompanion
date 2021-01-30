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
          return this.src;
        })
        .get(),
      deck: $("#deck").val(),
    },
    function (data) {
      $("#thread_status").append(running_status_element(data));
    }
  );
}
