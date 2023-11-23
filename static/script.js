// Function to generate and add falling numbers to the document
function createFallingNumbers() {
    const container = document.querySelector('.falling-numbers-container');

    for (let i = 0; i < 50; i++) {
        const number = document.createElement('div');
        number.textContent = Math.floor(Math.random() * 2);
        number.classList.add('falling-numbers');
        number.style.left = `${Math.random() * 100}vw`;
        number.style.animationDuration = `${Math.random() * 3 + 1}s`;
        container.appendChild(number);
    }
}

$(document).ready(function(){
  // Add smooth scrolling to all links
  $(".scroll-link").on('click', function(event) {

    // Make sure this.hash has a value before overriding default behavior
    if (this.hash !== "") {
      // Prevent default anchor click behavior
      event.preventDefault();

      // Store hash
      var hash = this.hash;

      // Using jQuery's animate() method to add smooth page scroll
      // The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
      $('html, body').animate({
        scrollTop: $(hash).offset().top
      }, 500, function(){

        // Add hash (#) to URL when done scrolling (default click behavior)
        window.location.hash = hash;
      });
    } // End if
  });
}); 

createFallingNumbers();