import { useEffect, useRef, useState } from "react";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";

type Option = { id: string | number; label?: string };
type Props = {
  name: string;
  source: string;
  many: boolean;
  value: string[];
};

export function RelationField({ name, source, value }: Props) {
  const [options, setOptions] = useState<Option[]>([]);
  const checkedSet = new Set(value.map(String));
  const inputRefs = useRef<Record<string, HTMLInputElement | null>>({});

  useEffect(() => {
    fetch(source)
      .then((r) => r.json())
      .then(setOptions)
      .catch((err) => console.error("❌ Fetch failed:", err));
  }, [source]);

  return (
    <div className="space-y-2 border border-red-500 p-2">
      <div className="text-sm text-red-500">
        🧱 RelationField mounted for "{name}"
      </div>

      {options.map((opt) => {
        const id = String(opt.id);
        const initial = checkedSet.has(id);

        return (
          <div key={id} className="flex items-center gap-2">
            <input
              type="checkbox"
              name={name}
              value={id}
              defaultChecked={initial}
              hidden
              ref={(el) => {
                inputRefs.current[id] = el;
              }}
            />
            <Checkbox
              defaultChecked={initial}
              onCheckedChange={(state) => {
                const input = inputRefs.current[id];
                if (input) {
                  input.checked = state === true;
                }
              }}
              id={`${name}-${id}`}
            />
            <Label htmlFor={`${name}-${id}`}>{opt.label || id}</Label>
          </div>
        );
      })}
    </div>
  );
}
