import {
  Button,
  ButtonGroup,
  Card,
  CardBody,
  CardFooter,
  Divider,
  Heading,
  Image,
  Stack,
  Text,
} from "@chakra-ui/react";
import React from "react";

const Event = () => {
  return (
    <>
      <Card maxW="sm">
        <CardBody>
          <Image
            src="https://source.unsplash.com/1600x900/?Professional"
            alt="Green double couch with wooden legs"
            borderRadius="lg"
          />
          <Stack mt="6" spacing="3">
            <Heading size="md">Professional Development</Heading>
            <Text>
              {new Date(
                Math.random() * 120000000000 + 1660000000000
              ).toDateString()}
            </Text>
            <Text>4:00 PM</Text>
            <Text>GITC 3600 </Text>
            <Text>Cathy Gordio</Text>
          </Stack>
        </CardBody>
      </Card>
    </>
  );
};

export default Event;
