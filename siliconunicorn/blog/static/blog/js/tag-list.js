const tagList = document.getElementById('tag-list');
const newTag = document.getElementById('new-tag');
let currentTags = [];

window.addEventListener('load', getCurrentTags);
newTag.addEventListener('keydown', newTagKey);
tagList.addEventListener('click', removeTag);

function newTagKey(e) {
    // e.preventDefault();

    if (e.key === 'Tab' || e.key === 'Enter') {
        e.preventDefault();
        let newTagText = '#' + this.value.replace(/ /g,'');
        if (!currentTags.includes(newTagText)){
            currentTags.push(newTagText);
            addTag(newTagText);
        }
        this.value = '';
    }
}

function addTag(newTagText) {
    t = document.createElement('li');
    t.className = 'blog-tag'
    t.textContent = newTagText

    tagList.insertBefore(t, newTag);
}


function getCurrentTags() {
    currentTags = [...document.getElementsByClassName('blog-tag')];
    currentTags.pop();
    currentTags = currentTags.map( bt => bt.textContent );
}

let t;
function removeTag(e) {
    let target = e.target;
    t = target;
    if (target.tagName === 'LI' && target.className === 'blog-tag') {
        let index = currentTags.indexOf(target.textContent);
        currentTags.splice(index,1);
        tagList.removeChild(target);
        console.log(currentTags);

    }
}
