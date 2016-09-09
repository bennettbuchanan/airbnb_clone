const checkboxState = (state = false, action) => {
    switch (action.type) {
        case 'CHECK':
            return true;
        case 'UNCHECK':
            return false;
        default:
            return false;
    }
};

const expandState = (state = false, action) => {
    switch (action.type) {
        case 'EXPAND':
            return true;
        case 'COLLAPSE':
            return false;
        default:
            return false;
    }
};

export { checkboxState, expandState };
