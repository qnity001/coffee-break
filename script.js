function changeBackground(color) {
    document.body.style.backgroundColor = color;
    if (color === '#6F4E37' || color === '#4B2E20' || color == '#3A2C29')
    {
        document.querySelector(".coffee").style.color = '#EDE1D4';
    }
    opacity = 0.9;
}
function resetBackground() {
    document.body.style.backgroundColor = '#E3C8A8';
    document.querySelector(".coffee").style.color = '#3E2723';
}