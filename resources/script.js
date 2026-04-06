// Convert vertical scroll → horizontal (except during Ctrl zoom)
window.addEventListener("wheel", (ev) => {
    if (ev.ctrlKey) return;
    ev.preventDefault();
    window.scrollBy({ left: ev.deltaY * 0.5, behavior: "auto" });
}, { passive: false });

/* ============================================================
   Safe HTML-aware soft hyphenation without HTML escaping
   ============================================================ */

function softHyphenateWord(word) {
    return word.replace(/(.{6})/g, "$1\u00AD");   // ← REAL SOFT HYPHEN
}

function softHyphenateText(text) {
    return text.replace(/([A-Za-zæøåÆØÅ]{8,})/g, softHyphenateWord);
}

function processNode(node) {
    if (node.nodeType === Node.TEXT_NODE) {
        // Replace the node content IN PLACE
        node.nodeValue = softHyphenateText(node.nodeValue);
        return;
    }
    for (let child of node.childNodes) {
        processNode(child);
    }
}

document.getElementById("wrapper").addEventListener("paste", function (ev) {
    ev.preventDefault();

    let html = ev.clipboardData.getData("text/html");
    let text = ev.clipboardData.getData("text/plain");

    // Case 1: HTML paste available (Word, browsers, PDFs, etc.)
    if (html) {
        let div = document.createElement("div");
        div.innerHTML = html;

        // Modify DOM in place
        processNode(div);

        // Insert DOM, not escaped HTML
        while (div.firstChild) {
            this.appendChild(div.firstChild);
        }
        return;
    }

    // Case 2: Plain text only
    document.execCommand("insertHTML", false, softHyphenateText(text));
});
