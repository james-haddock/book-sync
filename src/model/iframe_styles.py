def get_iframe_styles():
    return '''body{overflow-x:hidden;}
    @media (prefers-color-scheme: dark) {
    body, p, h1, h2, h3, h4, h5, h6, a, span, pre, blockquote, ul, ol, li, table, tr, th, td, input, textarea, button, select, label, .some-custom-class {
        color: #ffffff; 
        background-color: #000000; 
        
    }

    a {
        color: #bb86fc;
    }
    svg text {
        fill: #ffffff;
    }

    input, textarea, button, select {
        background-color: #333;
        border: 1px solid #555;
        color: #ddd;
    }

    table {
        border-color: #555;
    }}
    th, td {
        border-color: #555;
    }}
    
    }}
    img {
        opacity: 0;
    transition: opacity 0.5s ease-in-out;
    }}

    img.loaded {
    opacity: 1;
    }'''