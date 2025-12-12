function detectDrug() {
    let example = document.getElementById("formula").value.toLowerCase().trim();
    let resultBox = document.getElementById("result");

    resultBox.style.display = "block";
    resultBox.innerHTML = `<p>⏳ Processing...</p>`;

    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ drug_example: example })
    })
    .then(res => res.json())
    .then(data => {

        if (data.status === "Drug detected") {

            let d = data.details;

            let html = `
                <img src="https://cdn-icons-png.flaticon.com/512/3176/3176366.png" class="drug-img">

                <h2>✔ ${d.usp_drug}</h2>

                <ul>
                    <li><strong>Name:</strong> ${d.usp_drug}</li>
                    <li><strong>Category:</strong> ${d.usp_category}</li>
                    <li><strong>Class:</strong> ${d.usp_class}</li>
                    <li><strong>KEGG ID (drug):</strong> ${d.kegg_id_drug}</li>
                    <li><strong>KEGG ID (example):</strong> ${d.kegg_id_drug_example}</li>
                    <li><strong>Nomenclature:</strong> ${d.nomenclature}</li>
                </ul>
            `;

            resultBox.innerHTML = html;

        } else {
            resultBox.innerHTML = `
                <p style="color:#e63946; font-size:18px;">
                    ❌ No drug found for: <strong>${example}</strong>
                </p>
            `;
        }
    })
    .catch(err => {
        console.error(err);
        resultBox.innerHTML = `<p style="color:red;">⚠️ Error connecting to server</p>`;
    });
}
