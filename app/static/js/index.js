function clearAll() {
  $(".form_container").html("");
}

function translate() {
  clearAll();
  $.get(
    "/vocabulary/translate",
    {
      word: $("#word_src").val(),
      target: $("#target").val(),
    },
    function (data) {
      $("#result_translate").html(data);
    }
  );
}

function search() {
  $.get(
    "/vocabulary/search",
    {
      word: $("#word_dst").val(),
      target: $("#target").val(),
    },
    function (data) {
      $("#result_search").html(data);
      $("#load_image_btn").click();
      if ($("#recording option").length < 1) {
        $("#load_audio_btn").click();
      }
    }
  );
}

function add_vocabulary() {
  $.get(
    "/vocabulary/add",
    {
      word: $("#word_dst").val(),
      ipa: $("#ipa").val(),
      word_usage: $("#word_usage").val(),
      recording: $("#recording").val(),
      spelling: $("#spelling").val(),
      images: $(".selected")
        .map(function () {
          return this.src;
        })
        .get(),
      deck: $("#deck").val(),
    },
    function (data) {
      $("#result_add").html(data);
      clearAll();
    }
  );
}

function add_pronunciation() {
  $.get(
    "/pronunciation/add",
    {
      word: $("#word_dst").val(),
      spelling: $("#spelling").val(),
      ipa: $("#ipa").val(),
      recording: $("#recording").val(),
      images: $(".selected")
        .map(function () {
          return this.src;
        })
        .get(),
      deck: $("#deck").val(),
    },
    function (data) {
      $("#result_add").html(data);
      clearAll();
    }
  );
}

function playAudio() {
  select_item = $("#recording");
  var audio = new Audio(select_item.val());
  audio.play();
}

function selectImage(event) {
  image = event.target;
  if (image.classList.contains("selected")) {
    event.target.classList.remove("selected");
    event.target.classList.add("unselected");
  } else {
    event.target.classList.add("selected");
    event.target.classList.remove("unselected");
  }
}

function pronunciate() {
  clearAll();
  $.get(
    "/pronunciation/search",
    {
      word: $("#word_dst").val(),
      target: $("#target").val(),
    },
    function (data) {
      $("#result_search").html(data);
      if ($("#recording option").length < 1) {
        $("#load_audio_btn").click();
      }
    }
  );
}

function word_list() {
  $.get(
    "/vocabulary/word_list",
    {
      word_list: $("#word_list").val(),
    },
    function (data) {
      $("#result_word_list").html(data);
    }
  );
}

function replace_word_src(event) {
  word = event.target.getAttribute("data-word");
  $("#word_src").val(word);
  $("#" + event.target.id).remove();
}

function load_image() {
  var offset = $("#image img").length;
  $.get(
    "/image_search",
    {
      word: $("#word_dst").val(),
      target: $("#target").val(),
      offset: offset,
    },
    function (data) {
      $("#image").append(data);
    }
  );
}

function addAudio() {
  $.get(
    "/audio/add",
    {
      word: $("#word_dst").val(),
      target: $("#target").val(),
    },
    function (data) {
      $("#recording").append(data);
    }
  );
}

function displaySentence() {
  $("#choose_sentence_result").text($("#word_dst").val());
  $("#choose_sentence_description").html(
    '<br> Select part of the sentence and click Select <br>     <button onclick="selectSentence()" id="select_sentence">Select</button>'
  );
}

function selectSentence() {
  text_part = window.getSelection().toString();
  if (text_part == "") {
    window.alert("You didn't choose anything");
    return;
  }

  $.get("/sentences/search", {}, function (data) {
    $("#select_sentence_result").append(data);
    $("#front").val($("#definition").data("definition"));
  });
  $("#choose_sentence_description").html(
    "You chose : <em id='text_part'>" + text_part + "</em>"
  );
}

function add_sentences() {
  $.get(
    "/sentences/add/",
    {
      text_full: $("#word_dst").val(),
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
      $("#choose_sentence_result").html("");
      $("#choose_sentence_description").html("");
      $("#select_sentence_result").html("");
    }
  );
}
function searchAbstractWord() {
  $.get(
    "/vocabulary/abstract_word/",
    {
      word_src: $("#word_src").val(),
      word_dst: $("#word_dst").val(),
      detail: $("#word_dst option:selected").text(),
      target: $("#target").val(),
    },
    function (data) {
      var newDoc = document.open("text/html", "replace");
      newDoc.write(data);
      newDoc.close();
    }
  );
}

function replace_word_dst(event) {
  $("#word_dst").val(event.target.getAttribute("data-word"));
}

function pasteWatch() {
  const sel = "#image";
  $(sel)
    .pastableNonInputable()
    .off("pasteImage")
    .on("pasteImage", function (e, data) {
      $("<img />")
        .attr("src", data.dataURL)
        .attr("onclick", "selectImage(event)")
        .addClass("selected")
        .appendTo(sel);
      console.log(data);
    });
}

setInterval(pasteWatch, 500);
