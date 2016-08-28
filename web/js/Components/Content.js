import React from 'react';

const styles = {
    content: {
        width: '100%',
        marginRight: '200px',
        backgroundColor: '#FFFFFF',
        borderLeft: '1px solid black',
        borderRight: '1px solid black'
    }
}

const Content = (props) => (
        <div style={styles.content}>
        </div>
);

Content.propTypes = {
    imagePath: React.PropTypes.string
};

Content.defaultProps = {

};

export default Content;
