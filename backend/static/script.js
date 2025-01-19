const form = document.getElementById('predict-form');
form.addEventListener('submit', async function(event) {
  event.preventDefault();

  const area = document.getElementById('area').value;
  const bhk = document.getElementById('bhk').value;
  const bath = document.getElementById('bath').value;
  const location = document.getElementById('location').value;

  const data = {
    area: area,
    bhk: bhk,
    bath: bath,
    location: location
  };

  // Send the data to the backend
  const response = await fetch('/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });

  const result = await response.json();
  if (result.predicted_price) {
    document.getElementById('result').innerText = `Predicted Price: ₹${result.predicted_price}`;
  } else {
    document.getElementById('result').innerText = `Error: ${result.error}`;
  }
});

  