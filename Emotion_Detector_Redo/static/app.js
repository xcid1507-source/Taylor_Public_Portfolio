const form = document.querySelector("#emotion-form");
const input = document.querySelector("#text-input");
const button = document.querySelector("#analyze-button");
const result = document.querySelector("#result");
const message = document.querySelector("#status-message");
const scores = document.querySelector("#scores");
const count = document.querySelector("#character-count");

input.addEventListener("input", () => {
  count.textContent = `${input.value.length} / 5000`;
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = input.value.trim();
  result.hidden = false;
  scores.replaceChildren();

  if (!text) {
    message.textContent = "Please enter text to analyze.";
    return;
  }

  button.disabled = true;
  button.textContent = "Analyzing…";
  message.textContent = "Contacting Watson NLP…";

  try {
    const params = new URLSearchParams({ textToAnalyze: text });
    const response = await fetch(`/emotionDetector?${params.toString()}`);
    const body = await response.text();
    if (!response.ok) {
      throw new Error(body || "The text could not be analyzed.");
    }

    message.textContent = body;
  } catch (error) {
    message.textContent = error.message || "The service is temporarily unavailable.";
  } finally {
    button.disabled = false;
    button.textContent = "Analyze text";
  }
});

