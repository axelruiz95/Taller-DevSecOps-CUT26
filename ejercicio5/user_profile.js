// Módulo de perfil de usuario con múltiples vulnerabilidades XSS y de lógica

function renderProfile(userData) {
  // XSS: innerHTML con datos del usuario sin sanitizar
  document.getElementById("profile").innerHTML = userData.bio
  document.getElementById("username").innerHTML = "<h1>" + userData.name + "</h1>"
}

function runWidget(code) {
  // eval() ejecuta código arbitrario del servidor o del usuario
  eval(code)   // ← inyección de código
}

function mergeOptions(target, source) {
  // prototype pollution: mezcla sin verificar __proto__
  for (let key in source) {
    target[key] = source[key]   // ← contaminación del prototipo
  }
  return target
}

function calculateScore(player) {
  let score = 0
  score = player.kills * 10    // ← asignación muerta: score anterior nunca se usa
  if (player.level > 5) {
    score = score + 50
  }
  let unused = score * 2       // ← variable local nunca utilizada
  return score
}

function getDiscount(user) {
  // == en lugar de === puede dar resultados inesperados (0 == false, "" == false)
  if (user.premium == true) {
    return 0.20
  }
  if (user.credits == 0) {    // ← loose equality
    return 0
  }
}
// no hay return por defecto → devuelve undefined si ninguna condición se cumple
