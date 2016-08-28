import React from 'react';
import Header from './Header.js';
import ContentWrapper from './ContentWrapper.js';
import Footer from './Footer.js';

const styles = {
    outerWrapper: {
        'height': '100%',
        'minHeight': '100%',
        'width': 'auto',
        'display': 'flex',
        'flexDirection': 'column'
    }
}

const OuterWrapper = (props) => (
        <div style={styles.outerWrapper}>
        <Header
    imagePath={'../assets/images/airbnb_logo.png'}
        />
        <ContentWrapper/>
        <Footer/>
        </div>
);

OuterWrapper.defaultProps = {

};

export default OuterWrapper;
