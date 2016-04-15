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

    var setStatus = (function(message) {
      var statusTimer = afterDelay();
      return function(message, timeout) {
        status.textContent = message;
        if (timeout !== undefined) {
          statusTimer(function() {
            status.textContent = '';
          }, timeout);
        } else {
          statusTimer();
        };
      };
    })();

    var save = (function() {
      var saveTimer = afterDelay();
      return function() {
        saveTimer(function() {
          http('PUT', '', {
            title: title.value,
            text: text.value,
          }).then(function(e) {
            setStatus('Saved.', 2000);
          }, function(e) {
            console.error(e);
            setStatus('Error saving.');
          });
        }, 500);
      };
    })();

    title.addEventListener('input', function() {
      save();
    });

    text.addEventListener('input', function() {
      save();
      this.setAttribute('rows', this.value.split("\n").length + 1 || 2);
    });

    text.addEventListener('keydown', function(evt) {
      if (evt.keyCode == 9) {
        evt.preventDefault();
        insertText(text, "\t");
      }
    });
  });
})();
