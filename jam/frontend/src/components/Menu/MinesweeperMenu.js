import React, { Component } from "react";
import MinesweeperMenuItem from "./MinesweeperMenuItem"
import PropTypes from "prop-types";

class MinesweeperMenu extends Component {
    menuStyle = {
        marginTop: '20px',
        minWidth: '250px',
        maxWidth: '250px',
        height: '100%',
        display: 'flex',
        padding: '10px',
        flexDirection: 'column',
        justifyContent: 'flex-start',
        justifySelf: 'flex-start',
        alignItems: 'center',
        backgroundColor: 'rgba(0,0,0,0.2)'
    }
    
    menuTitleStyle = {
        fontSize: '1.5em',
        marginBelow: '20px'
    }

    static propTypes = {
        api: PropTypes.string,
        updateUri: PropTypes.func
    }

    render () {
        return (
            <div style={this.menuStyle}>
                <p style={this.menuTitleStyle}> New Game? </p>
                <MinesweeperMenuItem text="Small" api={this.props.api} action="create-small-game" updateUri={this.props.updateUri}/>
                <MinesweeperMenuItem text="Medium" api={this.props.api} action="create-medium-game" updateUri={this.props.updateUri}/> 
                <MinesweeperMenuItem text="Large" api={this.props.api} action="create-large-game" updateUri={this.props.updateUri}/> 
            </div>
        )
    }
}

export default MinesweeperMenu;