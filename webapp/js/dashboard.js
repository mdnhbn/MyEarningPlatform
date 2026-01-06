document.addEventListener("DOMContentLoaded", () => {
  const balanceDiv = document.getElementById("balance");
  const statusDiv = document.getElementById("status");

  if (!currentUserId) {
    balanceDiv.textContent = "❌ User not found (Telegram WebApp user.id missing)";
    return;
  }

  apiGet("/api/user/balance", { user_id: currentUserId })
    .then(data => {
      if (data.balance !== undefined) {
        balanceDiv.textContent = "💰 Your Balance: " + data.balance;
      } else if (data.detail) {
        balanceDiv.textContent = "Error: " + data.detail;
      } else {
        balanceDiv.textContent = "Unknown response";
      }
    })
    .catch(err => {
      console.error(err);
      balanceDiv.textContent = "Error loading balance";
      statusDiv.textContent = "Network error";
    });
});
