document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("withdraw-form");
  const resultDiv = document.getElementById("result");

  if (!currentUserId) {
    resultDiv.textContent = "❌ User not found (Telegram WebApp user.id missing)";
    form.style.display = "none";
    return;
  }

  form.addEventListener("submit", e => {
    e.preventDefault();
    resultDiv.textContent = "";

    const amount = parseFloat(form.amount.value);
    const currency = form.currency.value.trim();

    if (!amount || !currency) {
      resultDiv.textContent = "Please fill all fields.";
      return;
    }

    apiPost("/api/user/withdraw", {
      user_id: currentUserId,
      amount,
      currency
    })
      .then(data => {
        if (data.message) {
          resultDiv.textContent = "✅ " + data.message;
        } else if (data.detail) {
          resultDiv.textContent = "❌ " + data.detail;
        } else {
          resultDiv.textContent = "Unknown response.";
        }
      })
      .catch(err => {
        console.error(err);
        resultDiv.textContent = "Network error.";
      });
  });
});
