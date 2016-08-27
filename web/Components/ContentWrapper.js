import React from 'react';
import LeftColumn from './LeftColumn.js';
import Content from './Content.js';
import Header from './Header.js';
import Footer from './Footer.js';

const styles = {
    contentWrapper: {
        width: '100%',
        height: '100%',
        display: 'flex',
        flexDirection: 'row'
    }
}

const ContentWrapper = (props) => (
        <div style={styles.contentWrapper}>
        <LeftColumn/>
        <Content/>
        </div>
);

ContentWrapper.defaultProps = {

};

export default ContentWrapper;
