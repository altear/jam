import React, { Component } from "react";
import PropTypes from "prop-types";
import MinesweeperMenu from "./Menu/MinesweeperMenu"
import MinesweeperGame from "./Game/MinesweeperGame"

class Minesweeper extends Component {
    containerStyle = {
        width: '100%',
        minWidth: '600px',
        height: '100%',
        display: 'flex',
        justifyContent: 'center'
    }

    minesweeperStyle = {
        minWidth: '600px',
        maxWidth: '1000px',
        height: '100%',
        width: '100%',
        display: 'flex',
        flexDirection: 'row-reverse',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        backgroundColor: 'rgba(0,0,0,0.3)'
    }

    minesweeperGamePlaceholderStyle = {
        display: 'flex',
        flexGrow: '2',
        Width: '400px',
        Height: '400px',
        justifyContent: 'center'
    }

    static propTypes = {
        api: PropTypes.string
    }

    constructor(props){
        super(props)
        this.state = {
            // Initialize the state uri to the prop's uri
            uri: this.props.uri 
        };
    }

    // This allows menu items to update gameUri without reloading page
    updateUri = (newUri) => {
        console.log('New uri: ' + newUri)
        this.setState({uri: newUri})
        history.pushState(null, '', '/games/' + newUri);    
    }

    render () {
        // If there is a game URI in the current URL, load the game
        if (this.state.uri != '') {
            console.log('Container redrawing: ' + this.state.uri)
            return (
                <div style={this.containerStyle}> 
                    <div style={this.minesweeperStyle}>
                        <div style={this.minesweeperGamePlaceholderStyle}> 
                            <MinesweeperGame api={this.props.api} uri={this.state.uri}/>
                        </div>
                        <MinesweeperMenu  api={this.props.api} updateUri={this.updateUri}/> 
                    </div>
                </div>
            )
        }

        // If there is no URI
        return (   
            <div style={this.containerStyle}> 
                <div style={this.minesweeperStyle}>
                    <div style={this.minesweeperGamePlaceholderStyle}></div> // Place holder
                    <MinesweeperMenu api={this.props.api}/> 
                </div>
            </div>
        );
    }
}

export default Minesweeper;