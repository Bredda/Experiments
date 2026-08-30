import {
  Item,
  ItemContent,
  ItemTitle,
  ItemDescription,
  ItemActions,
  ItemSeparator,
} from "@/components/ui/item";
import { ScrollArea } from "@/components/ui/scroll-area";
import { getRuns } from "@/lib/api";
import { ArrowRight } from "@hugeicons/core-free-icons";
import { HugeiconsIcon } from "@hugeicons/react";
import Link from "next/link";
import React from "react";
import { Suspense } from "react";

export default async function Home() {
  const runs = await getRuns();
  console.log(runs);
  return (
    <div className="h-screen overflow-hidden p-8">
      <div className="text-center">Runs</div>
      <Suspense fallback={<div>loading...</div>}>
        <div className="p-3 max-w-md mx-auto">
          <ScrollArea className="h-full">
            {runs.map((r) => (
              <React.Fragment key={r.run_id}>
                <Item
                  key={r.run_id}
                  render={
                    <Link href={"/runs/" + r.run_id}>
                      <ItemContent>
                        <ItemTitle>{r.scenario.name}</ItemTitle>
                        <ItemDescription>
                          <span>Run: {r.run_id}</span>
                        </ItemDescription>
                      </ItemContent>
                      <ItemActions>
                        <HugeiconsIcon icon={ArrowRight} className="size-4" />
                      </ItemActions>
                    </Link>
                  }
                />
                <ItemSeparator />
              </React.Fragment>
            ))}
          </ScrollArea>
        </div>
      </Suspense>
    </div>
  );
}
