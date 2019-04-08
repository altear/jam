import React, { Component } from "react";
import PropTypes from "prop-types";
import GridCell from "./MinesweeperGameCell"
import key from "weak-key";
import axios from 'axios';

// These tokens need to be sent in Post request to Django
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'


class MinesweeperGame extends Component {
    minesweeperGameContainerStyle = {
        display: 'flex',
        justifyContent: 'center',
        flexWrap: 'wrap',
        width: "600px",
        height: "600px",
        position: 'relative',
        overflow: 'wrap'
    }

    minesweeperGameStyle = {
        width: "600px",
        height: "600px",
        tableLayout: "fixed",
        backgroundColor: 'rgba(0,0,0,0.2)'
    }

    minesweeperGameOverlayStyle = {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        position: 'absolute',
        fontSize: '3em',
        color: 'rgba(255,255,255,0.8)',
        top: '0px',
        left: '0px',
        width: "100%",
        height: "100%",
        backgroundColor: 'rgba(0,0,0,0.8)',
    }

    static propTypes = {
        api: PropTypes.string,
        uri: PropTypes.string
    }

    constructor(props){
        super(props)
        this.state = {
            isWinner: false,
            isLoser: false,
            data: {},
            loaded: false,
            uri: this.props.uri // we use this to force render from children
        };
    }

    componentDidMount() {
        this.fetchGameData()
    }

    componentDidUpdate(prevProps, prevState) {
        // Has the game URI changed? If so, update state and fetch new game data
        if (prevProps.uri != this.props.uri) {
            this.setState({uri: this.props.uri, loaded: false}, this.fetchGameData) 
        }
    }

    // Return the URI to the current game
    getGameUri = () => {
        return this.props.api + "games/" + this.state.uri
    }
    
    fetchGameData = () => {
        // Fetch the current game state
        console.log("Fetching game data from " + this.getGameUri())
        fetch(this.getGameUri())
            .then(response => response.json())
            .then(this.messageHandler)
    }

    /*
     * Clear area
     */
    clearArea = (index) => {
        console.log("clear space")
        axios.post(this.getGameUri() + '/clear-area/', {i: index[0], j:index[1]})
            .then((response) => response.data) 
            .then(this.messageHandler); 
    }   

    /*
     * Add/remove flag on cell
     */
    plantFlag = (index) => {
        console.log("flag")
        axios.post(this.getGameUri() + '/plant-flag/', {i: index[0], j:index[1]})
            .then((response) => response.data) 
            .then(this.messageHandler);  
    }   

    /*
     * Handle server responses
     */
    messageHandler = (message) => {
        if (message['message-type'] == 'game-state') {
            this.setState({data: message, loaded: true});
            if (message.is_loser) {
                console.log('Lost!')
            } else if (message.is_winner) {
                console.log('Won')
            }
        } else if (message['message-type'] == 'new-game'){
            // todo
        }
    }

    createGrid() {
        console.log("Creating new grid... ")
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
                        clearArea={this.clearArea} 
                        plantFlag={this.plantFlag} 
                        updateUri={this.updateUri}
                        display={display} />
                ) 
            }     
            table.push(<tr key={key([i])} >{children}</tr>)  
        }
        return table
    }

    // We've modularized this to make the render() function a little cleaner. Only call when the game is over
    getGameOverMessage = () => {
        if (this.state.data.is_winner) {
            return "You Won!"
        } else {
            return "You Lost!"
        } 
    }

    render () {
        // Game hasn't loaded
        if (this.state.loaded == false) {
            return (<p> Loading Game... </p>)
        }
        // Game has finished
        if (this.state.data.is_winner || this.state.data.is_loser){
            return (
                <div style={this.minesweeperGameContainerStyle}>
                    <table style={this.minesweeperGameStyle}>
                        <tbody>
                            {this.createGrid()}
                        </tbody>
                    </table>
                    <div style={this.minesweeperGameOverlayStyle}><p>{this.getGameOverMessage()}</p></div>
                </div>
            )
        }
        // Game is still ongoing
        return (
            <div style={this.minesweeperGameContainerStyle}>
                <table style={this.minesweeperGameStyle}>
                    <tbody>
                        {this.createGrid()}
                    </tbody>
                </table>
            </div>
        )
    }
}

export default MinesweeperGame;