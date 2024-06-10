function filterPatients() {
    const query = document.getElementById('search-bar').value.toLowerCase();
    fetch(`/search?q=${query}`)
        .then(response => response.json())
        .then(data => {
            const patientList = document.getElementById('patient-list');
            let patientHtml = '<table class="table table-striped"><thead><tr><th>Name</th><th>Age</th><th>Email</th><th>Phone</th><th>Status</th></tr></thead><tbody>';
            data.forEach(patient => {
                patientHtml += `<tr>
                    <td onclick="submitForm('${patient.id}')">${patient.name}</td>
                    <td>${patient.age}</td>
                    <td>${patient.email}</td>
                    <td>${patient.phone}</td>
                    <td>${patient.admission_filled ? '<img src="/static/check.png" alt="Completed">' : '<img src="/static/cross.png" alt="Not Completed">'}</td>
                </tr>`;
            });
            patientHtml += '</tbody></table>';
            patientList.innerHTML = patientHtml;
        });
}

function submitForm(patientId) {
    fetch('/submit_admission_form', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ patient_id: patientId })
    })
    .then(response => response.json())
    .then(data => {
        window.location.href = data.url;
    });
}
