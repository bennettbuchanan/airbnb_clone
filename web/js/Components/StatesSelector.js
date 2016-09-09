import React from 'react';
import $ from 'jquery';
import StateItemSelector from './StateItemSelector.js'

const styles = {
    statesSelector: {
        backgroundColor: '#red',
        margin: '10px',
        width: '100%'
    }
}

var StatesSelector = React.createClass({
    render: function() {

        if (this.props.stateData != undefined) {
            return (
                    <div style={styles.statesSelector}>
                    <h1>States</h1>
                    {this.props.stateData.map(function(item) {
                        return (<StateItemSelector key={item.id}
                                name={item.name} />);
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
