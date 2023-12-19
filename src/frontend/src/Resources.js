import React from 'react';

function Item(props) {
    return (
    <div className="item" >
        <a href={props.url} class="item">
          <img src={props.thumbnail} alt={props.title} />
          <h2>{props.title}</h2>
        <p>{props.description}</p>
        </a>
    </div>
  );
}

export default Item;