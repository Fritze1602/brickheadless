import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

type Props = {
  name: string;
  label: string;
  value?: string;
};

export default function TextField({ name, label, value = "" }: Props) {
  return (
    <div className="mb-4 space-y-1">
      <Label htmlFor={name}>{label}</Label>
      <Input id={name} name={name} defaultValue={value} type="text" />
    </div>
  );
}
