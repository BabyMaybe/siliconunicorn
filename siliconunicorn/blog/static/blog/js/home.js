const hearts = document.getElementsByClassName("blog-hearts");

for (let i = 0; i < hearts.length; i++) {
    hearts[i].addEventListener("click", heartControls);
}

function heartControls(e) {
    console.log("tryna heart");
    console.log(this);
    console.log(this.dataset);
    console.log(this.dataset.pid);
    const target = e.target;

    const pid = this.dataset.pid;
    const heartNum = this.firstElementChild.firstElementChild;

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
