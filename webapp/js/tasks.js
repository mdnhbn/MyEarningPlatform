document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("tasks-container");

  if (!currentUserId) {
    container.textContent = "❌ User not found (Telegram WebApp user.id missing)";
    return;
  }

  apiGet("/api/user/tasks", { user_id: currentUserId })
    .then(data => {
      container.innerHTML = "";
      if (!data.tasks || data.tasks.length === 0) {
        container.textContent = "No tasks available at the moment.";
        return;
      }

      data.tasks.forEach(task => {
        const card = document.createElement("div");
        card.className = "card";

        card.innerHTML = `
          <div class="task-title">${task.title}</div>
          <div class="task-reward">Reward: ${task.reward}</div>
          <a href="${task.link}" target="_blank" class="btn small">🔗 Open</a>
          <div class="hint">After completing, go back to bot and send:<br><code>/done ${task.id}</code></div>
        `;

        container.appendChild(card);
      });
    })
    .catch(err => {
      console.error(err);
      container.textContent = "Error loading tasks.";
    });
});
