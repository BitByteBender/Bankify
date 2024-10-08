// button.js

function createButton(text, onClick) {
    const button = document.createElement('button');
    button.textContent = text;
    button.onclick = onClick;
    return button;
}

// Example usage
// const myButton = createButton('Click Me', () => alert('Button Clicked!'));
// document.body.appendChild(myButton);