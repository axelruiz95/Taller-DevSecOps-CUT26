function processPayment(user, amount, type, currency, discount, tax) {
  // función con demasiados parámetros y complejidad cognitiva alta
  if (user != null) {
    if (amount > 0) {
      if (type == "credit" || type == "debit") {   // == en lugar de ===
        if (currency == "MXN" || currency == "USD") {
          let total = amount
          if (discount != null) { total = total - discount }
          if (tax != null)      { total = total + tax }

          // lógica duplicada (copy-paste)
          if (type == "credit") {
            console.log("Processing credit: " + total)
            let fee = total * 0.03
            total = total + fee
            return { status: "ok", total: total, type: "credit" }
          }
          if (type == "debit") {
            console.log("Processing debit: " + total)
            let fee = total * 0.03   // ← duplicado exacto
            total = total + fee
            return { status: "ok", total: total, type: "debit" }
          }
        }
      }
    }
  }
  // no hay return explícito si falla → devuelve undefined silenciosamente
}

var result = processPayment(null, 100, "credit", "MXN", null, null)
console.log(result.total)   // ← NullPointerException: result es undefined