function clearAll() {
  $(".form_container").html("");
}

function translate() {
  clearAll();
  $.get(
    "/vocabulary/translate",
    {
      word: $("#word_src").val(),
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
    },
    function (data) {
      $("#result_search").html(data);
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
      word: $("#word").val(),
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
      word: $("#word").val(),
    },
    function (data) {
      $("#result_search").html(data);
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

function replace_word(event) {
  word = event.target.id;
  $("#word_src").val(word);
  $("#" + word).remove();
}

function load_image() {
  var offset = $("#image img").length;
  $.get(
    "/image_search",
    {
      word: $("#word_dst").val(),
      offset: offset,
    },
    function (data) {
      $("#image").append(data);
    }
  );
}
