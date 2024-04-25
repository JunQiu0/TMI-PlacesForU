console.log("Background script running");
//Create context menu to italicize text
chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
        id: "searchImage",
        title: "Buscar en PlacesForU",
        contexts: ["image"]
    });
    console.log("Context menu created");
});

//When context menu is clicked, send message to content script to italicize text
chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === "searchImage") {
        //La forma directa
        chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
            var currentIndex = tabs[0].index;
            chrome.tabs.create({
                url: "http://192.168.1.177:8080/placesforu/?image_url=" + info.srcUrl,
                index: currentIndex + 1
            });
        });

        //La forma alternativa (usando el content script)
        //chrome.tabs.sendMessage(tab.id, { action: "searchImage", image: info.srcUrl });
        
        console.log("Search image sent!");
    }
});