// frontend/src/init-textfields.tsx
import React from "react";
import ReactDOM from "react-dom/client";
import URLField from "@/components/URLField";

export function mountURLFields() {
  document
    .querySelectorAll<HTMLElement>('[data-field-type="url"]')
    .forEach((el) => {
      const name = el.dataset.name || "";
      const label = el.dataset.label || "";
      const value = el.dataset.value || "";

      const root = ReactDOM.createRoot(el);
      root.render(<URLField name={name} label={label} value={value} />);
    });
}
