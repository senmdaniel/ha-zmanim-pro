class HelloWorldCard extends HTMLElement {
  setConfig(config) {
    this.attachShadow({ mode: "open" });
    this.shadowRoot.innerHTML = `
      <ha-card header="Hello World">
        <div style="padding: 16px;">
          👋 Hello World from HACS
        </div>
      </ha-card>
    `;
  }

  set hass(hass) {}
}

customElements.define("hello-world-card", HelloWorldCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: "hello-world-card",
  name: "Hello World Card",
  description: "Simple test card"
});
