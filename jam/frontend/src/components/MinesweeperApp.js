import React from "react";
import ReactDOM from "react-dom";
import Minesweeper from "./Minesweeper";

// Hacky regular expression to build the API URI for the current game
let gameURI = "/api/games/" + window.location.href.match(/games\/(.*)/)[1]

const App = () => (
    // We use DataProvider to request the data and render the MineGrid 
    <Minesweeper gameURI={gameURI}/>
);

const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App />, wrapper) : null;