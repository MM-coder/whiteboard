(function() {
  'use strict'

  var insertText = function(elem, text) {
      var startPos = elem.selectionStart;
      var endPos = elem.selectionEnd;
      elem.value = elem.value.substring(0, startPos)
        + text
        + elem.value.substring(endPos);
      elem.selectionStart = elem.selectionEnd = startPos + text.length;
      elem.focus();
  };

  var afterDelay = function() {
    var timer = null;
    return function(fn, delay) {
      if (timer !== null) {
        clearTimeout(timer);
      }
      timer = setTimeout(fn, delay);
    };
  };

  var http = function(method, url, body) {
    return new Promise(function (resolve, reject) {
      var xhr = new XMLHttpRequest();
      xhr.open(method, url);
      xhr.onload = resolve;
      xhr.onerror = reject;
      xhr.send(body);
    });
  };

  window.addEventListener('load', function() {
    var area = document.getElementsByTagName('textarea')[0];

    var saveTimer = afterDelay();
    area.addEventListener('input', function() {
      saveTimer(function() {
        http('PUT', '/', area.value).then(function(e) {
          console.log(e.target.response);
        }, function(e) {
          console.error(e);
        });
    }, 1000);
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
