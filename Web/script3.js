  function saveConfig(configData) {
    fetch('../config.json', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(configData)
    })
    .then(response => response.json())
    .then(data => console.log('Config saved:', data))
    .catch(error => console.error('Error:', error));
  }

  function updateToggles(configData) {
    document.getElementById('toggle1').checked = configData.shorter_wanted;
    document.getElementById('toggle2').checked = configData.lower_wanted;
  }

  function loadConfig(callback) {
    fetch('../config.json')
      .then(response => response.json())
      .then(data => callback(data))
      .catch(error => console.error('Error:', error));
  }

  loadConfig(function(configData) {
    updateToggles(configData);
  });


  document.getElementById('toggle2').addEventListener('change', function() {
    sendToggleState();
  });

  function updateJson() {
    const toggle1 = document.getElementById('toggle1').checked;
    const toggle2 = document.getElementById('toggle2').checked;
    
    const data = {
      shorter_wanted: toggle1,
      lower_wanted: toggle2
    };
    console.log(data)
    alert(data)
    
    fetch('http://localhost:1235/stat1', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => {
      if (!response.ok) {
        throw new Error("Erreur lors de l'envoi de la requête.");
      }
      return response.json();
    })
    .then(responseData => {
      console.log(responseData);
    })
    .catch(error => {
      console.error("Erreur:", error);
    });
  }

  function envoyerRequete() {
    const champ1 = document.getElementById("champ1").value;
    const champ2 = document.getElementById("champ2").value;

    const data = {
      "Src": champ1,
      "Dst": champ2
    };

    fetch("http://localhost:1235/data", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    })
    .then(response => {
      if (!response.ok) {
        throw new Error("Erreur lors de l'envoi de la requête.");
      }
      return response.json();
    })
    .then(responseData => {
      console.log(responseData);
    })
    .catch(error => {
      console.error("Erreur:", error);
    });
  }
