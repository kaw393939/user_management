import React from "react";
import Event from "@/components/Event";
import { SimpleGrid, Container } from "@chakra-ui/react";

// Dictionary of events with dynamic title and host
const events = [
  {
    title: "Professional Development",
    host: "Cathy Gordio",
    start_time: "4:00 PM",
    location: "GITC 3600",
    detailsUrl: "/events/professional-development",
    date: new Date().toDateString(),
    image: "https://source.unsplash.com/1600x900/?Professional"
  },
  {
    title: "Tech Trends 2024",
    host: "John Doe",
    start_time: "2:00 PM",
    location: "Tech Hall",
    detailsUrl: "/events/tech-trends",
    date: new Date().toDateString(),
    image: "https://source.unsplash.com/1600x900/?Technology"
  },
  {
    title: "Design Thinking",
    host: "Alice Johnson",
    start_time: "1:00 PM",
    location: "Design Studio",
    detailsUrl: "/events/design-thinking",
    date: new Date().toDateString(),
    image: "https://source.unsplash.com/1600x900/?Design"
  },
  {
    title: "Tech Trends 2024",
    host: "John Doe",
    start_time: "2:00 PM",
    location: "Tech Hall",
    detailsUrl: "/events/tech-trends",
    date: new Date().toDateString(),
    image: "https://source.unsplash.com/1600x900/?Technology"
  },
  {
    title: "Professional Development",
    host: "Cathy Gordio",
    start_time: "4:00 PM",
    location: "GITC 3600",
    detailsUrl: "/events/professional-development",
    date: new Date().toDateString(),
    image: "https://source.unsplash.com/1600x900/?Professional"
  },
  {
    title: "Tech Trends 2024",
    host: "John Doe",
    start_time: "2:00 PM",
    location: "Tech Hall",
    detailsUrl: "/events/tech-trends",
    date: new Date().toDateString(),
    image: "https://source.unsplash.com/1600x900/?Technology"
  },
  {
    title: "Design Thinking",
    host: "Alice Johnson",
    start_time: "1:00 PM",
    location: "Design Studio",
    detailsUrl: "/events/design-thinking",
    date: new Date().toDateString(),
    image: "https://source.unsplash.com/1600x900/?Design"
  },
  {
    title: "Tech Trends 2024",
    host: "John Doe",
    start_time: "2:00 PM",
    location: "Tech Hall",
    detailsUrl: "/events/tech-trends",
    date: new Date().toDateString(),
    image: "https://source.unsplash.com/1600x900/?Technology"
  },
  {
    title: "Professional Development",
    host: "Cathy Gordio",
    start_time: "4:00 PM",
    location: "GITC 3600",
    detailsUrl: "/events/professional-development",
    date: new Date().toDateString(),
    image: "https://source.unsplash.com/1600x900/?Professional"
  }
];

const Page = () => {
  return (
    <Container maxW="container.xl" centerContent>
      <SimpleGrid columns={{ sm: 1, md: 2, lg: 3 }} spacing={10} paddingTop="5" paddingBottom="5">
        {events.map((event, index) => (
          <Event key={index} title={event.title} host={event.host} start_time={event.start_time}
          location={event.location}
          detailsUrl={event.detailsUrl}
          date={event.date}
          image={event.image} />
        ))}
      </SimpleGrid>
    </Container>
  );
};

export default Page;
