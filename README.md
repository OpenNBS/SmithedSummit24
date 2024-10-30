# Note Block Studio @ Smithed Summit '24

<img src="https://smithed.net/assets/mountain2-1b30efda.webp" width="512px" />

This repository holds the data pack and resource pack created for [Note Block Studio](https://noteblock.studio/)'s booth in the [Smithed Summit 2024](https://smithed.net/summit).

We've decided to make this project public so everyone can learn from what we've made for our participation in the event!

## About

The pack generation is powered by [beet](https://github.com/mcbeet/beet), a powerful toolkit that serves as an authoring tool for data packs using the Python programming language. [mecha](https://github.com/mcbeet/mecha) and [bolt](https://github.com/mcbeet/bolt) are used to unlock some special syntax that makes working with multiple function files a breeze.

The song generation module was adapted from [pigstep](https://github.com/vberlier/pigstep), which itself is an adaptation of Note Block Studio's data pack export feature to generate songs programmatically via a beet plugin. The playback mechanic was upgraded to remove the function tree altogether, and instead relies on macros to play the right tick at the right time.

Songs are quantized to 20 t/s in a pre-processing step to allow any playback speed. Custom instruments that consist of vanilla Minecraft sounds and follow the path format introduced in NBS 3.11 are added automatically to the pack, provided the notes are in the two-octave range. Vanilla note block sounds support a six-octave range by dynamically including extended sounds from the extra notes resource pack.

The pack differs from NBS's native data pack export in that songs are **global** by design. That means the same song plays to everyone at the same time. There are lots of ways to tackle the scope of song playback, depending on whether you need different players to be able to hear different songs at a time, or hear the same song but be in different parts of the song at once, vs. the performance impact your world is able to bear.

Since performance was a heavy consideration for the event, we chose to make song playback global across the entire server, with the same sound sources serving for multiple players (which makes sense in a public event, as everyone can hear and vibe to the same music). This means it's not possible to have different players hearing different parts of a song, or even different songs at a given moment – unlike NBS's native data pack export, which tracks each song's progress individually and in a per-player basis — you could even have multiple songs playing at once to the same player! (_why_ would you is a different question.)

This repository serves as a public demo and showcase of everything seen in the Note Block Studio booth, so feel free to explore it as you wish! However, since many things in it were implemented in a hardcoded manner specifically for the Smithed Summit, keep in mind this repository is likely to be archived in the near future. Its code will serve as a base for an upcoming refactor of the native data pack export feature in NBS. This experiment served as a playground of many different techniques we explored. We learned a lot about Minecraft's sound engine workings and caveats, and actually figured out a bunch of clever things you can do with its limitations!

## Features

### Song playback

Note Block Studio hosted a two-week event called _Reach the Summit_ on our Discord server, where over thirty songs were submitted to be played during the Smithed Summit, amounting to over an hour of music! The songs featured in the event are not included in this repository for file size reasons, and because participants were informed that their source files would not be publicized. Instead, for the purpose of demonstration you'll find four songs made by me (Bentroen), which are sufficient to test the functionality of this pack. All mechanics were implemented to work with any number of songs, provided their metadata is inserted properly.

The pack is programmed to start playback as soon as it's loaded, but its rich set of playback control functions lets you control it as tightly as you need:

-   **Play:** start or resume playback.

    ```mcfunction
    /function nbs:global/play
    ```

-   **Pause:** pauses playback, retaining the same position in the current song.

    ```mcfunction
    /function nbs:global/pause
    ```

-   **Stop:** stops playback and seeks the current song back to the start.

    ```mcfunction
    /function nbs:global/stop
    ```

-   **Seek song:** move the song ahead or behind by a given amount of ticks.

    ```mcfunction
    /scoreboard players add songtime nbs 10    # seek the song 0.5s ahead
    /scoreboard players remove songtime nbs 10 # seek the song 0.5s back
    ```

    > NOTE: due to the way macros work, songs shift at the precise tick at which they end rather than at any tick greater than the song's length. If you advance past the end of the current song, it will not be skipped automatically. Advance the song manually to fix this (see below), and seek in small increments to avoid it.

-   **Next song:** advance to the next song in sequential order.

    ```mcfunction
    /function nbs:global/next
    ```

-   **Previous song:** go back to the previous song in sequential order.

    ```mcfunction
    /function nbs:global/prev
    ```

-   **Shuffle song:** change to a random song. If the randomizer picks the same song that's currently playing, it will advance to the next song in sequential order.

    ```mcfunction
    /function nbs:global/shuffle
    ```

-   **Toggle shuffle/sequential playback:** if enabled, a random song will play after the current one is finished. Otherwise, songs will play sequentially in alphabetical order.

    ```mcfunction
    /scoreboard players set shuffle nbs 1 # enable
    /scoreboard players set shuffle nbs 0 # disable
    ```

There are three different audio sources that play the same song simultaneously at different locations, to different targets:

-   **Speakers:** can be heard fully inside an 8-block range, with the sound completely fading away at a 12-block range.
-   **Loudpeakers:** can be heard fully inside a 32-block range, with the sound completely fading away at a 48-block range.
-   **Headphones:** when equipped by a player, can be heard globally everywhere they go.

Each of the three mechanics manipulate the target selectors' `distance` condition and `/playsound`'s `volume` and `minVolume` arguments to create three entirely different playback auditory experiences. To learn more about the implementation, take a look at the [`note.py`](src/note.py) module to see how each of the commands are generated.

### Speakers

Speakers and loudspeakers can be placed in the world with two different commands:

```mcfunction
/function nbs:global/place_speaker
/function nbs:global/place_loudspeaker
```

> NOTE: Placement is entirely handled by Animated Java, which places the rig relative to your player's position. Combine the commands above with `/execute positioned`, `aligned`, `rotated` etc. to make sure you get the right positioning!

Song playback triggers a beat animation in sync with the beat in the music speaker model, created with [Animated Java](https://animated-java.dev/), to make it bounce to the rhythm of the music. When a song ends and another one begins, the current song's title is shown in the action bar to players that can hear it The music speaker's display text is also updated to reflect the title of the current song.

### Headphones

Headphones can be collected in the world by interacting with an entity tagged `nbs_headphone_collectible`. This will give the player a headphone item that, when equipped in their head slot, will let them hear the music everywhere they go. Upon equipping the headphones, the title of the song currently being streamed on the server is displayed in the action bar. Players wearing headphones will have a note particle beating above their head in sync with the music!

### Models

The resource pack holds all the models used in the booth. Some models, such as the monitor screenshots and glowing note variations, are dynamically generated and added as an item predicate with a unique, auto-incrementing `custom_model_data` value. There are helper functions to set the alpha channels of images to specific values to make it work with Smithed Summit's emissive and no-shade shader resource packs, as well as generate a scrolling texture animation for the scrolling LED panel at the top of Note Block World's building.

### Album art paintings

Along with the songs, participants of the Reach the Summit event could submit album art to be placed in the walls of our booth, with credits to their preferred social media links. Clicking the paintings shows a message in the chat with a list of tracks submitted by each participant, as well as their Discord username, Minecraft IGN and a link to their YouTube channel. Advancements and functions for interaction detection are dynamically generated based in a JSON file containing the authors' submitted data.

## Credits

[encode42](https://github.com/encode42)

-   Monitor model
-   Album art and song submission compilation

[Kyrius](https://github.com/Kyrkis)

-   Speakers model and animation (boombox)

[rx](https://github.com/RitikShah)

-   Refactoring and development of the playback system

Participants listed in [`credits.md`](/assets/credits.md):

-   Album art and songs played during the event

## Special thanks

Our participation in the Smithed Summit wouldn't have been possible without the help of these amazing folks:

-   [**encode42**](https://github.com/encode42)

    for conceptualizing and building our entire booth, recruiting build assistance, helping with modelling, planning, writing, art direction, general feedback and a lot more – because "every build tells as a story"!

-   [**Vizeon**](https://www.youtube.com/@overlordvizeon)

    for being an awesome community manager, providing a lot of great feedback, making the song that got me through this entire month, being generally so enthusiastic about this project, and working in our marvelous panel!

-   [**Fizzy**](https://github.com/vberlier)

    for making [pynbs](https://github.com/OpenNBS/pynbs/), my first ever contact with programmatic note blocks (and now part of our organization!); beet/mecha/bolt which power this entire repository; and pigstep, which let me learn the power of combining beet with nbs, and served as the base for our refined playback system!

-   [**rx**](https://github.com/ritikshah)

    for tearing down, refactoring and upgrading the entire playback code of pigstep which I was using before, and for providing great guidance with beet and data pack knowledge (and for making the very announcement which let me know about the Summit!);

-   [**Kyrius**](https://github.com/Kyrkis)

    for contributing amazing models to our booth and providing a lot of resource pack and style assistance;

And also:

-   Everyone else from the [Smithed](https://smithed.net/) team for promoting such an awesome event!

-   [Bloom Host](https://bloom.host/) for generously sponsoring Smithed;

-   The entire NBS community, especially our financial contributors and those who submitted songs to play during the event. You make all of this possible!

###### Supporters

<img src="https://opencollective.com/opennbs/backers.svg" height="48px"/>

---

> This repository is published under the MIT license. See the [LICENSE](/LICENSE) file for more information.
