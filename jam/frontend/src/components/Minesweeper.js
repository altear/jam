import React, { Component } from "react";
import GridCell from "./GridCell";
import key from "weak-key";
import axios from 'axios';

// These tokens need to be sent in Post request to Django
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

let gameContainerStyle = {
    display: 'flex',
    justifyContent: 'center',
    alignContent: 'center',
    flexDirection: 'row'
}

let menuContainerStyle = {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    flexDirection: 'column'
}

class Minesweeper extends Component {
    constructor(props){
        super(props);
        
        this.state = {
          data: {},
          loaded: false
        };
      }

    /*
     * Handles cases such as winning, losing, and updating the game view
     */
    messageHandler = (message) => {
        if (message['message-type'] == 'game-state') {
            this.setState({data: message, loaded: true});
        } else if (message['message-type'] == 'new-game'){
            // todo
        }
    }

    /*
     * Runs when the component first mounds
     */
    componentDidMount() {
        fetch(this.props.gameURI)
            .then(response => response.json())
            .then(this.messageHandler)
    }

    /*
     * Clear an area of mines and get the new game state
     */
    clearArea(index, value) {
        axios.post(this.props.gameURI + '/clear-area/', {i: index[0], j:index[1]})
            .then((response) => response.data) 
            .then(this.messageHandler); 
    }   

    /*
     * What happens if you miss?
     */
    plantFlag(index, value) {
        axios.post(this.props.gameURI + '/plant-flag/', {i: index[0], j:index[1]})
            .then((response) => response.data) 
            .then(this.messageHandler);  
    }   

    /*
     * Create the grid of mines
     */
    createGrid() {
        let table = []

        // Get array dimentions
        let m = this.state.data.view.length
        let n = this.state.data.view[0].length
        
        // Create grid, populate with GridCell
        for (let i = 0; i < m; i++) {
            let children = []
            for (let j = 0; j < n; j++) {
                let display = this.state.data.view[i][j]
                children.push(
                    <GridCell 
                        key={key([i,j,display])} 
                        index={[i, j]} 
                        clearArea={this.clearArea.bind(this)} 
                        plantFlag={this.plantFlag.bind(this)} 
                        display={display} />
                ) 
            }     
            table.push(<tr key={key([i])} >{children}</tr>)  
        }
        return table
    }
    
    /*
     * Redirect to new game (super hacky)
     */
    newGame = () => {
        fetch("/api/create-large-game")
            .then((response) => response.json())
            .then((data) => window.location.href = "/games/" + data.uuid)
    }

    /* 
     * Render this component and its children
     */
    render() {
        if (!this.state.loaded) {
            return (<p> Your game is almost ready </p>)
        } 

        if (this.state.data.is_loser || this.state.data.is_winner){
            // Game has finished
            return (
                <div style={menuContainerStyle}>
                    <h1> Game Over! Another one bites the dust. </h1> 
                    <button onClick={this.newGame}> Play Again? </button>

                    <div style={gameContainerStyle}>
                        <table>
                            <tbody>
                                {this.createGrid()}
                            </tbody>
                        </table>
                    </div>
                </div>  
            )
        }

        // If the game is still going on
        return (
            <div style={gameContainerStyle}>
                <table>
                    <tbody>
                        {this.createGrid()}
                    </tbody>
                </table>
            </div>
        )
    }
}
export default Minesweeper;

