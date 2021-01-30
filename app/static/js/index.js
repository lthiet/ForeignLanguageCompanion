function clearAll() {
  $("#image").html("");
  $('input[type=text]').each(function (index) {
    $(this).val('');
  });
  $('select')
    .not("#word_list")
    .not("#deck")
    .not("#target")
    .each(function () {
      $(this).html('');
    });
  $('#entry_form datalist').each(function () {
    $(this).html('');
  });

}

function translate() {
  $.get(
    "/vocabulary/translate", {
      word: $("#word_src").val(),
      target: $("#target").val(),
    },
    function (data) {
      $("#result_translate").html(data);
    }
  );
}

function search() {
  console.log(
    $("#word_dst").val()
  );
  $.get(
    "/vocabulary/search", {
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

function running_status_element(ident) {
  var element = document.createElement("div");
  element.id = ident
  element.innerHTML = ident
  element.classList.add("running");
  var interval;
  var check_thread_status = function () {
    $.get(
      "/thread_status/" + ident, {},
      function (response) {
        if (response == 'running') {
          $("#" + ident).attr("class", "running");
        } else {
          $("#" + ident).attr("class", "done");
          setTimeout(function () {
            clearInterval(interval);
            $("#" + ident).remove();
          }, 500);
        }
      }
    )
  }
  interval = setInterval(
    check_thread_status,
    2000)
  return element
}


function add_vocabulary() {
  $.get(
    "/vocabulary/add", {
      word: $("#word_dst").val(),
      ipa: $("#ipa").val(),
      word_usage: $("#word_usage").val(),
      recording: $("#recording").val(),
      spelling: $("#spelling").is(':checked'),
      images: $(".selected")
        .map(function () {
          // return this.src;
          return this.dataset.content;
        })
        .get(),
      deck: $("#deck").val(),
    },
    function (data) {
      $("#thread_status").append(running_status_element(data));
      clearAll();
    }
  );
}

function add_pronunciation() {
  $.get(
    "/pronunciation/add", {
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
    "/pronunciation/search", {
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
    "/vocabulary/word_list", {
      word_list: $("#word_list").val(),
    },
    function (data) {
      $("#result_word_list").html(data);
    }
  );
}

function add_from_word_list(event) {
  word = event.target.getAttribute("data-word");
  is_en = event.target.getAttribute("data-is_en") == "True";
  if (is_en)
    $("#word_src").val(word);
  else
    $("#word_dst").val(word);

  $("#" + event.target.id).remove();
}

function load_image() {
  var offset = $("#image img").length;
  $.get(
    "/image_search", {
      word: $(".input_image").val(),
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
    "/audio/add", {
      word: $(".input_audio").val(),
      target: $("#target").val(),
    },
    function (data) {
      $("#recording").append(data);
    }
  );
}


function searchAbstractWord() {
  $.get(
    "/vocabulary/abstract_word/", {
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
      $.post("/image/upload", data.dataURL, function (res) {
        $(sel).prepend(res);
      });
      // $("<img />")
      //   .attr("src", data.dataURL)
      //   .attr("onclick", "selectImage(event)")
      //   .addClass("selected")
      //   .appendTo(sel);
      // console.log(data);
    });
}

setInterval(pasteWatch, 500);