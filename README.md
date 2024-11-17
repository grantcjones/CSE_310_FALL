# Overview

This is my attempt to use Sqlite to create and use a database for a game save file.

Using Sqlite, a file contains functions to save and load game data to and from a Sqlite database stored in the directory. These functions are called within the menu options within the game, and either update the information in the database, or pull from it to start the game at the saved destination.

This was for me to learn how to work with relational SQL databases locally.

{Provide a link to your YouTube demonstration. It should be a 4-5 minute demo of the software running, a walkthrough of the code, and a view of how created the Relational Database.}

[Software Demo Video](https://www.youtube.com/watch?v=-gYfJRopC5o)

# Relational Database

This database has 3 tables for the player, the enemies, and for the platforms.

The player table simply stores the player's id, their health, and their player's level. The enemies table stores the enemies and their saved positions, and the platforms table does the same.

# Development Environment

I used VSCode, as well as ChatGPT to help ensure that my database functions would work seamlessly together to read and write game data.

I used Sqlite to create a database to hold game data for a game created using pygame.

# Useful Websites

{Make a list of websites that you found helpful in this project}

- [W3 Schools](https://www.w3schools.com)
- [ChatGPT](http://openai.com)

# Future Work

A list of things that that I will fix, improve, and add in the future.

- Item 1: Need to implement more code to utilize saving and deleting saves. The Sqlite code is there, but it's not yet fully integrated into the game.
- Item 2: I want to add a more fleshed out start menu in the game to allow for different players to login and play their own files.
- Item 3: I would like to add the option to have multiple save files.