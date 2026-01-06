document.addEventListener("DOMContentLoaded", () => {
  const profileDiv = document.getElementById("profile-info");

  if (!currentUserId) {
    profileDiv.textContent = "❌ User not found (Telegram WebApp user.id missing)";
    return;
  }

  apiGet("/api/user/profile", { user_id: currentUserId })
    .then(data => {
      if (data.detail) {
        profileDiv.textContent = "Error: " + data.detail;
        return;
      }

      profileDiv.innerHTML = `
        <div><b>Telegram ID:</b> ${data.telegram_id}</div>
        <div><b>Balance:</b> ${data.balance}</div>
        <div><b>Banned:</b> ${data.banned ? "Yes" : "No"}</div>
        <div><b>Joined:</b> ${data.created_at}</div>
        <div><b>Total Earned:</b> ${data.total_earned}</div>
      `;
    })
    .catch(err => {
      console.error(err);
      profileDiv.textContent = "Error loading profile.";
    });
});
