<h1 align="center">Fort Defender:</h1><br>

<details>
  <summary>Table of Contents: </summary>
  <ol>
    <li>
      <a href="#about">About</a>
      <ul>
      </ul>
    </li>
    <li>
      <a href="#installation">Installation</a>
      <ul>
      </ul>
    </li>
    <li><a href="#contributors">Contributors</a></li>
    <li><a href="#changelog">Changelog</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>


## About:

<img src = "https://i.imgur.com/v5JnN81.png" width = 960 height = 540>


This is a Fort Defending video game, made in Python. The engine is able to handle a lot of tasks including: 

* Displaying sprites and updating them.
* Displaying an interactive background, supporting the day & night cycle.
* Displaying different animations (moving, death, attack...).
* Playing sounds and music.
* Displaying interactive Buttons (repair, re-load, add towers...).
* Displaying a User Interface (Health, Ammunition and other stuff).
* Displaying & updating automatic towers (helps the player taking down enemy tanks).
* Displaying particles & different effects (including lighting, can be seen when you shoot a tank during night time).
* Increasing the game level after a few kills, making the game harder. 
* Displaying different types of enemies (including custom animations & health).
* Supporting multiple game resolutions.
* Enabling or disabling certain features including particles & clouds.
* And a few more minor features...

I made sure the engine is well optimized and all of the features are split into different classes. I don't have a lot of time to work on this tiny game, the progress seems to be slower than what i've expected. The core of the engine needs to re-written.

## Installation:

To be able to run Fort Defender, you need to have Pygame installed on your computer.

<b>NOTE:</b> Messing with directories may cause some unforeseen consequences...

1. Clone the repository: 

   ```sh
   git clone https://github.com/Carbon32/fort-defender.git
   ```
2. Install all necessary libraries:

    ```sh
    pip install pygame
    ```

## Contributors:

<a href="https://vnitti.itch.io">Vnitti (Background)</a><br>
<a href="https://kassjak.itch.io">_Kassjak_ (Clouds)</a><br>
<a href="https://www.deviantart.com/dietdoctorsprite">DietDoctorSprite (Tanks)</a><br>

## Changelog:

Changes made on: 07/30/2022

* Improved the documentation.

## License:

Distributed under the MIT License. See `LICENSE` for more information.

