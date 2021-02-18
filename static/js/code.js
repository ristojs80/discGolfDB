function countScores() {
    let tmp = 0;
    let values = [];
    let st = document.getElementById("scoreTable");
    for (c = 2; c < st.tBodies[0].rows[0].cells.length; c++) {
        
        for (r = 1; r < st.tBodies[0].rows.length; r++) {
            tmp = tmp + parseInt(st.tBodies[0].rows[r].cells[c].textContent);
        }
        values.push(tmp)
        tmp = 0;
    }

    let x = st.insertRow(-1);
    x.insertCell(-1).textContent = "Total: "
    x.insertCell(-1);  

    for (i = 2; i < st.tBodies[0].rows[0].cells.length; i++) { 
        x.insertCell(-1).textContent = values[i - 2];
    }
    
}