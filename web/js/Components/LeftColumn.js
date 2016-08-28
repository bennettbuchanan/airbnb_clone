import React from 'react';
import StateSelector from './StatesSelector.js';
import $ from 'jquery';

const styles = {
    leftColumn: {
        minWidth: '300px',
        height: '100%',
        backgroundColor: '#CFFFEE',
        display: 'flex',
        justifyContent: 'flex-start'
    }
}

var LeftColumn = React.createClass({
    getInitialState: function() {
        return {stateData: []};
    },

    componentDidMount: function() {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            cache: false,
            success: function(data) {
                this.setState({stateData: data});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
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
