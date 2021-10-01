# GitHub action for checking in on Genshin Web Event

----------

Setup this repo, then forget the hassle of checking in to Genshin Daily Web Event manually.


### Setup Instruction
 * Fork this repo
 * Extract Cookies from [event page](https://webstatic-sea.mihoyo.com/ys/event/signin-sea/index.html?act_id=e202102251931481 "Event Page") using `Network` tab of `Developer Tools`
  * Required Cookies:
     * `_MHYUUID`
     * `account_id`
     * `cookie_token`
 * Set cookies in `Repo Settings > Secrets`
   * `_MHYUUID`     -> `MHYUUID`
   * `account_id`   -> `MHYACID`
   * `cookie_token` -> `MHYTOKEN`
 * Enjoy.