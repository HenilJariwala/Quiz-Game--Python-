function selectDifficulty(value) {
  // Set the value of the hidden input based on the button clicked
  document.getElementById("difficulty").value = value;
  //alert("Selected difficulty: " + value); // Optional, for testing
}

// Confetti explosion effect and sound
function celebrate() {
  // Play sound effect
  var audio = document.getElementById("successSound");
  audio.play();

  // Confetti explosion effect
  var duration = 2 * 1000; // 2 seconds
  var animationEnd = Date.now() + duration;
  var defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

  function randomInRange(min, max) {
    return Math.random() * (max - min) + min;
  }

  var interval = setInterval(function () {
    var timeLeft = animationEnd - Date.now();

    if (timeLeft <= 0) {
      return clearInterval(interval);
    }

    var particleCount = 50 * (timeLeft / duration);
    // Confetti explosion from random points
    confetti(
      Object.assign({}, defaults, {
        particleCount,
        origin: { x: randomInRange(0.1, 0.9), y: Math.random() - 0.2 },
      })
    );
  }, 250);
}
