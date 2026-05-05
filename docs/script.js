const username = "Fresht0Death";
const repoContainer = document.getElementById("repo-container");

async function loadRepos() {
  try {
    const response = await fetch(`https://api.github.com/users/${username}/repos?sort=updated`);

    if (!response.ok) {
      throw new Error("Failed to fetch repositories");
    }

    const repos = await response.json();

    repoContainer.innerHTML = "";

    repos.forEach(repo => {
      const card = document.createElement("div");
      card.className = "repo-card";

      card.innerHTML = `
        <h3>${repo.name}</h3>
        <p>${repo.description || "No description provided yet."}</p>
        <p><strong>Language:</strong> ${repo.language || "Not specified"}</p>
        <a href="${repo.html_url}" target="_blank">View on GitHub</a>
      `;

      repoContainer.appendChild(card);
    });
  } catch (error) {
    repoContainer.innerHTML = `
      <p>Could not load GitHub repositories right now.</p>
    `;
    console.error(error);
  }
}

loadRepos();