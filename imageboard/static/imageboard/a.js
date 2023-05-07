$.extend($.ui.autocomplete, {
  filter: function (array, term) {
    var arraySub = term.split(" ");

    var regEx = "^";
    regEx +=
      "(?=.*" +
      $.ui.autocomplete.escapeRegex(arraySub[arraySub.length - 1]) +
      ".*)";
    regEx += ".*$";

    var matcher = new RegExp(regEx, "i");
    return $.grep(array, function (value) {
      return matcher.test(value.label || value.value || value);
    });
  },
});
$.widget("ui.autocomplete", $.ui.autocomplete, {
  _renderItem: function (ul, item) {
    var arraySub = this.term.split(" ");

    var regEx = "";
    for (i = 0; i < arraySub.length; i++) {
      if (i == 0) {
        regEx += "(";
      } else {
        regEx += "|(";
      }
      regEx += $.ui.autocomplete.escapeRegex(arraySub[i]) + ")";
    }

    return $("<li>")
      .append(
        $("<div>").html(
          item.label.replace(
            new RegExp(regEx, "gi"),
            '<span class="ui-autocomplete-term">$&</span>'
          )
        )
      )
      .appendTo(ul);
  },
});
