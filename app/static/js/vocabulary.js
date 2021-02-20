function add_simple_vocabulary() {
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

function add_abstract_vocabulary() {
  $.get(
    "/sentences/add/", {
      text_full: $("#example").val(),
      recording: $("#recording").val(),
      text_part: $("#word_dst").val(),
      images: $(".selected")
        .map(function () {
          return this.dataset.content;
        })
        .get(),
      deck: $("#deck").val(),
      front: $("#definition").val(),

      // TODO: this
      twocard: true,
      guess_syntax: false
    },
    function (data) {
      $("#thread_status").append(running_status_element(data));
    }
  );
}

function addExamples() {
  $.get(
    "/vocabulary/examples", {
      word_dst: $("#word_dst").val(),
      word_src: $("#word_src").val(),
      target: $("#target").val(),
    },
    function (data) {
      var loc = "#examples_result"
      $(loc).html('');
      $.each(data, function (i, val) {
        console.log(val);
        var $button = $("<button>")
          .html(val.dst_example)
          .click(function () {
            $("#example")
              .val($(this).text())
              .attr("data-inputimage", val.src_example);
            $.get("/translate/", {
              "text": $("#definition").attr('data-english'),
              "src": "en",
              "dst": $("#target").val()
            }, function (data) {
              $("#definition")
                .val(data)
            })
          })
        $(loc).append($button);
        $(loc).append($("<br/>"));

      })
    }
  );
}