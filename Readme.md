# Script for checking in on an Anime Game Daily Web Event

Setup this repo, then forget the hassle of checking in to an Anime Game Daily Check-in Web Event manually.


### Setup Instruction
 * Extract Cookies from the Daily login event page using `Network` tab of `Developer Tools`
  * Required Cookies:
     * `_MHYUUID`
     * `account_id`
     * `cookie_token`
 * Set cookies in `Repo Settings > Secrets`
   * `_MHYUUID`     -> `UUID`
   * `account_id`   -> `ACCOUNT`
   * `cookie_token` -> `TOKEN`
 * Enable check ins for the game you want:
   * `GAMES` -> `:` separated `list`, like `$PATH`
   * Values:
     * `KenJin`  (Toggle rendaku on け & じ (けんじん))
     * `BouGai3` (Toggle rendaku on ぼ & が (ぼうがい))
     * `SutaaReiru` (Romaji of japanese :3)
 * Create a github action
   ```yaml
   # Can be anything you want
   name: A certain anime game check-in

   on:
     # Allow manual start
     workflow_dispatch:
     # Run job on 16:15UTC/00:15CST daily
     schedule:
     - cron: "15 16 * * *"
   # this got flagged by github.
   jobs:
     # check-in now
     check-in:
       runs-on: ubuntu-latest
       steps:
       - uses: ahmubashshir/anime-game-check-in@master
         with:
           # Account ID, required.
           id:    ${{ secrets.MHYACID }}
           # UUID, required.
           uuid:  ${{ secrets.MHYUUID }}
           # Auth Token, required.
           token: ${{ secrets.MHYTOKEN }}
   ```
 * Enjoy.
