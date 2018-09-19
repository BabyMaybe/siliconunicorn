const tagList = document.getElementById("tag-list");
const newTag = document.getElementById("new-tag");
let currentTags = [];

window.addEventListener("load", getCurrentTags);
newTag.addEventListener("keydown", newTagKey);
tagList.addEventListener("click", removeTag);

function newTagKey(e) {
    // e.preventDefault();

    if (e.key === "Tab" || e.key === "Enter") {
        e.preventDefault();
        let newTagText = "#" + this.value.replace(/ /g, "");
        if (!currentTags.includes(newTagText)) {
            currentTags.push(newTagText);
            addTag(newTagText);
        }
        this.value = "";
    }
}

function addTag(newTagText) {
    t = document.createElement("li");
    t.className = "blog-tag";
    t.innerHTML = `<a>${newTagText}</a>`;

    tagList.insertBefore(t, newTag);
}

function getCurrentTags() {
    currentTags = [...document.getElementsByClassName("blog-tag")];
    currentTags.pop();
    currentTags = currentTags.map(bt => bt.textContent);
}

let t;
function removeTag(e) {
    e.preventDefault();
    let target = e.target;
    let tag = e.target.closest("li.blog-tag");
    t = target;
    if (tag) {
        let index = currentTags.indexOf(target.textContent);
        currentTags.splice(index, 1);
        tagList.removeChild(tag);
        console.log(currentTags);
    }
}
