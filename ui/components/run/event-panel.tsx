import { Event } from "@/lib/types";
import { Card, CardContent } from "../ui/card";
import { cn } from "@/lib/utils";
import { ScrollArea } from "../ui/scroll-area";

export function EventPanel({
  event,
  className,
}: {
  event: Event;
  className?: string;
}) {
  return (
    <ScrollArea className={cn(className)}>
      <Card className="h-full">
        <CardContent>
          <p>id: {event.id}</p>
          <p>timestamp: {event.timestamp}</p>
          <p>step: {event.step}</p>
          <p>type: {event.type}</p>
          <p>agent_id: {event.agent_id}</p>
          <p>room_id: {event.room_id}</p>
          <p>content: {event.content}</p>
          {event.action && (
            <>
              <p>Action</p>
              <p>agent_id: {event.action.agent_id}</p>
              <p>room_id: {event.action.room_id}</p>
              <p>content: {event.action.content}</p>
              <p>urgency: {event.action.urgency}</p>
              <p>relevance: {event.action.relevance}</p>
              <p>social_cost: {event.action.social_cost}</p>
            </>
          )}
          {!event.action && (
            <>
              <p>No action</p>
            </>
          )}
        </CardContent>
      </Card>
    </ScrollArea>
  );
}
