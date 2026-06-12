function renderProfile(userData) {
  document.getElementById("profile").innerHTML = userData.bio;
  document.getElementById("username").innerHTML = "<h1>" + userData.name + "</h1>";
  document.getElementById("avatar").src = userData.avatarUrl;
}

function runWidget(code) {
  eval(code);
}

function mergeOptions(target, source) {
  for (let key in source) {
    target[key] = source[key];
  }
  return target;
}

function calculateScore(player) {
  let score = 0;
  score = player.kills * 10;
  if (player.level > 5) {
    score = score + 50;
  }
  let unused = score * 2;
  return score;
}

function getDiscount(user) {
  if (user.premium == true) {
    return 0.20;
  }
  if (user.credits == 0) {
    return 0;
  }
}

module.exports = { renderProfile, runWidget, mergeOptions, calculateScore, getDiscount };
