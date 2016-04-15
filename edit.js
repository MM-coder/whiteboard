(function() {
  'use strict'

  var insertText = function(elem, text) {
      var startPos = elem.selectionStart;
      var endPos = elem.selectionEnd;
      elem.value = elem.value.substring(0, startPos)
        + text
        + elem.value.substring(endPos);
      elem.selectionStart = elem.selectionEnd = startPos + text.length;
  };

  window.addEventListener('load', function() {
    var area = document.getElementsByTagName('textarea')[0];

    area.addEventListener('input', function() {
      this.setAttribute('rows', this.value.split("\n").length + 1 || 2);
    });

    area.addEventListener('keydown', function(evt) {
      if (evt.keyCode == 9) {
        evt.preventDefault();
        insertText(area, "\t");
      }
    });
  });
})();
