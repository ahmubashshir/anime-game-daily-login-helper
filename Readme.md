# GitHub action for checking in on Genshin Web Event

Setup this repo, then forget the hassle of checking in to Genshin Daily Web Event manually.


### Setup Instruction
 * Extract Cookies from [event page](https://webstatic-sea.mihoyo.com/ys/event/signin-sea/index.html?act_id=e202102251931481 "Event Page") using `Network` tab of `Developer Tools`
  * Required Cookies:
     * `_MHYUUID`
     * `account_id`
     * `cookie_token`
 * Set cookies in `Repo Settings > Secrets`
   * `_MHYUUID`     -> `MHYUUID`
   * `account_id`   -> `MHYACID`
   * `cookie_token` -> `MHYTOKEN`
 * Create a github action
   ```yaml
   # Can be anything you want
   name: Genshin check-in

   on:
     # Allow manual start
     workflow_dispatch:
     # Run job on 16:15UTC/00:15CST daily
     schedule:
     - cron: "15 16 * * *"

   jobs:
     # check-in now
     check-in:
       runs-on: ubuntu-latest
       steps:
       - uses: ahmubashshir/genshin-check-in@master
         with:
           # MiHoYo Account ID, required.
           id:    ${{ secrets.MHYACID }}
           # MiHoYo UUID, required.
           uuid:  ${{ secrets.MHYUUID }}
           # Auth Token, required.
           token: ${{ secrets.MHYTOKEN }}
           # Server name(append os_ before server name so that asia becomes
           # os_asia)
           region: ${{ secrets.REGION }}
           # Server UID
           uid: ${{ secrets.REGIONAL_UID }}
   ```
 * Enjoy.
