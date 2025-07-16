document.addEventListener('DOMContentLoaded', () => {
    const pinSelect = document.getElementById('pin-select');
    const findButton = document.getElementById('find-button');
    const resultsContainer = document.getElementById('results-container');
    const loader = document.getElementById('loader');
    const controls = document.getElementById('controls');

    // On page load, fetch the list of all properties to populate the dropdown
    fetch('/api/properties')
        .then(response => response.json())
        .then(data => {
            loader.style.display = 'none'; // Hide loader
            controls.classList.remove('hidden'); // Show controls

            data.forEach(property => {
                const option = document.createElement('option');
                option.value = property.property_identification_number;
                option.textContent = property.property_identification_number;
                pinSelect.appendChild(option);
            });
        })
        .catch(error => {
            loader.textContent = 'Error: Could not load property data from the backend API.';
            console.error('Error fetching properties:', error);
        });

    // When the "Find Comparables" button is clicked
    findButton.addEventListener('click', () => {
        const selectedPin = pinSelect.value;
        if (!selectedPin || selectedPin.startsWith('--')) {
            alert('Please select a valid property PIN.');
            return;
        }

        resultsContainer.innerHTML = '<div class="loader">Agent is performing analysis...</div>';

        // Fetch the comparables for the selected PIN from our Python API
        fetch(`/api/comparables/${selectedPin}`)
            .then(response => response.json())
            .then(comparables => {
                resultsContainer.innerHTML = ''; // Clear the loader

                if (comparables.length === 0) {
                    resultsContainer.innerHTML = '<p>No comparables found.</p>';
                    return;
                }

                // Create and display a table with the results
                const table = document.createElement('table');
                table.innerHTML = `
                    <thead>
                        <tr>
                            <th>PIN</th>
                            <th>Square Footage</th>
                            <th>Year Built</th>
                            <th>Confidence Score</th>
                        </tr>
                    </thead>
                `;
                const tbody = document.createElement('tbody');
                comparables.forEach(comp => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${comp.property_identification_number}</td>
                        <td>${comp.square_footage.toLocaleString()}</td>
                        <td>${comp.year_built}</td>
                        <td>${comp.confidence_score.toFixed(4)}</td>
                    `;
                    tbody.appendChild(row);
                });
                table.appendChild(tbody);
                resultsContainer.appendChild(table);
            })
            .catch(error => {
                resultsContainer.innerHTML = '<p>An error occurred during analysis.</p>';
                console.error('Error fetching comparables:', error);
            });
    });
});