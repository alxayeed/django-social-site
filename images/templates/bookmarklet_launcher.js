(function () {
    if (window.myBookmarklet !== undefined) {
        console.log('hello');
        myBookmarklet();
    }
    else {

        document.body.appendChild(document.createElement('script')).src = 'https://127.0.0.1:8000/static/js/bookmarklet.js?r=' + Math.floor(Math.random() * 99999999999999999999);
    }
})();

        // that s single semicolon up there after line 3, that costs me 1 hour today!hail javascript!hail jquery!!