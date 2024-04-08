# Script for checking in on an Anime Game Daily Web Event

Setup this repo, then forget the hassle of checking in to an Anime Game Daily Check-in Web Event manually.


### Setup Instruction
 * Extract Cookies from the Daily login event page using `Network` tab of `Developer Tools`
  * Required Cookies:
     * `_MHYUUID`
     * `ltmid_v2`|`account_mid_v2`
     * `ltoken_v2`
     * `cookie_token_v2`
     * `ltuid_v2`|`account_id_v2`
 * Set cookies in `Repo Settings > Secrets`
   * `ltuid_v2`  -> `ACCOUNT`
   * `ltoken_v2` -> `TOKEN`
   * `cookie_token_v2` -> `COOKIE`
   * `ltmid_v2`  -> `LOGIN`
   * `_MHYUUID`  -> `UUID`
 * Enable check ins for the game you want:
   * `GAMES` -> `:` separated `list`, like `$PATH`
   * Values:
     * `KenJin`      (Toggle rendaku on け & じ (けんじん))
     * `BouGai3`     (Toggle rendaku on ぼ & が (ぼうがい))
     * `HoshiRessha` (Just in romaji tl)
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
           id:    ${{ secrets.ACCOUNT }}
           # Auth Token, required.
           token: ${{ secrets.TOKEN }}
           login: ${{ secrets.LOGIN }}
           games:
           - KenJin
           - BouGai3
           - HoshiRessha
   ```
 * Enjoy.
