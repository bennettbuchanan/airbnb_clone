import React from 'react';

const styles = {
    content: {
        width: '100%',
        marginRight: '200px',
        backgroundColor: '#9ACD32',
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
