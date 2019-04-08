import React from "react";
import ReactDOM from "react-dom";
import Minesweeper from "./Minesweeper"

const API_LOCATION = "/api/" 
var gameUri = ''
try {
    gameUri = window.location.href.match(/games\/(.*)/)[1] 
} catch {
    console.log("No game URI found")
}

const App = () => {
    return (<Minesweeper api={API_LOCATION} uri={gameUri}/>)
}

const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App />, wrapper) : null;