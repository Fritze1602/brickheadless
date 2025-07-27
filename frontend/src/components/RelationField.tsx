import { useEffect, useState } from "react";
import { Checkbox } from "@/components/ui/checkbox";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";

type Props = {
  name: string;
  source: string;
  many: boolean;
};

type Option = {
  id: string;
  label?: string;
  name?: string;
  slug?: string;
};

export function RelationField({ name, source, many }: Props) {
  const [options, setOptions] = useState<Option[]>([]);

  useEffect(() => {
    fetch(source)
      .then((res) => res.json())
      .then((data) => setOptions(data));
  }, [source]);

  return (
    <div className="space-y-2">
      {many ? (
        options.map((opt) => (
          <div key={opt.id} className="flex items-center gap-2">
            <Checkbox id={`${name}-${opt.id}`} name={name} value={opt.id} />
            <Label htmlFor={`${name}-${opt.id}`}>
              {opt.label || opt.name || opt.slug || opt.id}
            </Label>
          </div>
        ))
      ) : (
        <RadioGroup name={name}>
          {options.map((opt) => (
            <div key={opt.id} className="flex items-center gap-2">
              <RadioGroupItem value={opt.id} id={`${name}-${opt.id}`} />
              <Label htmlFor={`${name}-${opt.id}`}>
                {opt.label || opt.name || opt.slug || opt.id}
              </Label>
            </div>
          ))}
        </RadioGroup>
      )}
    </div>
  );
}
