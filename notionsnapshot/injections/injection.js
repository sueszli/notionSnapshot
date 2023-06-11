/**
 * re-implement toggle buttons
 */
const showToggle = (content, arrow) => {
    arrow.style.transform = 'rotateZ(180deg)'
    content.style.display = 'block'
}

const hideToggle = (content, arrow) => {
    arrow.style.transform = 'rotateZ(90deg)'
    content.style.display = 'none'
}

const toggleButtons = document.getElementsByClassName('notionsnapshot-toggle-button')
for (toggleButton of toggleButtons) {
    const toggleId = toggleButton.getAttribute('notionsnapshot-toggle-id')
    const toggleContent = document.querySelector(
        `.notionsnapshot-toggle-content[notionsnapshot-toggle-id='${toggleId}']`
    )
    const toggleArrow = toggleButton.querySelector('svg')
    if (toggleButton && toggleContent) {
        hideToggle(toggleContent, toggleArrow)
        toggleButton.addEventListener('click', () => {
            if (toggleContent.style.display == 'none') {
                showToggle(toggleContent, toggleArrow)
            } else {
                hideToggle(toggleContent, toggleArrow)
            }
        })
    }
}

/**
 * re-implement anchor links
 */
const anchorLinks = document.querySelectorAll('a.notionsnapshot-anchor-link')
for (anchorLink of anchorLinks) {
    const id = anchorLink.getAttribute('href').replace('#', '')
    const targetBlockId =
        id.slice(0, 8) + '-' + id.slice(8, 12) + '-' + id.slice(12, 16) + '-' + id.slice(16, 20) + '-' + id.slice(20)
    anchorLink.addEventListener('click', (e) => {
        e.preventDefault()
        console.log(targetBlockId)
        document.querySelector(`div[data-block-id='${targetBlockId}']`).scrollIntoView({
            behavior: 'smooth',
            block: 'start',
        })
    })
}

/**
 * set all iframes' parent container opacity to 1
 */
const pendingIframes = document.getElementsByTagName('iframe')
for (let i = 0; i < pendingIframes.length; i++) {
    pendingIframes.item(i).parentElement.style.opacity = 1
}

/**
 * hide search box on inline databases
 */
const collectionSearchBoxes = document.getElementsByClassName('collectionSearch')
for (let i = 0; i < collectionSearchBoxes.length; i++) {
    const collectionSearchBox = collectionSearchBoxes.item(i).parentElement
    collectionSearchBox.style.display = 'none'
}

/**
 * remove extra padding in Webkit renderers on iOS devices
 */
const imgs = document.querySelectorAll('img:not(.notion-emoji)')
for (let i = 0; i < imgs.length; i++) {
    parent = imgs[i].parentElement
    let style = parent.getAttribute('style')
    style = style.replace(/padding-bottom: 133\.333\%;/, '')
    style = style + '; height:auto!important;'
    parent.setAttribute('style', style)
}
