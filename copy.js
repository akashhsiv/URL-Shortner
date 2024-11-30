function copyToClipboard() {
  // Select the text of the short URL
  let shortUrl = document.querySelector("#shortUrl").textContent;

  // Use the Clipboard API for modern browsers
  navigator.clipboard
    .writeText(shortUrl)
    .then(() => {
      // Provide feedback to the user (optional)
      alert("Shortened URL copied to clipboard!");
    })
    .catch((err) => {
      console.error("Failed to copy text: ", err);
    });
}
