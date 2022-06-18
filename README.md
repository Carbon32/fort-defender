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
    <li><a href="#changelog">Changelog</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>


## About:

<img src = "https://i.imgur.com/z6x6LTA.png" width = 900 height = 600>

This is a Python Fort Defending video game, made in pure Python. The engine is able to handle a lot of tasks including: 

* Displaying sprites and updating them.
* Displaying an interactive background, supporting the day & night cycle.
* Displaying different animations (moving, death, attack...).
* Playing sounds and music.
* Displaying Interactive Buttons (repair, re-load, add towers...).
* Displaying a User Interface (Health, Ammunition and other stuff).
* Displaying & updating automatic towers (helps the player taking down enemy tanks).
* Displaying particles & different effects (including lighting, can be seen when you shoot a tank during night time).
* Increasing the game level after a few kills, making the game harder. 
* Displaying different types of enemies (including custom animations & health).
* Supporting multiple game resolutions.
* Enabling or disabling certain features including particles & clouds.
* And a few more minor features...

I made sure the engine is well optimized and all of the features are split into different classes.

Thanks to 'vnitti' for the background art. And also thanks to _Kassjak_ for the clouds art.
Each tank sprite is based on DietDoctorSprite's "M163 PIVADS".

I don't have a lot of time to work on this tiny game, the progress seems to be slower than what i've expected. The core of the engine needs to re-written.

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

## Changelog:

Changes made on: 06/19/2022

* Optimized the clouds system.
* Fixed some performance issues.
* Fixed the button handling.
* Rendering is now handled properly by the engine.
* You can choose different types of cannon balls, each one with it's own unique damage.
* Added health bars, for the fort and the enemies.
* You can see construction workers upgrading the armor whenever you click the upgrade button.
* Armor upgrades are now visible on the fort.
* Added a temporary container to improve text readbility during night time.
* Added accuracy rate to the cannon.
* Added two temporary enemy types.
* The cannon supports re-loading now, you can fire eight balls before having to re-load.
* "Start" will become "Continue" once you're in-game.
* Game speed is properly handled in different screen resolutions.

## License:

Distributed under the MIT License. See `LICENSE` for more information.

