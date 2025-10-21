document.addEventListener("DOMContentLoaded", function () {
  const input = document.querySelector('input[name="inputmessage"]');
  if (input) {
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && e.shiftKey) {
        e.preventDefault(); // Stops Shift+Enter from doing anything
      }
    });
  }
});

window.addEventListener('load', function () {
  const container = document.querySelector('.MessageContainer');
  if (container) {
    container.scrollTop = container.scrollHeight;
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector(".inputbox form");
  const popup = document.getElementById("loading-popup");

  form.addEventListener("submit", function (e) {
    // Find which button triggered the submit
    const activeElement = document.activeElement;
    // If the mic button was clicked, show the popup
    if (
      activeElement &&
      activeElement.classList.contains("micbutton")
    ) {
      popup.style.display = "flex"; // show popup for voice input
    } else {
      popup.style.display = "none"; // hide popup for text input
    }
  });

  window.addEventListener("pageshow", function () {
    popup.style.display = "none"; // hide popup after reload/response
  });
});

function OpenPopup() {
  const popup = document.querySelector('#popup');
  const overlay = document.querySelector('#overlay');
  if (popup && overlay) {
    popup.style.display = 'block';
    overlay.style.display = 'block';
    document.body.classList.add('freeze-body');
  }
}

function ClosePopup() {
  const popup = document.querySelector('#popup');
  const overlay = document.querySelector('#overlay');
  if (popup && overlay) {
    popup.style.display = 'none';
    overlay.style.display = 'none';
    document.body.classList.remove('freeze-body');
  }
}