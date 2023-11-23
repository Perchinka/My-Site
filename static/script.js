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

createFallingNumbers();

