const comments = document.getElementById("comments-list");
comments.addEventListener("click", commentControls);

const test = document.getElementById("ajax");

function commentControls(e) {
    let target = e.target;
    let commentContainer = target.closest("li");
    let endpoint = "";
    let data = {
        cid: commentContainer.dataset.cid,
        active: true,
        content: commentContainer.getElementsByTagName("p")[0].textContent
    };

    if (target.classList.contains("comment-edit")) {
        console.log("edit clicked");
    }

    if (target.classList.contains("comment-delete")) {
        console.log("delete clicked");
        // comments.removeChild(commentContainer);
        endpoint = "/ajax/test";
        data.active = false;
    }

    if (target.classList.contains("fa-heart")) {
        console.log("heart clicked");
        console.log(commentContainer.dataset.cid);
    }

    fetch(endpoint, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": Cookies.get("csrftoken"),
            Accept: "application/json",
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        },
        body: JSON.stringify(data),
        data: JSON.stringify(data)
    })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            console.log(JSON.stringify(data));
        });
}

test.addEventListener("click", ajaxTest);

function ajaxTest() {
    let myData = {
        hello: 1,
        cat: "goldberry",
        fluff: "bombadil",
        comment: "the comment id",
        author: "comment author id"
    };

    console.log("clicked ajax");

    fetch("/ajax/test", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": Cookies.get("csrftoken"),
            Accept: "application/json",
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        },
        body: JSON.stringify(myData),
        data: JSON.stringify(myData)
    })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            console.log(JSON.stringify(data));
        });
}
