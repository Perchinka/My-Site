import React from "react";
import ReactDOM from "react-dom/client";

import Item from "./Plate";

// Ask API for items (127.0.0.1:8000/tutorials)
function getItems() {
    return fetch("http://127.0.0.1:8000/tutorials")
        .then(response => response.json())
        .then(json => json.results);
}

// Render items
function renderItems(items) {
    const items_html = items.map(item => {
        return (
            <Item
                key={item.id}
                title={item.title}
                description={item.description}
                url={item.url}
                thumbnail={item.thumbnail}
            />
        );
    });
    ReactDOM.render(items_html, document.getElementById("root"));
}

// Get items and render them in div
getItems().then(renderItems);