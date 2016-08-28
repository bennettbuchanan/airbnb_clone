import React from 'react';

const styles = {
    footer: {
        minHeight: '40px',
        background: '#7FB2A0',
        borderTop: '1px solid black',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center'
    },
    text: {
        color: '#FFFFFF'
    }
}

const Footer = (props) => (
        <div style={styles.footer}>
        <div>
        <p style={styles.text}>Some text</p>
        </div>
        </div>
);

export default Footer;
