def save_book_session_js(UUID):
    return f"""
var bookUUID = "{UUID}";

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
      contentElements[topElementIndex].scrollIntoView({{ block: 'start' }});
    }}
  }}

  window.addEventListener('scroll', saveTopElement, {{ passive: true }});
  window.addEventListener('resize', saveTopElement, {{ passive: true }});

  restoreScrollPosition();

  document.documentElement.style.transition = 'opacity 0.5s';
  document.documentElement.style.opacity = 1;
"""
