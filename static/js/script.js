document.addEventListener("DOMContentLoaded", function() {
  var editor = ace.edit("editor");
  editor.setTheme("ace/theme/monokai");
  editor.session.setMode("ace/mode/python");

  function runCode() {
      var code = editor.getValue();
      var output = code;
      appendToTerminal(output);
  }

  function appendToTerminal(output) {
      var terminalOutput = document.getElementById('terminal').querySelector('pre');
      terminalOutput.innerText += "\n" + output;
      terminalOutput.scrollTop = terminalOutput.scrollHeight;
  }

  function clearTerminal() {
      var terminalOutput = document.getElementById('terminal').querySelector('pre');
      terminalOutput.innerText = "Terminal:";
  }


  document.getElementById('runButton').addEventListener('click', runCode);

  document.getElementById('clearButton').addEventListener('click', clearTerminal);
});