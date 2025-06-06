document.getElementById('launch').addEventListener('click', () => {
    const count = parseInt(document.getElementById('sessionCount').value);
    if (isNaN(count) || count < 1 || count > 20) {
      alert('Veuillez entrer un nombre entre 1 et 20.');
      return;
    }
    window.electronAPI.openLobbies(count);
  });
  