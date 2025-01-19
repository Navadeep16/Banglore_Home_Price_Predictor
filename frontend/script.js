document.getElementById('predict-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    
    // Get form values
    const area = document.getElementById('area').value;
    const bhk = document.getElementById('bhk').value;
    const bath = document.getElementById('bath').value;
    const location = document.getElementById('location').value;
  
    // Send request to Flask API
    const response = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ area, bhk, bath, location })
    });
    
    const data = await response.json();
    document.getElementById('result').innerText = `Estimated Price: ₹${data.estimated_price}`;
  });
  
  // Fetch locations from Flask API and populate dropdown
  fetch('/locations').then(response => response.json()).then(data => {
    const locationDropdown = document.getElementById('location');
    data.locations.forEach(location => {
      const option = document.createElement('option');
      option.value = location;
      option.innerText = location;
      locationDropdown.appendChild(option);
    });
  });
  