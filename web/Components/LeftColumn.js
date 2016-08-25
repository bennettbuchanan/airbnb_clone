import React from 'react';

const styles = {
    leftColumn: {
        width: '300px',
        background: 'blue',
        display: 'float',
        float: 'left'
    }
}

const LeftColumn = (props) => (
        <div style={styles.leftColumn}>
        </div>
);

LeftColumn.defaultProps = {

};

export default LeftColumn;
