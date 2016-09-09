const initialState = {
    stateData : []
};

const fetchData = (url, callback) => {
    let req = new XMLHttpRequest();
    req.open("GET", url, true);
    req.addEventListener("load", () => {
        if (req.status < 400) {
            callback(req.responseText);
        }
    });
    req.send(null);
};

export default fetchData;
