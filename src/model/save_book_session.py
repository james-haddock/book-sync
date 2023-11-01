def save_book_session_js(UUID):
    return f"""
var bookUUID = "{UUID}";
document.documentElement.style.opacity = 0; // Initially hide content
window.onload = function() {{
  // All assets are now fully loaded, including images.

  // Select all significant content elements
  const contentElements = document.querySelectorAll(
    'p, h1, h2, h3, h4, h5, h6, li, span, strong, div, img, ' +
    'a, table, tr, th, td, ul, ol, blockquote, figure, figcaption, ' +
    'section, article, aside, header, footer, nav, time, mark, ' +
    'code, pre, q, cite, *[id]'
  );

  function saveTopElement() {{
    let topElementIndex = 0;
    let highestTop = -Infinity;
    contentElements.forEach((element, index) => {{
      const rect = element.getBoundingClientRect();
      // This element is the last one with its top above the viewport's top, making it the topmost element.
      if (rect.top < 0 && rect.top > highestTop) {{
        highestTop = rect.top;
        topElementIndex = index;
      }}
    }});
    localStorage.setItem('topElementIndex-' + bookUUID, topElementIndex.toString());
  }}

  function restoreScrollPosition() {{
    const topElementIndex = parseInt(localStorage.getItem('topElementIndex-' + bookUUID), 10);
    if (!isNaN(topElementIndex) && contentElements[topElementIndex]) {{
      // Use `scrollIntoView` with `block: 'start'` to align to the top of the viewport.
      contentElements[topElementIndex].scrollIntoView({{ block: 'start' }});
    }}
  }}

  window.addEventListener('scroll', saveTopElement, {{ passive: true }});
  window.addEventListener('resize', saveTopElement, {{ passive: true }});

  restoreScrollPosition(); // Call this immediately to restore position

  // Now that everything is loaded, we can fade in the content
  document.documentElement.style.transition = 'opacity 0.5s';
  document.documentElement.style.opacity = 1;
}};
"""
