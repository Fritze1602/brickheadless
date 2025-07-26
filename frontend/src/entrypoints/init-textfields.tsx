// frontend/src/init-textfields.tsx
import React from "react";
import ReactDOM from "react-dom/client";
import TextField from "@/components/TextField";

export function mountTextFields() {
  document
    .querySelectorAll<HTMLElement>('[data-field-type="text"]')
    .forEach((el) => {
      const name = el.dataset.name || "";
      const label = el.dataset.label || "";
      const value = el.dataset.value || "";

      const root = ReactDOM.createRoot(el);
      root.render(<TextField name={name} label={label} value={value} />);
    });
}
