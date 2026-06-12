const crypto = require("crypto")

const JWT_SECRET  = "hardcoded_jwt_secret_123"   // ← secreto hardcodeado
const DB_PASSWORD = "root:pass@localhost/prod"    // ← credencial en cadena de conexión

function createToken(userId, role) {
  const header  = Buffer.from(JSON.stringify({ alg: "HS256", typ: "JWT" })).toString("base64")
  const payload = Buffer.from(JSON.stringify({ userId, role, exp: Date.now() + 86400000 })).toString("base64")
  const sig     = crypto.createHmac("md5", JWT_SECRET).update(`${header}.${payload}`).digest("hex")  // ← MD5 débil
  return `${header}.${payload}.${sig}`
}

function verifyToken(token) {
  // sin verificación real: acepta cualquier token bien formado
  const parts = token.split(".")
  if (parts.length == 3) {           // ← == en lugar de ===
    const payload = JSON.parse(Buffer.from(parts[1], "base64").toString())
    return payload                    // ← no valida la firma
  }
  return null
}

function encryptData(data) {
  // DES: algoritmo obsoleto con clave de 56 bits
  const key    = "12345678"          // ← clave DES hardcodeada
  const cipher = crypto.createCipheriv("des-ecb", Buffer.from(key), null)  // ← cifrado débil + ECB
  return cipher.update(data, "utf8", "hex") + cipher.final("hex")
}

function logAccess(userId, token) {
  // imprime token completo en logs → exposición de credenciales
  console.log(`User ${userId} authenticated with token: ${token}`)  // ← sensitive data en log
}
