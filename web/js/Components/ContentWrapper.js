import React from 'react';
import LeftColumn from './LeftColumn.js';
import Content from './Content.js';

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
        <LeftColumn url="http://localhost:3333/states"/>
        <Content/>
        </div>
);

ContentWrapper.defaultProps = {

};

export default ContentWrapper;
