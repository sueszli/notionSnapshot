/**
 * re-implement toggle buttons (we remove the original event listeners)
 */
const showToggle = (content, arrow) => {
  arrow.style.transform = "rotateZ(180deg)";
  content.style.display = "block";
};

const hideToggle = (content, arrow) => {
  arrow.style.transform = "rotateZ(90deg)";
  content.style.display = "none";
};

const toggleButtons = document.getElementsByClassName("notionsnapshot-toggle-button");
for (toggleButton of toggleButtons) {
  const toggleId = toggleButton.getAttribute("notionsnapshot-toggle-id");
  const toggleContent = document.querySelector(`.notionsnapshot-toggle-content[notionsnapshot-toggle-id='${toggleId}']`);
  const toggleArrow = toggleButton.querySelector("svg");
  if (toggleButton && toggleContent) {
    hideToggle(toggleContent, toggleArrow);
    toggleButton.addEventListener("click", () => {
      if (toggleContent.style.display == "none") {
        showToggle(toggleContent, toggleArrow);
      } else {
        hideToggle(toggleContent, toggleArrow);
      }
    });
  }
}

/**
 * re-implement anchor links (we remove the original event listeners)
 */
const anchorLinks = document.querySelectorAll("a.notionsnapshot-anchor-link");
for (anchorLink of anchorLinks) {
  const id = anchorLink.getAttribute("href").replace("#", "");
  const targetBlockId =
    id.slice(0, 8) + "-" + id.slice(8, 12) + "-" + id.slice(12, 16) + "-" + id.slice(16, 20) + "-" + id.slice(20);
  anchorLink.addEventListener("click", (e) => {
    e.preventDefault();
    console.log(targetBlockId);
    document.querySelector(`div[data-block-id='${targetBlockId}']`).scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  });
}


// sets all iframes' parent container opacity to 1
// originally notion has a callback to do that on iframe loaded
const pendingIframes = document.getElementsByTagName("iframe");
for (let i = 0; i < pendingIframes.length; i++) {
  pendingIframes.item(i).parentElement.style.opacity = 1;
}

// const pendingIframes = document.getElementsByClassName("notionsnapshot-iframe-target");
// for (let i = 0; i < pendingIframes.length; i++) {
//   const pendingIframe = pendingIframes.item(i);
//   const iframeSrc = pendingIframe.getAttribute("notionsnapshot-iframe-src");
//   const iframe = document.createElement("iframe");

//   pendingIframe.style.opacity = 0;
//   iframe.onload = () => {
//     pendingIframe.style.opacity = 1;
//   };

//   iframe.style.width = "100%";
//   iframe.style.height = "100%";
//   iframe.style.position = "absolute";
//   iframe.style.left = 0;
//   iframe.style.top = 0;
//   iframe.style.pointerEvents = "auto";

//   iframe.setAttribute("src", iframeSrc);
//   iframe.setAttribute("frameborder", "0");
//   iframe.setAttribute(
//     "sandbox",
//     "allow-scripts allow-popups allow-top-navigation-by-user-activation allow-forms allow-same-origin"
//   );

//   pendingIframe.appendChild(iframe);
// }

// hide search box on inline databases
// couldn't find a reliable way to do this in css
const collectionSearchBoxes = document.getElementsByClassName("collectionSearch");
for (let i = 0; i < collectionSearchBoxes.length; i++) {
  const collectionSearchBox = collectionSearchBoxes.item(i).parentElement;
  collectionSearchBox.style.display = "none";
}


// fix the problem with images having an annoying extra padding in Webkit renderers on iOS devices
const imgs = document.querySelectorAll("img:not(.notion-emoji)");
for (let i = 0; i < imgs.length; i++) {
  parent = imgs[i].parentElement
  let style = parent.getAttribute("style")
  style = style.replace(/padding-bottom: 133\.333\%;/, "")
  style = style + "; height:auto!important;"
  parent.setAttribute("style",  style);
}
