document.addEventListener("DOMContentLoaded", function () {
          var copyButtons = document.querySelectorAll(".btn");
  
          copyButtons.forEach(function (button) {
              button.addEventListener("click", function () {
                  var levelId = button.getAttribute("data-level-id");
                  copyToClipboard(levelId);
              });
          });
      });
  
      function copyToClipboard(text) {
          var textarea = document.createElement("textarea");
          textarea.value = text;
          document.body.appendChild(textarea);
          textarea.select();
          document.execCommand("copy");
          document.body.removeChild(textarea);
          alert();
      }