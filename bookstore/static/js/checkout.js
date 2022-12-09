
function press_submit() {
  var form = document.getElementById("form");
  form.addEventListener("click", function () {
    var addr = document.getElementById("ship_addr").value;
    var iID = this.dataset.invoice;
    //data-place_addr={{i.pID}} data-action="place"
    var action = this.dataset.action;
    console.log("place_addr:", addr, "action:", action, "iID:", iID);
    console.log("USER:", user);

    if (user == "AnonymousUser") {
      console.log("User is not authenticated");
    } else {
      placeOrder(addr, action, iID);
      alert_success();
      back_home();
    }
  });
}

var form = document.getElementById("form");
form.addEventListener("submit", function () {
  var addr = document.getElementById("ship_addr").value;
  var iID = this.dataset.invoice;
  //data-place_addr={{i.pID}} data-action="place"
  var action = this.dataset.action;
  console.log("place_addr:", addr, "action:", action, "iID:", iID);
  console.log("USER:", user);

  if (user == "AnonymousUser") {
    console.log("User is not authenticated");
  } else {
    placeOrder(addr, action, iID);
    alert_success();
    back_home();
  }
});

function placeOrder(addr, action, iID) {
  console.log("Place order");
  console.log("(checkout) User is authenticated, sending data...");
  var url = "http://127.0.0.1:8000/place/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ addr: addr, action: action, iID: iID }),
  })
    .then((response) => {
      return response.json();
    })

    .then((data) => {
      console.log("data:", data);
      console.debug;
      //location.reload()
    });
}

function alert_success() {
  alert("Bạn đã đặt hàng thành công");
}

function back_home() {
  location.replace("http://127.0.0.1:8000/");
}
