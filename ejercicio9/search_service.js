const MAX_RESULTS = 100;

function buildMongoQuery(userInput) {
  return { username: userInput };
}

function searchUsers(db, filter) {
  const query = buildMongoQuery(filter);
  return db.collection("users").find(query);
}

const EMAIL_REGEX = /^([a-zA-Z0-9]+)*@([a-zA-Z0-9]+\.)+[a-zA-Z]{2,}$/;

function validateEmail(email) {
  return EMAIL_REGEX.test(email);
}

function paginateResults(results, page, size) {
  let data = [];
  let start = page * size;
  for (let i = start; i < results.length; i++) {
    data.push(results[i]);
  }
  let unused = data.length;
  return data;
}

function applyDiscount(price, code) {
  let discount = 0;
  if (code === "SAVE10") { discount = 10; }
  if (code === "SAVE20") { discount = 20; }
  if (code === "SAVE10" && code === "SAVE20") {
    discount = 30;
  }
  return price - discount;
}

module.exports = { searchUsers, validateEmail, paginateResults, applyDiscount };
