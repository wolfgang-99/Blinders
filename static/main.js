function playAudio(text, priority) {
    var el = document.createElement("div");
    var id = "speak-" + Date.now();
    el.setAttribute("id", id);
    el.setAttribute("aria-live", priority || "polite");
    el.classList.add("visually-hidden");
    document.body.appendChild(el);

    window.setTimeout(function () {
      document.getElementById(id).innerHTML = text;
    }, 100);

    window.setTimeout(function () {
        document.body.removeChild(document.getElementById(id));
    }, 1000);
}

function buttonChange() {
  var x = document.getElementById("hide");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}
// function copyText() {
//   var content = document.getElementById('content').innerText;
//   var textarea = document.createElement('textarea');
//   textarea.value = content;
//   document.body.appendChild(textarea);
//   textarea.select();
//   document.execCommand('copy');
//   document.body.removeChild(textarea);
//   alert('All text copied to clipboard!');
// }
// document.getElementById("audioload").innerHTML = "Screen Width: " + screen.width;
