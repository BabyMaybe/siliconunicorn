const new_post = document.getElementById("new-post");
const btn = document.getElementById("new-post-submit");
const hiddenForm = document.getElementById("compiledForm");
let showHTML = false;

btn.addEventListener("click", function(e) {
    const title = document.getElementById("new-title").textContent;
    const content = new_post.innerHTML;

    hiddenForm.title.value = title;
    hiddenForm.content.value = content;
    hiddenForm.tags.value = currentTags.toString();
    console.table(hiddenForm.children, ["index", "value"]);
    hiddenForm.submit();
});

function initDoc() {
    document.execCommand("defaultParagraphSeparator", false, "p");
}
window.addEventListener("load", initDoc);

function formatDoc(cmd, value) {
    // console.log("executing command", cmd, value);
    if (!showHTML) {
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
    let toggleButton = document.getElementById("htmlToggle");
    if (viewSource) {
        let iHTML = new_post.innerHTML;
        let reFirst = /(<p>|<ul>|<\/ul>|<\/li>)/g;
        let reSecond = /(<\/p>)/g;
        let formatted = iHTML.replace(reFirst, "$&\n").trim();
        formatted = formatted.replace(reSecond, "\n$&\n\n").trim();

        new_post.innerHTML = "";

        let code = document.createElement("code");
        code.id = "sourceText";
        code.contentEditable = true;
        code.innerText = formatted;

        new_post.contentEditable = false;
        new_post.appendChild(code);

        document.execCommand("defaultParagraphSeparator", false, "br");
        toggleButton.textContent = "Show Content";
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
        toggleButton.textContent = "Show HTML";
    }
    new_post.focus();
}

let selection = window.getSelection();
let range;

function addLink() {
    console.log("adding link");
    document
        .getElementById("modal-input-link")
        .classList.remove("modal-hidden");
    document.getElementById("modal-input-file").style.display = "none";

    document
        .getElementById("modal-ok")
        .addEventListener("click", confirmModalLink);

    document.getElementById("modal-input-link").value = "http://";

    range = selection.getRangeAt(0);
    openModal();
}

function addImage() {
    console.log("adding image");
    document.getElementById("modal-input-link").classList.add("modal-hidden");
    document.getElementById("modal-input-file").style.display = "flex";

    range = selection.getRangeAt(0);
    document
        .getElementById("modal-ok")
        .addEventListener("click", confirmModalImage);
    openModal();
}

function openModal() {
    document.getElementById("modal").classList.remove("modal-hidden");
}

function closeModal(e) {
    document.getElementById("modal").classList.add("modal-hidden");
}

function checkCloseModal(e) {
    target = e.target;

    if (target.matches("#modal") || target.matches("#modal-cancel")) {
        closeModal();
    }
}

function confirmModalLink() {
    selection.removeAllRanges();
    selection.addRange(range);

    let user_url = document.getElementById("modal-input").value;
    console.log(user_url);

    if (user_url && user_url != "" && user_url != "http://") {
        formatDoc("createlink", user_url);
    }

    document
        .getElementById("modal-ok")
        .removeEventListener("click", confirmModalLink);
    closeModal();
}

document
    .getElementById("id_docfile")
    .addEventListener("change", updateImageName);

function updateImageName() {
    document.getElementById(
        "modal-input-file-text"
    ).textContent = document.getElementById("id_docfile").files[0].name;
}

function confirmModalImage() {
    selection.removeAllRanges();
    selection.addRange(range);

    let file = document.getElementById("id_docfile").files[0];
    let image = document.getElementById("id_docfile").value;

    if (image && image != "") {
        imageUpload();
    }

    document
        .getElementById("modal-ok")
        .removeEventListener("click", confirmModalImage);
    closeModal();
}

function imageUpload() {
    console.log("tryna upload images");
    let img = document.getElementById("imageForm");
    let fd = new FormData(img);

    fetch("/ajax/image/upload", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": Cookies.get("csrftoken"),
            // Accept: "application/json",
            // "Content-Type": "multipart/form-data",
            "X-Requested-With": "XMLHttpRequest"
        },
        body: fd
    })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            formatDoc("insertImage", data.url);
        });
}

document
    .getElementById("modal-close-btn")
    .addEventListener("click", closeModal);
document.getElementById("modal").addEventListener("click", checkCloseModal);
