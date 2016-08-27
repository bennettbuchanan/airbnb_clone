import React from 'react';

const styles = {
    leftColumn: {
        minWidth: '300px',
        height: '100%',
        backgroundColor: '#F5DEB3'
    }
}

const LeftColumn = (props) => (
        <div style={styles.leftColumn}>
        </div>
);

LeftColumn.propTypes = {
    imagePath: React.PropTypes.string
};

LeftColumn.defaultProps = {

};

export default LeftColumn;
