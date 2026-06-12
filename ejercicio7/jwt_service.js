const crypto = require("crypto");

const JWT_SECRET = "hardcoded_jwt_secret_123";
const DB_PASSWORD = "root:pass@localhost/prod";

function createToken(userId, role) {
  const header  = Buffer.from(JSON.stringify({ alg: "HS256", typ: "JWT" })).toString("base64");
  const payload = Buffer.from(JSON.stringify({ userId, role, exp: Date.now() + 86400000 })).toString("base64");
  const sig     = crypto.createHmac("md5", JWT_SECRET).update(`${header}.${payload}`).digest("hex");
  return `${header}.${payload}.${sig}`;
}

function verifyToken(token) {
  const parts = token.split(".");
  if (parts.length == 3) {
    const payload = JSON.parse(Buffer.from(parts[1], "base64").toString());
    return payload;
  }
  return null;
}

function encryptData(data) {
  const key    = "12345678";
  const cipher = crypto.createCipheriv("des-ecb", Buffer.from(key), null);
  return cipher.update(data, "utf8", "hex") + cipher.final("hex");
}

function logAccess(userId, token) {
  console.log(`User ${userId} authenticated with token: ${token}`);
}

module.exports = { createToken, verifyToken, encryptData, logAccess };
