function poster() {
    const movieTitle = document.getElementById("title").innerText.trim().toLowerCase();
    fetch("static/poster.json")
      .then(response => response.json())
      .then(data => {
        if (data.hasOwnProperty(movieTitle)) {
          const posterURL = data[movieTitle];
          const posterElement = document.getElementById("poster");
          posterElement.innerHTML = `<img src="${posterURL}" width="230px" height="346px">`;
        }
      })
      .catch(error => {
        console.error("Error fetching poster.json:", error);
      });
  }
window.onload = poster;
  