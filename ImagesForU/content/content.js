console.log("Content script running")
// When we receive the italicize message from the background script, we
// italicize the page.
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  console.log("Message received: " + request.action);
  if (request.action === "searchImage") {
    //window.open(request.image, "_blank"); //Para ver la imagen
    
    window.open("http://192.168.1.177:8080/placesforu/?image_url=" + request.image, "_blank");
  }
});
