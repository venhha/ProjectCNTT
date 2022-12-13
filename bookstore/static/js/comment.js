var cmt = document.getElementById("comment");

cmt.addEventListener("submit", function () {
  var text = document.getElementById("textarea").value;
  var oID = this.dataset.order;
  var action = this.dataset.action;

  console.log("text:", text, "action:", action, "oID:", oID);
  console.log("USER:", user);

  comment(text, action, oID);
  alert_success();
  back_home();
});

function clickcmt() {
  console.log("user comment!");
  var text = document.getElementById("textarea").value;
  var oID = this.dataset.order;
  var action = this.dataset.action;

  console.log("text:", text, "action:", action, "oID:", oID);
  console.log("USER:", user);

  comment(text, action, oID);
  alert_success();
  back_home();
}

function comment(text, action, oID) {
  console.log("(comment) User is authenticated, sending data...");
  var url = "http://127.0.0.1:8000/comment/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ text: text, action: action, oID: oID }),
  })
    .then((response) => {
      return response.json();
    })

    .then((data) => {
      console.log("data:", data);
      //console.debug;
      location.reload();
    });
}

function alert_success() {
  alert("Cảm ơn bạn đã đánh giá sản phẩm");
}

function back_home() {
  location.replace("http://127.0.0.1:8000/");
}
