import {
  Item,
  ItemContent,
  ItemTitle,
  ItemDescription,
  ItemActions,
  ItemSeparator,
} from "@/components/ui/item";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Event } from "@/lib/types";
import { ArrowRight } from "@hugeicons/core-free-icons";
import { HugeiconsIcon } from "@hugeicons/react";
import Link from "next/link";

function formatTime(timestamp: string) {
  return new Date(timestamp).toLocaleTimeString("fr-FR", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

function eventLabel(event: Event) {
  switch (event.type) {
    case "agent.joined":
      return "Agent joined";

    case "action.proposed":
      return event.action?.content ?? "Action proposed";

    case "action.selected":
      return event.action?.content ?? "Action selected";

    case "message.published":
      return event.content ?? "Message published";

    default:
      return event.type;
  }
}

export function RunEvents({
  events,
  selected,
  onSelect,
}: {
  events: Event[];
  selected?: string | null;
  onSelect?: (eventId: string) => void;
}) {
  const handleSelected = (
    e: MouseEvent<HTMLAnchorElement, MouseEvent>,
    eventId: string,
  ) => {
    e.preventDefault();
    onSelect?.(eventId);
  };
  return (
    <ScrollArea className="h-full">
      <div className="p-3">
        {events.length === 0 ? (
          <div className="flex h-32 items-center justify-center text-sm text-muted-foreground">
            No events
          </div>
        ) : (
          <div className="space-y-1">
            {events.map((event) => (
              <>
                <Item
                  variant={selected === event.id ? "primary" : "muted"}
                  key={"event_" + event.id}
                  render={
                    <Link href="#" onClick={(e) => handleSelected(e, event.id)}>
                      <ItemContent>
                        <ItemTitle>
                          {event.step} - [{event.agent_id}] -{" "}
                          {eventLabel(event)}
                        </ItemTitle>
                        <ItemDescription>
                          <span> {formatTime(event.timestamp)}</span>
                        </ItemDescription>
                      </ItemContent>
                      <ItemActions>
                        <HugeiconsIcon icon={ArrowRight} className="size-4" />
                      </ItemActions>
                    </Link>
                  }
                />
                <ItemSeparator key={"sep_" + event.id} />
              </>
            ))}
          </div>
        )}
      </div>
    </ScrollArea>
  );
}
