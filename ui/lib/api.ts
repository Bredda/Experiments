import { apiFetch } from "./fetch";
import { Event, Run } from "@/lib/types";

export async function getRuns(): Promise<Run[]> {
  return await apiFetch<Run[]>(`runs`, {
    cache: "no-store",
  });
}

export async function getRun(runId: string): Promise<Run> {
  return await apiFetch<Run>(`runs/${runId}`, {
    cache: "no-store",
  });
}

export async function getRunEvents(runId: string) {
  return await apiFetch<Event[]>(`runs/${runId}/events`, {
    cache: "no-store",
  });
}
