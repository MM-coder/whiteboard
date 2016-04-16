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
        timer = null;
      }
      if (fn !== undefined) {
        timer = setTimeout(fn, delay);
      }
    };
  };

  var http = function(method, url, data) {
    return new Promise(function (resolve, reject) {
      var xhr = new XMLHttpRequest();
      xhr.open(method, url);
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.onload = function(evt) {
        if (this.status >= 200 && this.status < 300) {
          resolve(this.response);
        } else {
          reject(evt);
        }
      };
      xhr.onerror = reject;
      xhr.send(JSON.stringify(data));
    });
  };

  window.addEventListener('load', function() {
    var title = document.getElementById('title');
    var text = document.getElementById('text');
    var status = document.getElementById('status');

    var save = (function() {
      var saveTimer = afterDelay();
      return function() {
        status.textContent = '';
        saveTimer(function() {
          http('PUT', '', {
            title: title.value,
            text: text.value,
          }).then(function(e) {
            status.textContent = '✔ Saved';
          }, function(e) {
            console.error(e);
            status.textContent = '✗ Error saving.';
          });
        }, 500);
      };
    })();


    if (text) {
      var updateRows = function() {
        text.setAttribute('rows', text.value.split("\n").length + 1 || 2);
      };
      updateRows();

      text.addEventListener('input', function() {
        updateRows();
        save();
      });

      text.addEventListener('keydown', function(evt) {
        if (evt.keyCode == 9) {
          evt.preventDefault();
          insertText(text, "\t");
        }
      });

      title.addEventListener('input', function() {
        save();
      });
    };
  });
})();
