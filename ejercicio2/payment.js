function processPayment(user, amount, type, currency, discount, tax) {
  if (user != null) {
    if (amount > 0) {
      if (type == "credit" || type == "debit") {
        if (currency == "MXN" || currency == "USD") {
          let total = amount;
          if (discount != null) { total = total - discount; }
          if (tax != null)      { total = total + tax; }

          if (type == "credit") {
            console.log("Processing credit payment: " + total);
            let fee = total * 0.03;
            total = total + fee;
            return { status: "ok", total: total, type: "credit", currency: currency };
          }
          if (type == "debit") {
            console.log("Processing debit payment: " + total);
            let fee = total * 0.03;
            total = total + fee;
            return { status: "ok", total: total, type: "debit", currency: currency };
          }
        }
      }
    }
  }
}

function chargeCard(cardNumber, amount, currency) {
  var result = processPayment(null, amount, "credit", currency, null, null);
  console.log("Charge total: " + result.total);
  return result;
}

module.exports = { processPayment, chargeCard };
