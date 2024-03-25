/**
 * Returns a random integer between 1 and 100 (inclusive)
 * @returns a random integer between 1 and 100 (inclusive)
 */
export function getRandomNumber() : number {
  return Math.floor(Math.random() * 100) + 1;
}

export function initialize() {
  const randomNumberElement = document.getElementById("random-number");
  if (randomNumberElement) {
    randomNumberElement.innerHTML = getRandomNumber().toString();
  } else {
    console.error("Could not find element with id 'random-number'")
  }
}