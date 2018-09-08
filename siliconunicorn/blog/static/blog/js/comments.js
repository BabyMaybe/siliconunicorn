const comments = document.getElementById("comments-list");

const editableComments = document.getElementsByClassName("comment-controls");
for (let i = 0; i < editableComments.length; i++) {
    editableComments[i].addEventListener("click", commentControls);
}

function commentControls(e) {
    const target = e.target;
    const commentContainer = target.closest("li");
    let endpoint = "";

    if (target.matches(".comment-edit")) {
        let comment = commentContainer.getElementsByClassName(
            "comment-content"
        )[0].firstElementChild;
        comment.contentEditable = true;
        comment.classList.add("editing");
        comment.focus();

        commentContainer.getElementsByClassName(
            "comment-controls"
        )[0].innerHTML = '<span class="comment-save"> | | | Save | | | </span>';
    }

    if (target.matches(".comment-save")) {
        endpoint = "/ajax/comment/edit";

        let comment = commentContainer.getElementsByClassName(
            "comment-content"
        )[0].firstElementChild;
        comment.contentEditable = false;
        comment.classList.remove("editing");

        commentContainer.getElementsByClassName(
            "comment-controls"
        )[0].innerHTML = `<span class="comment-edit">\\ \\ \\ Edit \\ \\ \\</span>
            <span class="comment-delete">: : Delete: :</span >`;

        // send form
        let data = {
            cid: commentContainer.dataset.cid,
            content: commentContainer.getElementsByTagName("p")[0].textContent
        };

        fetch(endpoint, {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "X-CSRFToken": Cookies.get("csrftoken"),
                Accept: "application/json",
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest"
            },
            body: JSON.stringify(data)
            // data: JSON.stringify(data)
        });
    }

    if (target.matches(".comment-delete")) {
        endpoint = "/ajax/comment/delete";

        let data = {
            cid: commentContainer.dataset.cid,
            active: false
        };

        comments.removeChild(commentContainer);

        fetch(endpoint, {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "X-CSRFToken": Cookies.get("csrftoken"),
                Accept: "application/json",
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest"
            },
            body: JSON.stringify(data)
            // data: JSON.stringify(data)
        })
            .then(function(response) {
                return response.json();
            })
            .then(function(data) {
                console.log(JSON.stringify(data));
            });
    }
}

document
    .getElementById("post-hearts")
    .firstElementChild.addEventListener("click", heartControls);

function heartControls(e) {
    const pid = this.dataset.pid;
    const heartNum = this.firstElementChild;

    let data = { pid: pid };

    fetch("/ajax/post/heart", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": Cookies.get("csrftoken"),
            Accept: "application/json",
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        },
        body: JSON.stringify(data)
    })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            if (data.hearted === "hearted") {
                heartNum.textContent = parseInt(heartNum.textContent) + 1;
            } else {
                heartNum.textContent = parseInt(heartNum.textContent) - 1;
            }
        });
}

const newCommentButton = document.getElementById("comment-submit");
newCommentButton.addEventListener("click", addComment);

function addComment(e) {
    e.preventDefault();

    console.log("adding comment");
    const form = new FormData(document.getElementById("comment-form"));

    const pid = this.dataset.pid;

    let data = {
        pid: pid,
        content: form.get("content"),
        display_author: form.get("display_author"),
        csrfmiddleware: Cookies.get("csrftoken")
    };

    fetch("/ajax/comment/add", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": Cookies.get("csrftoken"),
            Accept: "application/json",
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        },
        body: JSON.stringify(data)
    })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            if (data.status === "success"):
            let newComment = document.createElement('li');
                let newCommentHTML =
                `<li class="comment-container" data-cid="${ data.cid }">
                    <div class="comment-info ${ data.isAuthor ? 'author' : '' }">
                        ${ data.isAnonymous ? `<span class="unregistered">(unregistered user)</span>
                        < span class="comment-username anon"> ${ data.display_author } </span >` : ''}
                        ${ data.isAuthor ? `<span class="comment-username author">${ data.display_author }</span>` : ''}
                        ${ !data.isAuthor && !data.isAnonymous ? `<span class="comment-username user">${ data.display_author }</span>` : ''}
                        <div class="comment-date-heart">
                            <div class="comment-date-time">
                                <span class="comment-date">${ data.timestamp }</span>
                                <span class="comment-time">${ data.timestamp }</span>
                            </div>
                            <div class="comment-heart">
                                <span>0</span>
                                <i class="far fa-heart ${ data.isAuthor ? 'author' : ''}"></i>
                            </div>
                        </div>
                    </div>
                    <div class="comment-background skewed ${ data.isAuthor ? 'author' : ''}"></div>
                    <div class="comment-content">
                        <p>${ data.content }</p>
                    </div>
                    <div class="comment-controls-background comment-controls-edit skewed"></div>
                    <div class="comment-controls-container">
                        <div class="comment-controls">
                            <span class="comment-edit">\ \ \ Edit \ \ \</span>
                            <span class="comment-delete">: : Delete : :</span>
                        </div>
                    </div>
                </li>`
            newComment.innerHTML = newCommentHTML;
            comments.appendChild(newComment);
        });
}
