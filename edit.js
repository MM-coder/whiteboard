(function() {
  'use strict'

  var addRanges = function(a, b, off) {
    var result = a.slice(0, -1);
    var bStart = 0;
    if (a.length && b.length && a[a.length - 1][1] == off - 1 && b[0][0] == 0) {
      // Overlap
      result.push([a[a.length - 1][0], b[0][1] + off]);
      bStart++; // Don't copy first interval of b
    } else if (a.length) {
      // No overlap
      result.push(a[a.length - 1]);
    }
    for (var i = bStart; i < b.length; i++)
      result.push([b[i][0] + off, b[i][1] + off]);
    return result;
  };

  var Line = function(text, bold, italic) {
    this.text = text;
    this.bold = bold;
    this.italic = italic;
  };

  Line.prototype.equals = function(other) {
    return this.text == other.text
      && this.bold == other.bold
      && this.italic == other.italic;
  };

  Line.prototype.concat = function(other) {
    return new Line(this.text + other.text,
      addRanges(this.bold, other.bold, this.text.length),
      addRanges(this.italic, other.italic, this.text.length));
  };

  Line.prototype.toNode = function() {
    var p = document.createElement('p');
    var offset = 0;
    while (offset < this.text.length) {
      text =
    }
    return p;
  };

  Line.prototype.filterItalics = function(parent, start, end) {
    for (var i = 0; i < this.italic && this.italic[i][0] <= end; i++) {
      if (this.italic[i][1] < start) {
        continue;
      } else if (this.italic[i][0])
    }
  };

  var nodeToLine = function(node) {
    if (node instanceof Text) {
      return new Line(node.nodeValue, [], []);
    }
    var line = new Line('', [], []);
    for (var i = 0; i < node.childNodes.length; i++) {
      line = line.concat(nodeToLine(node.childNodes[i]));
    }
    var fullRange = [[0, line.text.length - 1]];
    if (node.tagName == 'B' || node.tagName == 'STRONG') {
      line.bold = fullRange;
    } else if (node.tagName == 'I' || node.tagName == 'EM') {
      line.italic = fullRange;
    }
    return line;
  };

  window.addEventListener('load', function() {
    var main = document.getElementsByTagName('main')[0];

    main.addEventListener('input', function(evt) {
      var nodes = main.getElementsByTagName('p');
      var lines = [];
      for (var i = 0; i < nodes.length; i++) {
        lines.push(nodeToLine(nodes[i]));
      };

      console.log(lines);
    });

    main.focus();
  });
})();
