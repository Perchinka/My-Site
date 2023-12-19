import React from 'react';

function Item(props) {
  // TODO visible func for item
    return (
    <div className="item" >
        <a href={props.url} class="item">
        <img src={"data:image/png;base64"+ props.thumbnail} alt={props.title} />
        <h2>{props.title}</h2>
        <p>{props.description}</p>
        </a>
    </div>
  );
}

export default Item;