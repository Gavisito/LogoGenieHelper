function dropdownmenu() {
    var links = document.querySelector('.links');

    if (links.style.display === 'none' || links.style.display === '') {
        links.style.display = 'flex';
    } else {
        links.style.display = 'none';
    }
}