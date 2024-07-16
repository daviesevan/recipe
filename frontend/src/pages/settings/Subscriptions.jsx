import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { AuthContext } from "@/context/AuthContext"

export default function Subscriptions() {
  return (
    <Card
    //   className="flex flex-1 items-center justify-center rounded-lg border border-dashed shadow-sm"
    >
      <div className="flex flex-col items-center gap-1 text-center px-24 py-24">
        <h3 className="text-2xl font-bold tracking-tight">
          You have no active subscriptions
        </h3>
        <p className="text-sm text-muted-foreground">
          You can start getting great benefits if you have one
        </p>
        <Button className="mt-4">Choose a plan</Button>
      </div>
    </Card>
  )
}
