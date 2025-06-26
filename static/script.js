
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



