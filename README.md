# Terminal Lab 1

The practice environment for the 90-minute terminal lab in Introduction to Software Engineering. This repository contains **Lab 1 only**.

Use the printed student booklet during the session. The terminal runs Bash on Ubuntu inside your own GitHub Codespace.

## Start here

1. Sign in to your own GitHub account and open [Create your Lab 1 Codespace](https://codespaces.new/nalinabrol/terminal-labs?quickstart=1). Create it on the `main` branch. The smallest available machine is sufficient.
2. Wait for setup to finish. If prompted, choose **Trust Folder & Continue** for this course repository. A maximized **Lab 1 - Bash** terminal opens in the `terminal-labs` repository folder. The editor, Explorer, and AI panel start closed. Copilot is disabled in this workspace. You do not need to fork or clone anything manually.
3. Type:

   ```bash
   bash terminal-lab-1/start.sh
   ```

4. Enter the lab ID assigned by your instructor. Setup prints a `cd` command: run that exact command, followed by `pwd` and `cat identity.txt`. Write the path and identity values on page 1 of your printed booklet.

**This is a new repository and Codespace for the lab.** The earlier practice-and-revision sheet linked to a different repository. Keep that earlier Codespace separate. For the current booklet's first setup instruction, use this repository and the link above.

## Continue an existing attempt

Reopen your Lab 1 Codespace from [Your Codespaces](https://github.com/codespaces). At the repository root, run the setup command again with the same ID. It preserves your work and prints the command for returning to your lab folder.

Your attempt is stored in `lab-work/lab1-YOUR_ID/`. Do not delete this folder or the Codespace before your instructor has checked your work.

## Check your work

From your **lab root** (the folder containing `identity.txt`), run:

```bash
python3 ../../terminal-lab-1/check.py
```

The checker reads your files and reports which conditions pass. It does not repair, upload, or submit your work. Use the printed booklet for predictions, observations, and explanations.

To restore the terminal layout at any time, open the Command Palette and run **Lab 1: Focus Bash Terminal**.

## If setup fails

From the repository root, run:

```bash
bash scripts/verify_environment.sh
```

Show any error to your instructor. Setup never replaces an existing attempt. Do not delete your files to start over without help.

## At the end

Keep your files and Codespace for review. Use **Codespaces: Stop Codespace** in the Command Palette when finished working; reopen the same Codespace to continue later.
