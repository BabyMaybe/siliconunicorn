const new_post = document.getElementById("new-post");
const btn = document.getElementById('new-post-submit');
const hiddenForm = document.getElementById('compiledForm');
let showHTML = false;

btn.addEventListener('click', function(e) {
    const title = document.getElementById('new-title').textContent;
    const content = new_post.innerHTML;

    hiddenForm.title.value = title;
    hiddenForm.content.value = content;
    hiddenForm.tags.value = currentTags.toString();
    console.table(hiddenForm.children, ['index','value']);
    hiddenForm.submit()
});

function initDoc() {
    document.execCommand("defaultParagraphSeparator", false, "p");
}
initDoc();

function formatDoc(cmd, value) {
    if (!showHTML)
    {
        document.execCommand(cmd, false, value);
        new_post.focus();
    }
}

function toggleDocMode(e) {
    showHTML = !showHTML;
    setDocMode(showHTML);
}

function setDocMode(viewSource) {
let content;
if (viewSource) {
    let iHTML = new_post.innerHTML;
    let reFirst = /(<p>|<ul>|<\/ul>|<\/li>)/g;
    let reSecond = /(<\/p>)/g;
    let formatted = iHTML.replace(reFirst, '$&\n').trim();
    formatted = formatted.replace(reSecond, '\n$&\n\n').trim();

    new_post.innerHTML = "";

    let code = document.createElement("code");
    code.id = "sourceText";
    code.contentEditable = true;
    code.innerText = formatted;

    new_post.contentEditable = false;
    new_post.appendChild(code);

    document.execCommand("defaultParagraphSeparator", false, "br");
} else {
    if (document.all) {
    new_post.innerHTML = new_post.innerText;
    } else {
    content = document.createRange();
    content.selectNodeContents(new_post.firstChild);
    new_post.innerHTML = content.toString();
    }
    new_post.contentEditable = true;
    document.execCommand("defaultParagraphSeparator", false, "p");
}
new_post.focus();
}
