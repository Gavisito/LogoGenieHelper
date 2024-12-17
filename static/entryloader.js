window.addEventListener('load', () => {
    const entryloader = document.querySelector('.entry-loader');
    setTimeout(() => {
    entryloader.classList.add('entry-loader--hidden');
}, 1500);
});

//place button onclick action here
function entryloader() {
    const entryloader = document.querySelector('.entry-loader');
    entryloader.classList.remove('entry-loader--hidden');
    setTimeout(() => {
        entryloader.classList.add('entry-loader--hidden');
    }, 2500);
}