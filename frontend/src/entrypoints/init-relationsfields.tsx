import { createRoot } from "react-dom/client";
import { RelationField } from "@/components/RelationField";

export function mountRelationFields() {
  document
    .querySelectorAll<HTMLElement>('[data-field-type="relation"]')
    .forEach((el) => {
      const name = el.dataset.name!;
      const source = el.dataset.source!;
      const many = el.dataset.many === "true";
      const selected = JSON.parse(el.dataset.selected || "[]");

      createRoot(el).render(
        <RelationField
          name={name}
          source={source}
          many={many}
          value={selected}
        />
      );
    });
}
