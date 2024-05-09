import React from "react";
import {
  Card,
  CardBody,
  Heading,
  Image,
  Stack,
  Text,
} from "@chakra-ui/react";

// Define props interface if using TypeScript
interface EventProps {
  title: string;  // Title as a required prop
  host: string;   // Host as a required prop
  start_time: string;
  location: string;
  detailsUrl: string;
  date: string;
  image: string;
}

const Event: React.FC<EventProps> = ({ title, host, start_time, location, detailsUrl, date, image }) => {
  return (
    <>
      <Card maxW="sm">
        <CardBody>
        <Image
            src={image}  // Use image from props
            alt={`${title} event image`}
            borderRadius="lg"
          />
          <Stack mt="6" spacing="3">
            <Heading size="md">{title}</Heading>
            <Text>{date}</Text>
            <Text>{start_time}</Text>
            <Text>{location}</Text>
            <Text>{host}</Text>
          </Stack>
        </CardBody>
      </Card>
    </>
  );
};

export default Event;
