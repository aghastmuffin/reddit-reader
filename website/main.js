function dwnld(url) {
    document.getElementById('my_iframe').src = url;
      const paragraph = document.createElement('p');
    paragraph.textContent = "Give it a couple seconeds, but if that didn't work click";

    // Create a new anchor element
    const anchor = document.createElement('a');
    anchor.href = "https://github.com/aghastmuffin/reddit-reader/archive/refs/heads/main.zip";
    anchor.textContent = " here!";
    anchor.referrerPolicy = "no-referrer"; // Sets the referrer policy to 'no-referrer'

    // Append the anchor to the paragraph
    paragraph.appendChild(anchor);

    // Append the paragraph to the body of the document
    document.body.appendChild(paragraph);
};
function downloadraw(url) {
    fetch(url)
        .then(response => response.text())
        .then(data => {
            const blob = new Blob([data], { type: 'text/plain' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'guiv2.py';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => console.error('Error downloading the file:', error));
}
