document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('searchInput');
  const cityFilter = document.getElementById('cityFilter');
  const medicineRows = document.querySelectorAll('#medicineTable tbody tr');
  const loader = document.getElementById('loader');

  function filterMedicines() {
    const searchText = searchInput.value.toLowerCase();
    const city = cityFilter.value.toLowerCase();

    medicineRows.forEach(row => {
      const medicineName = row.querySelector('td:nth-child(1)').textContent.toLowerCase();
      const cityName = row.querySelector('td:nth-child(3)').textContent.toLowerCase();

      const matchesSearch = medicineName.includes(searchText);
      const matchesCity = city === 'all' || cityName === city;

      if (matchesSearch && matchesCity) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    });
  }

  searchInput.addEventListener('input', filterMedicines);
  cityFilter.addEventListener('change', filterMedicines);

  // Loader animation on form submit
  const donateForm = document.getElementById('donateForm');
  if (donateForm) {
    donateForm.addEventListener('submit', (e) => {
      loader.style.display = 'block';
    });
  }
});
