import React from "react";
import ReactDOM from "react-dom/client";

import Item from "./Resources";
import "./styles.css"

// Get items and put them in the div with id "items"
function getItems() {
    try{
        let data = fetch("http://127.0.0.1:8000/tutorials")
        .then(response => response.json())
        .then(data => {
            const items_html = data.map(item => {
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
            root.render(
                <div className="items">
                    {items_html}
                </div>
            );
        }
        );
    } catch (error) {
        console.log(error);
    }
}

const root = ReactDOM.createRoot(document.getElementById("root"));
console.log(getItems());