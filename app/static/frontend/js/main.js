/**
 * Sets up Justified Gallery.
 */
if (!!$.prototype.justifiedGallery) {
  var options = {
    rowHeight: 140,
    margins: 4,
    lastRow: "justify"
  };
  $(".article-gallery").justifiedGallery(options);
}

function el(cls_or_id) {
  return document.querySelector(cls_or_id);
}

document.addEventListener('DOMContentLoaded', () => {

  /**
   * Shows the responsive navigation menu on mobile.
   */
  el("#header > #nav > ul > .icon")?.addEventListener('click', () => {
    el("#header > #nav > ul").classList.toggle("responsive");
  });


  /**
   * Controls the different versions of  the menu in blog post articles 
   * for Desktop, tablet and mobile.
   */
  if (document.querySelectorAll('.post').length) {
    const menu = el('#menu')
    const nav = el("#menu > #nav"); 
    const menuIcon = Array.from(document.querySelectorAll("#menu-icon, #menu-icon-tablet"));
    /**
     * Display the menu on hi-res laptops and desktops.
     */
    addEventListener("resize", (event) => {
      if (window.innerWidth >= 1440) {
        menu.style.visibility = "visible";
        menuIcon.forEach((mIcon) => mIcon.classList.add("active"));
      }
    });

    /**
     * Display the menu if the menu icon is clicked.
     */
    menuIcon.forEach((mIcon) => {
      mIcon.addEventListener('click', () => {
        if (menu.style.visibility === "hidden") {
          menu.style.visibility = "visible";
          menuIcon.forEach((mIcon) => mIcon.classList.add("active"));
        } else {
          menu.style.visibility = "hidden";
          menuIcon.forEach((mIcon) => mIcon.classList.remove("active"));
        }
        return false;
      });
    })
    

    /**
     * Add a scroll listener to the menu to hide/show the navigation links.
     */
    if (menu) {
      window.addEventListener("scroll", (event) => {
        const menuRect = menu.getBoundingClientRect(); 
        var topDistance = menuRect.top + window.scrollY;

        // hide only the navigation links on desktop
        if (nav.style.display !== 'block' && topDistance < 50) {
          nav.style.display = 'block';
        } else if (nav.style.display === 'block' && topDistance > 100) {
          nav.style.display = 'none';
        }

        // on tablet, hide the navigation icon as well and show a "scroll to top
        // icon" instead
        if (el('#menu-icon').style.display !== 'block' && topDistance < 50) {
          el("#menu-icon-tablet").style.display = "block";
          el("#top-icon-tablet").style.display = "none";
        } else if (el('#menu-icon').style.display !== 'block' && topDistance > 100) {
          el("#menu-icon-tablet").style.display = "none";
          el("#top-icon-tablet").style.display = "block";
        }
      });

      el('#top-icon-tablet').addEventListener('click', () => {
        scrollToTop(100);
      })
    }

    /**
     * Show mobile navigation menu after scrolling upwards,
     * hide it again after scrolling downwards.
     */
    if (el("#footer-post")) {
      var lastScrollTop = 0;
      window.addEventListener("scroll", (event) => {
        var topDistance = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;

        if (topDistance > lastScrollTop){
          // downscroll -> show menu
          el("#footer-post").style.display = 'none';
        } else {
          // upscroll -> hide menu
          el("#footer-post").style.display = 'block';
        }
        lastScrollTop = topDistance;

        // close all submenu"s on scroll
        el("#nav-footer").style.display = 'none';
        el("#toc-footer").style.display = 'none';
        el("#share-footer").style.display = 'none';

        // show a "navigation" icon when close to the top of the page, 
        // otherwise show a "scroll to the top" icon
        if (topDistance < 50) {
          el("#actions-footer > #top").style.display = 'none';
        } else if (topDistance > 100) {
          el("#actions-footer > #top").style.display = 'block';
        }
      });
    }
  }
});
function scrollToTop (duration) {
    // cancel if already on top
    if (document.scrollingElement.scrollTop === 0) return;

    const totalScrollDistance = document.scrollingElement.scrollTop;
    let scrollY = totalScrollDistance, oldTimestamp = null;

    function step (newTimestamp) {
        if (oldTimestamp !== null) {
            // if duration is 0 scrollY will be -Infinity
            scrollY -= totalScrollDistance * (newTimestamp - oldTimestamp) / duration;
            if (scrollY <= 0) return document.scrollingElement.scrollTop = 0;
            document.scrollingElement.scrollTop = scrollY;
        }
        oldTimestamp = newTimestamp;
        window.requestAnimationFrame(step);
    }
    window.requestAnimationFrame(step);
}

// $('#???').toggle() ==> vanilla Js
const toggle = el => {
  const ele = document.querySelector(el)
  if (ele.style.display === 'none') {
    ele.style.display = null
  } else {
    ele.style.display = 'none'
  }
}