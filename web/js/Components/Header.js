import React from 'react';

const styles = {
    header: {
        marginRight: '200px',
        height: '60px',
        background: '#FFFFFF',
        borderBottom: '1px solid black'
    },
    logo: {
        height: '60px',
        width: 'auto',
    }
}

const Header = (props) => (
        <div style={styles.header}>
        <img style={styles.logo} src={props.imagePath} width={120} />
        </div>
);

Header.propTypes = {
    imagePath: React.PropTypes.string
};

Header.defaultProps = {

};

export default Header;
