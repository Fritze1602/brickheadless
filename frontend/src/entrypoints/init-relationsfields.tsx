import { createRoot } from "react-dom/client";
import { RelationField } from "@/components/RelationField";

export function mountRelationFields() {
  const nodes = document.querySelectorAll<HTMLElement>(
    '[data-field-type="relation"]'
  );

  nodes.forEach((node) => {
    const name = node.dataset.name || "";
    const source = node.dataset.source || "";
    const many = node.dataset.many === "true";

    const root = createRoot(node);
    root.render(<RelationField name={name} source={source} many={many} />);
  });
}
