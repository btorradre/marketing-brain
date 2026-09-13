#!/usr/bin/env python3
"""Fire AD1-AD3 on Seedance 2.5 as soon as the kie balance covers each one.

Cheapest first, one at a time, because each fire draws the balance down and the
next one has to clear on its own. Polls each task to completion and downloads it
before starting the next, so a stall never silently eats the budget.
"""
import json, subprocess, sys, time, pathlib

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import run as R                      # reuse balance/fire/poll + state.json

ORDER = [("AD2", 23), ("AD1", 25), ("AD3", 30)]   # 63 cr/sec
CHECK = 120                                        # seconds between balance checks
MAX_WAIT = 12 * 60 * 60                            # give up after 3h of waiting


def have(name):
    s = R.load()
    return bool(s["tasks"].get(name, {}).get("file"))


def main():
    waited = 0
    for name, dur in ORDER:
        need = 63 * dur
        if have(name):
            print(f"{name}: already downloaded", flush=True)
            continue
        while True:
            bal = R.balance()
            if bal >= need:
                print(f"{name}: balance {bal:.0f} >= {need}, firing", flush=True)
                R.fire([name])
                s = R.load()
                if not s["tasks"].get(name, {}).get("taskId"):
                    print(f"{name}: fire rejected, will retry", flush=True)
                    time.sleep(CHECK); waited += CHECK
                    continue
                break
            print(f"{name}: balance {bal:.0f}, need {need} (short {need-bal:.0f})", flush=True)
            time.sleep(CHECK); waited += CHECK
            if waited > MAX_WAIT:
                print(f"giving up after {waited//60} min waiting on credits", flush=True)
                return
        # poll this one to completion before moving on
        for _ in range(120):
            if R.poll():
                break
            time.sleep(20)
        print(f"{name}: {'downloaded' if have(name) else 'not finished'}", flush=True)
    print("autofire done", flush=True)


if __name__ == "__main__":
    main()
