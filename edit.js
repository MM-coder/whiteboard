(function() {
  'use strict'

  window.addEventListener('load', function() {
    var area = document.getElementsByTagName('textarea')[0];

    area.addEventListener('input', function() {
      this.setAttribute('rows', this.value.split("\n").length + 1 || 2);
    });

    area.addEventListener('keydown', function(evt) {
      if (evt.keyCode == 9) {
        evt.preventDefault();
        var startPos = this.selectionStart;
        var endPos = this.selectionEnd;
        this.value = this.value.substring(0, startPos)
          + "\t"
          + this.value.substring(endPos, this.value.length);
        this.selectionStart = this.selectionEnd = startPos + 1;
      }
    });
  });
})();
