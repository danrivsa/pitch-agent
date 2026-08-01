# Projects

Notable projects Daniel has worked on:

## Game development

Daniel has participated in multiple game jams and has developed several games using Unity, C# and Java. Here are some of the most relevant ones:

- **Project:** [Pollicia del espacio](https://v3.globalgamejam.org/2018/games/pollicia-del-espacio)  
  **Description:** A 2D top-down shooter game developed in Unity during a 48-hour game jam. Implemented a dungeon system with multiple rooms, enemies, and a boss fight.

- **Project:** [Mayhem on Xmas](https://kegnor.itch.io/mayhem-on-christmas)  
  **Description:** A 2D shooter game developed in Unity during a 48-hour game jam on itch.io. Implemented a wave-based enemy system with increasing difficulty and a scoring system, the game features holiday-themed enemies.

- **Project:** [House of memories](https://danrivsa.itch.io/house-of-memories)  
  **Description:** A 2D game that explores the history of a broken family through the echoes of the past. Developed in Unity in 48h, it features a unique narrative structure and interactive storytelling elements.

- **Project:** [Charon's passage](https://danrivsa.itch.io/charons-passage)
  **Description:** A 2D survival  game developed in Unity during a 48-hour game jam. Implemented a wave-based enemy system with increasing difficulty and a scoring system, The game features charon's passage as a central theme, where players must navigate through the river styx to protect a soul to reach the afterlife.

## Robotics and AI

Daniel also has experience in robotics and AI, having worked on several projects involving computer vision, machine learning, and natural language processing. Here are some of the most relevant ones:

- **Weapon detection and surveillance system:** Developed a smart surveillance system powered with AWS and computer vision AI models to help automate the detection of incidents related to the presence of people in restricted areas, weapons, smoke, fire, and gunshots, aiding the security departments of multiple clients. The system works with a stack of AWS services, including S3, Lambda, Rekognition, and DynamoDB. Object classification was achieved by using AWS rekognition with a large dataset of the objects of interest. Gunshot classification was achieved by training a convolutional neural network in AWS sagemaker using a technique called transfer learning which consist on modifying the last two fully connected layers a convolutional neural network to perform a binary classification to properly distinguish gunshots from other urban sounds. A pipeline was created to capture the feed of the surveillance cameras, process the images and audio, and send alerts to the security team in case of an incident.

- **Robotic engineering :** Daniel worked as a robotics teacher and mentor to help a student build an automatic vacuum robot that identified "filth" and "dust" particles (portrayed by colored paper) and vacuumed them up. The robot was built using Arduino UNO and an ESP32 Cam. The robot was able to identify the particles using computer vision techniques. One of the main challenges was to fit a fully trained computer vision model into the ESP32 Cam, which has limited memory and processing power. To overcome this challenge, Daniel trained a model in the platform Edge Impulse, that provided a framework to optimize models for edge devices using a technique called model quantization, which reduces the size of the model without sacrificing accuracy. Daniel also programmed the robot's navigation and control system and piggybacked the FOMO algorythm (faster objects, more objects) to optimize dust detection. The robot was able to successfully identify and vacuum the particles, demonstrating the potential of computer vision in robotics.

## Domotics

- Daniel is a bit of a tinkerer and domotics enthusiast, he has built several home automation projects using Arduino, ESP32, and Homeassistant. One of the most relevant one is a smart water sensor that detects the amount of water left in a water tank and sends alerts to the user's phone when the water level is low. The sensor uses a waterproof ultrasonic sensor to measure the distance to the water surface and a WiFi module to send the data to a local MQTT broker. The user can also monitor the water level in real-time through a web interface.
