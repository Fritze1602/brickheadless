import "./index.css"; // Dein TailwindCSS-Einstiegspunkt

import { mountTextFields } from "./entrypoints/init-textfields";
import { mountURLFields } from "./entrypoints/init-urlfields";
import { mountRelationFields } from "./entrypoints/init-relationsfields";

// Helper: Mount direkt oder nach DOMContentLoaded
function runWhenDomReady(fn: () => void) {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", fn);
  } else {
    fn();
  }
}

runWhenDomReady(() => {
  console.log("[bricks] DOM ready – mounting React fields...");
  mountTextFields();
  mountURLFields();
  mountRelationFields();
});

export {};
