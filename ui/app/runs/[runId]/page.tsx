import { RunHeader } from "@/components/run/header";
import { RunViewer } from "@/components/run/viewer";
import { getRunEvents, getRun } from "@/lib/api";
import { Suspense } from "react";

export default async function RunPage({
  params,
}: {
  params: Promise<{ runId: string }>;
}) {
  const { runId } = await params;
  const run = await getRun(runId);
  const events = await getRunEvents(runId);

  return (
    <div className="h-screen overflow-hidden ">
      <Suspense fallback={<div>loading...</div>}>
        <RunHeader run={run} eventsLength={events.length} />
        <RunViewer events={events} />
      </Suspense>
    </div>
  );
}
