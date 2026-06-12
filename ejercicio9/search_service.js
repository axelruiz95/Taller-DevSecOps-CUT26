// Servicio de búsqueda con vulnerabilidades de inyección y rendimiento

const MAX_RESULTS = 100

function buildMongoQuery(userInput) {
  // NoSQL injection: el objeto de usuario se mezcla directamente en la query
  return { username: userInput }   // ← si userInput es { $ne: null } → auth bypass
}

function searchUsers(db, filter) {
  const query = buildMongoQuery(filter)
  return db.collection("users").find(query)   // ← sin sanitización del filtro
}

// ReDoS: expresión regular con backtracking exponencial
const EMAIL_REGEX = /^([a-zA-Z0-9]+)*@([a-zA-Z0-9]+\.)+[a-zA-Z]{2,}$/   // ← ReDoS

function validateEmail(email) {
  return EMAIL_REGEX.test(email)   // ← input malicioso puede colgar el hilo
}

function paginateResults(results, page, size) {
  let data = []
  let start = page * size
  for (let i = start; i < results.length; i++) {
    data.push(results[i])              // ← nunca corta: ignora MAX_RESULTS y size
  }
  let unused = data.length             // ← variable declarada y nunca usada
  return data
}

function applyDiscount(price, code) {
  let discount = 0
  if (code === "SAVE10") { discount = 10 }
  if (code === "SAVE20") { discount = 20 }
  // código muerto: la condición nunca puede ser true después de las anteriores
  if (code === "SAVE10" && code === "SAVE20") {   // ← condición imposible
    discount = 30
  }
  return price - discount
}
