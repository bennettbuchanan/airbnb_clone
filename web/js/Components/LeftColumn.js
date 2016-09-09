import React from 'react';
import StateSelector from './StatesSelector.js';
import fetchData from '../Reducers/states.js';

const styles = {
    leftColumn: {
        minWidth: '300px',
        height: '100%',
        backgroundColor: '#CFFFEE',
        display: 'flex',
        justifyContent: 'flex-start'
    }
};

var LeftColumn = React.createClass({
    getInitialState: function() {
        return {
            stateData: []
        };
    },

    componentDidMount: function() {
        fetchData("http://localhost:3333/states", (res) => {
            res = JSON.parse(res);
            this.setState({stateData: res[0].data});
        });
    },

    render: function() {
        return (
                <div style={styles.leftColumn}>
                <StateSelector stateData={this.state.stateData}/>
                </div>
        );
    }
});

LeftColumn.propTypes = {
    imagePath: React.PropTypes.string
};

export default LeftColumn;
