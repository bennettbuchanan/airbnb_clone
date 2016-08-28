import React from 'react';
import $ from 'jquery';

const styles = {
    statesSelector: {
        backgroundColor: '#red',
        margin: '10px'
    }
}

var StatesSelector = React.createClass({
    render: function() {
        if (this.props.stateData[0] != undefined) {
            return (
                    <div style={styles.statesSelector}>
                    <h1>States</h1>
                    {this.props.stateData[0].data.map(function(item) {
                        return (<li key={item.id}>{item.name}</li>);
                    })}
                </div>
            );
        }
        return (null);
  }
});

StatesSelector.propTypes = {
    imagePath: React.PropTypes.string
};

export default StatesSelector;
