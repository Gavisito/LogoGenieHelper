window.addEventListener('load', () => {
    const entryloader = document.querySelector('.entry-loader');
    setTimeout(() => {
    entryloader.classList.add('entry-loader--hidden');
}, 1500);

        entryloader.addEventListener('transitionend', () => {
            document.body.removeChild(entryloader);
        });
});
